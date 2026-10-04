"""Deterministic, conservative three-valued evaluation of extracted legal rules.

Executable predicates live in logic.coverage and logic.exemptions.
Prose is never guessed into predicates. None represents missing knowledge.

Evaluation order (temporal precedence):
  1. Jurisdiction first. When the legal jurisdiction is not established
     (covered is None), the result is unknown even for pending or
     not-yet-effective rules, because no applicability statement can be made.
  2. Temporal standing second. Exact source dates (effective / operative
     date, enactment date, end date, candidate dates) take precedence over
     the declared status string; the string is only a fallback when no
     usable dates exist. Terminal states (ended, before enactment, future
     effective date with a precise day) short-circuit before coverage work.
  3. Executable coverage and exemptions last. Leaves whose fact starts with
     unresolved_ are open research questions, not executable predicates:
     they are stripped from the evaluated condition, recorded in
     review_required, and force unknown (fail-closed). A stripped side
     never establishes coverage and never establishes non-coverage.
"""
from datetime import date
from decimal import Decimal, DecimalException


_GAP_PREFIX = "unresolved_"


# Kanonisches Fakt-Vokabular, Spiegel von data/canonical_facts.json (alias_groups).
# Nur verifizierte bedeutungsidentische Aliase (gleiche Wertdomaene, gleiche Richtung,
# keine Negation). Verwandte, aber nicht identische Fakten (RSO-, unit_type-,
# Two-Unit-Gruppen) werden bewusst NICHT normalisiert; siehe related_groups_not_normalized.
_FACT_ALIASES = {
    "units": "unit_count",
}


def _canonical_fact(name):
    return _FACT_ALIASES.get(name, name)


def _normalize_facts(facts):
    if not isinstance(facts, dict):
        return facts
    normalized = {}
    for key, value in facts.items():
        canonical = _FACT_ALIASES.get(key, key)
        if canonical in normalized and key != canonical:
            continue
        normalized[canonical] = value
    return normalized


def evaluate_formula(expr, facts):
    """Evaluate safe typed arithmetic; return exact decimal string and diagnostics."""
    facts = _normalize_facts(facts)
    def visit(node):
        if not isinstance(node, dict):
            raise ValueError("Formula must be an object")
        if "value" in node or "fact" in node:
            raw = facts.get(_canonical_fact(node["fact"])) if "fact" in node else node["value"]
            if raw is None or raw == "" or raw == "unknown":
                return None, node.get("unit", "scalar"), {_canonical_fact(node["fact"]) if "fact" in node else "formula_value"}
            value = Decimal(str(raw))
            if not value.is_finite():
                raise ValueError("Non-finite numeric value")
            if abs(value.adjusted()) > 100:
                raise ValueError("Numeric magnitude outside supported bounds")
            return value, node.get("unit", "scalar"), set()
        operands = node.get("args", [])
        if not isinstance(operands, list):
            raise ValueError("Arithmetic arguments must be a list")
        op, args = node.get("op"), [visit(arg) for arg in operands]
        if op not in ("min", "max", "add", "sub", "mul", "div") or len(args) < 2:
            raise ValueError("Unsupported arithmetic operation or arity")
        units = [arg[1] for arg in args]
        missing = set().union(*(arg[2] for arg in args))
        if op in ("min", "max", "add", "sub"):
            if len(set(units)) != 1:
                raise ValueError("Incompatible units")
            unit = units[0]
        elif op == "mul":
            dimensions = [unit for unit in units if unit != "scalar"]
            if len(dimensions) > 1:
                raise ValueError("Multiplication requires scalar factors")
            unit = dimensions[0] if dimensions else "scalar"
        else:
            if len(args) != 2 or units[1] not in ("scalar", units[0]):
                raise ValueError("Incompatible division units")
            unit = "scalar" if units[0] == units[1] else units[0]
        if missing:
            return None, unit, missing
        values = [arg[0] for arg in args]
        if op == "min": value = min(values)
        elif op == "max": value = max(values)
        elif op == "add": value = sum(values, Decimal(0))
        elif op == "sub":
            value = values[0]
            for operand in values[1:]: value -= operand
        elif op == "mul":
            value = Decimal(1)
            for operand in values: value *= operand
        else: value = values[0] / values[1]
        return value, unit, set()
    try:
        value, unit, missing = visit(expr)
        return {"value": format(value, "f") if value is not None else None,
                "unit": unit, "missing_facts": sorted(missing), "error": None}
    except (ValueError, TypeError, DecimalException, ZeroDivisionError, OverflowError) as exc:
        return {"value": None, "unit": None, "missing_facts": [], "error": str(exc)}


def _truth_all(values):
    return False if False in values else (None if None in values else True)


def _truth_any(values):
    return True if True in values else (None if None in values else False)


def _strip_gap_flags(node):
    """Split an executable condition from open-research markers.

    Returns (cleaned, gaps). Leaves whose fact starts with
    unresolved_ are removed from the evaluated tree and their fact names
    are returned in gaps for review_required. A stripped side never establishes coverage.
    An emptied all collapses to True, an emptied any to False; a
    fully stripped side returns None so the caller can apply its default
    (coverage True / exemptions False).
    """
    gaps = []
    def walk(current):
        if isinstance(current, bool) or current is None or not isinstance(current, dict):
            return current
        fact = current.get("fact")
        if isinstance(fact, str) and fact.startswith(_GAP_PREFIX) and set(current) <= {"fact", "op", "value", "type"}:
            gaps.append(fact)
            return None
        if "not" in current and isinstance(current["not"], dict):
            inner = walk(current["not"])
            if inner is None:
                return None
            if inner is not current["not"]:
                return {"not": inner}
            return current
        for operator, neutral in (("all", True), ("any", False)):
            if operator in current and isinstance(current[operator], list):
                children = [walk(child) for child in current[operator]]
                children = [child for child in children if child is not None]
                if not children:
                    return neutral
                if len(children) == 1:
                    return children[0]
                return {operator: children}
        return current
    return walk(node), gaps


def evaluate_condition(expr, facts, trace=None):
    """Return (True/False/None, relevant missing fact names)."""
    trace = trace if trace is not None else []
    facts = _normalize_facts(facts)
    if isinstance(expr, bool):
        return expr, set()
    if not isinstance(expr, dict):
        return None, {"coverage_review"}
    combo_ops = [k for k in ("all", "any") if k in expr]
    if len(combo_ops) > 1:
        trace.append({"operator": "ambiguous", "value": None, "error": "Multiple top-level boolean operators"})
        return None, {"coverage_review"}
    for operator, reducer in (("all", _truth_all), ("any", _truth_any)):
        if operator in expr:
            if not isinstance(expr[operator], list):
                trace.append({"operator": operator, "value": None, "error": "Condition operands must be a list"})
                return None, {"coverage_review"}
            children = [evaluate_condition(child, facts, trace) for child in expr[operator]]
            result = reducer([child[0] for child in children])
            missing = set().union(*(child[1] for child in children)) if result is None else set()
            trace.append({"operator": operator, "value": result})
            return result, missing
    if "not" in expr:
        value, missing = evaluate_condition(expr["not"], facts, trace)
        return (None if value is None else not value), missing
    name, op = _canonical_fact(expr.get("fact")), expr.get("op", "eq")
    actual, expected = facts.get(name), expr.get("value")
    if actual in ("", "unknown", "declined", "refused"):
        actual = None
    if op == "exists":
        result = actual is not None
    elif actual is None:
        result = None
    else:
        try:
            if expr.get("type") == "date":
                low, high = _date_bounds(actual)
                expected_low, expected_high = _date_bounds(expected)
                if op in ("lt", "lte"):
                    true = high < expected_low if op == "lt" else high <= expected_low
                    false = low >= expected_high if op == "lt" else low > expected_high
                elif op in ("gt", "gte"):
                    true = low > expected_high if op == "gt" else low >= expected_high
                    false = high <= expected_low if op == "gt" else high < expected_low
                elif op == "eq":
                    true = low == high == expected_low == expected_high
                    false = high < expected_low or low > expected_high
                elif op == "ne":
                    true = high < expected_low or low > expected_high
                    false = low == high == expected_low == expected_high
                else:
                    true = false = False
                result = True if true else False if false else None
                trace.append({"fact": name, "operator": op, "expected": expected, "actual": actual, "value": result})
                return result, {name} if result is None else set()
            operations = {"eq": lambda: actual == expected, "ne": lambda: actual != expected,
                          "lt": lambda: actual < expected, "lte": lambda: actual <= expected,
                          "gt": lambda: actual > expected, "gte": lambda: actual >= expected,
                          "in": lambda: actual in expected, "not_in": lambda: actual not in expected}
            result = operations[op]() if op in operations else None
        except (TypeError, ValueError):
            result = None
    trace.append({"fact": name, "operator": op, "expected": expected, "actual": actual, "value": result})
    return result, {name or "coverage_review"} if result is None else set()


def _date_bounds(value):
    parts = str(value).split("-")
    year = int(parts[0])
    if len(parts) == 1:
        return date(year, 1, 1), date(year, 12, 31)
    month = int(parts[1])
    if len(parts) == 2:
        next_month = date(year + (month == 12), month % 12 + 1, 1)
        from datetime import timedelta
        return date(year, month, 1), next_month - timedelta(days=1)
    value = date.fromisoformat(value)
    return value, value


def _temporal_state(rule, query_date):
    """Derive temporal standing from exact source dates.

    Dates take precedence over the declared status string; the string is
    only a fallback when no usable dates exist. Precedence of terminal
    states: ended, then before-enactment, then not-yet-effective.
    Returns terminal / temporal_state / timing_unknown / notes.
    """
    notes = []
    terminal = None
    temporal_state = rule.get("status", "in_force")
    timing_unknown = False
    enacted = rule.get("enacted_at") or rule.get("enactment_date")
    if enacted:
        try:
            enacted_first, enacted_last = _date_bounds(enacted)
            if query_date < enacted_first:
                terminal = "before_enactment"
            elif enacted_first <= query_date < enacted_last:
                timing_unknown = True
                notes.append("Exact enactment date requires source review.")
        except (TypeError, ValueError):
            timing_unknown = True
            notes.append("Invalid enactment date requires source review.")
    effective = rule.get("effective_date") or rule.get("operative_date")
    if effective:
        try:
            first, last = _date_bounds(effective)
            if query_date < first:
                if terminal is None:
                    terminal = "not_yet_effective"
            elif query_date < last:
                timing_unknown = True
        except (TypeError, ValueError):
            timing_unknown = True
    elif temporal_state == "not_yet_effective":
        timing_unknown = True
    candidates = list(rule.get("effective_date_candidates", []))
    if rule.get("effective_date") and rule.get("operative_date") and rule["effective_date"] != rule["operative_date"]:
        candidates.extend([rule["effective_date"], rule["operative_date"]])
    if candidates:
        try:
            earliest = min(_date_bounds(value)[0] for value in candidates)
            latest = max(_date_bounds(value)[1] for value in candidates)
            if earliest <= query_date < latest:
                timing_unknown = True
                notes.append("Conflicting source effective dates require review.")
        except (TypeError, ValueError):
            timing_unknown = True
            notes.append("Invalid effective date candidates require review.")
    if rule.get("temporal_conflict") and not candidates:
        timing_unknown = True
        notes.append("Source timing conflict requires review.")
    end = rule.get("end_date")
    if end:
        try:
            first_end, last_end = _date_bounds(end)
            if query_date > last_end:
                terminal = "ended"
            elif query_date > first_end:
                timing_unknown = True
        except (TypeError, ValueError):
            timing_unknown = True
    if terminal == "ended":
        temporal_state = "ended"
    elif terminal == "before_enactment":
        temporal_state = "before_enactment"
    elif terminal == "not_yet_effective":
        temporal_state = "not_yet_effective"
    if timing_unknown:
        notes.append("Effective date cannot be determined precisely from the source.")
    return {"terminal": terminal, "temporal_state": temporal_state,
            "timing_unknown": timing_unknown, "notes": notes}


def evaluate_rule(rule, facts, as_of="2026-10-01"):
    """Evaluate a rule; result=None means omit it from address lookup output."""
    query_date = date.fromisoformat(as_of)
    facts = _normalize_facts(facts)
    trace, review = [], []
    status = rule.get("status", "in_force")
    if status == "withdrawn":
        status = "failed"
    invalid_status = status not in ("in_force", "not_yet_effective", "pending", "failed")
    jurisdiction = rule.get("jurisdiction", "")
    if rule.get("level") == "city":
        city, _, state = jurisdiction.rpartition(",")
        scope = {"all": [{"fact": "state", "value": state.strip()},
                         {"fact": "legal_city", "value": city.strip()}]}
    else:
        scope = {"fact": "state", "value": jurisdiction}
    covered, _ = evaluate_condition(scope, facts, trace)
    logic = rule.get("logic", {})
    if not isinstance(logic, dict):
        logic = {}
        review.append("Malformed executable logic requires source review.")
    raw_coverage = logic.get("coverage", rule.get("coverage_conditions"))
    if raw_coverage is None:
        raw_coverage = True if ("coverage" in logic or "coverage_conditions" in rule) else "untranslated coverage"
    raw_exemptions = logic.get("exemptions", rule.get("exemptions"))
    if raw_exemptions is None:
        raw_exemptions = False if ("exemptions" in logic or "exemptions" in rule) else "untranslated exemptions"
    # Explicit None with present key means "no executable condition supplied":
    # fail closed. A missing key everywhere keeps the legacy untranslated path.
    untranslated_coverage = ("coverage" in logic and logic["coverage"] is None) or ("coverage_conditions" in rule and rule["coverage_conditions"] is None)
    untranslated_exemptions = ("exemptions" in logic and logic["exemptions"] is None) or ("exemptions" in rule and rule["exemptions"] is None)
    coverage, coverage_gaps = _strip_gap_flags(raw_coverage)
    exemptions, exemption_gaps = _strip_gap_flags(raw_exemptions)
    if coverage is None:
        coverage = True
    if exemptions is None:
        exemptions = False
    for gap in coverage_gaps + exemption_gaps:
        review.append("Unresolved legal evidence requires source review: " + gap)
    questions = rule.get("questions", {})
    def question(key):
        if isinstance(key, str) and key.startswith(_GAP_PREFIX):
            return {"fact": key,
                    "question": "Source research required: which authoritative text resolves " + key.replace("_", " ") + "?",
                    "why_needed": "Open legal evidence blocks a reliable coverage decision; no user-supplied property fact can substitute the missing source.",
                    "source_doc_id": rule.get("source_doc_id"),
                    "acceptable_evidence": "Authoritative source text (statute, ordinance, or bill text) with retrieval date",
                    "may_decline": True, "research_task": True}
        if key == "untranslated_logic_review":
            return {"fact": key,
                    "question": "Source research required: which executable coverage or exemption condition follows from this rule's requirement and quoted span?",
                    "why_needed": "No executable coverage or exemption condition has been extracted for this rule, so no property fact can substitute the missing source study.",
                    "source_doc_id": rule.get("source_doc_id"),
                    "acceptable_evidence": "Executable logic with quote evidence, reviewed into the dataset",
                    "may_decline": True, "research_task": True}
        configured = questions.get(key)
        entry = configured if isinstance(configured, dict) else {"question": configured or "Please establish " + key.replace("_", " ") + "."}
        return {"fact": key, **entry, "why_needed": entry.get("why_needed", "This fact controls coverage or an exception."),
                "source_doc_id": rule.get("source_doc_id"), "acceptable_evidence": entry.get("acceptable_evidence", "Reliable property record or documented direct knowledge"),
                "may_decline": True}
    def assemble(result, explanation, missing, coverage_state, temporal_state, formula=None):
        if invalid_status and result is not None:
            result, temporal_state = "unknown", "unknown"
            review.append("Unrecognized source status requires review.")
        return {"team_rule_id": rule.get("team_rule_id"), "result": result,
                "as_of": as_of, "explanation": explanation,
                "conflict_flag": bool(rule.get("conflict_flag", False)) and result is not None,
                "missing_facts": sorted(missing) if result == "unknown" else [],
                "targeted_questions": [question(key) for key in sorted(missing)] if result == "unknown" else [],
                "dimensions": {"jurisdiction": covered, "coverage": coverage_state, "temporal_status": temporal_state},
                "review_required": list(dict.fromkeys(review)), "computed_value": formula,
                "trace": trace,
                "evidence": {key: rule.get(key) for key in ("citation", "source_doc_id", "source_url", "quoted_span", "retrieved_at")}}
    if status == "failed":
        return assemble(None, "Failed proposal is not an operative requirement.", set(), None, status)
    clock = _temporal_state(rule, query_date)
    review.extend(clock["notes"])
    if covered is False:
        return assemble(None, "Outside this rule\u0027s jurisdiction.", set(), None, status)
    if covered is None:
        if clock["terminal"] == "ended":
            return assemble(None, "Rule ended before the query date.", set(), None, "ended")
        temporal = "unknown" if clock["timing_unknown"] else clock["temporal_state"]
        return assemble("unknown", "Legal jurisdiction has not been established.", set(coverage_gaps + exemption_gaps), None, temporal)
    condition, needs = evaluate_condition(coverage, facts, trace)
    exempt, exemption_needs = evaluate_condition(exemptions, facts, trace)
    coverage_applies = _truth_all([True, condition, None if exempt is None else not exempt])
    if clock["terminal"] == "ended":
        return assemble(None, "Rule ended before the query date.", set(), coverage_applies, "ended")
    if clock["terminal"] == "before_enactment":
        return assemble("pending", "Before enactment; no operative requirement is established.", set(), coverage_applies, "before_enactment")
    if status == "pending":
        return assemble("pending", "Proposal is pending; it is not an operative requirement.", set(), coverage_applies, "pending")
    if clock["timing_unknown"]:
        return assemble("unknown", "Missing facts prevent a reliable coverage decision.", set(), None, "unknown")
    if clock["terminal"] == "not_yet_effective":
        return assemble("not_yet_effective", "Enacted, but the effective date is after the query date.", set(), coverage_applies, "not_yet_effective")
    if untranslated_coverage or untranslated_exemptions:
        review.append("No executable coverage condition extracted; source review required."
                      if untranslated_coverage else "No executable exemption condition extracted; source review required.")
        if coverage_gaps or exemption_gaps:
            # Offene Quellenluecken behalten ihre Research-Fragen (keine Maskierung):
            # Gap-Zweig hat Vorrang vor dem Untranslated-Zweig.
            return assemble("unknown", "Open legal evidence prevents a reliable coverage decision.",
                             set(coverage_gaps + exemption_gaps), None, "in_force")
        return assemble("unknown", "Missing executable logic prevents a reliable coverage decision.",
                         {"untranslated_logic_review"}, None, "in_force")
    if coverage_gaps or exemption_gaps:
        return assemble("unknown", "Open legal evidence prevents a reliable coverage decision.",
                         set(coverage_gaps + exemption_gaps), None, "in_force")
    if coverage_applies is False:
        return assemble("does_not_apply", "Coverage condition is false or an exemption is established.", set(), False, "in_force")
    if coverage_applies is None:
        missing = needs | exemption_needs
        missing = {fact for fact in missing if not (isinstance(fact, str) and fact.startswith(_GAP_PREFIX))}
        review_keys = {"coverage_review", "effective_date", "formula_value"}
        review.extend("Extracted condition requires source interpretation: " + key for key in missing & review_keys)
        missing -= review_keys
        return assemble("unknown", "Missing facts prevent a reliable coverage decision.", missing, None, "in_force")
    formula_logic = rule.get("logic", {})
    formula = evaluate_formula(formula_logic["formula"], facts) if isinstance(formula_logic, dict) and formula_logic.get("formula") else None
    if formula and (formula["missing_facts"] or formula["error"]):
        missing = set(formula["missing_facts"])
        if formula["error"]:
            review.append("Formula requires review: " + formula["error"])
        return assemble("unknown", "Coverage is established, but the applicable amount cannot be determined.", missing, True, "in_force", formula)
    return assemble("applies", "In force on the query date; coverage is established and no exemption applies.", set(), True, "in_force", formula)


def evaluate_rules(rules, facts, as_of="2026-10-01"):
    """Only explicit, evidenced supersedes edges can suppress a covered rule."""
    evaluated = {rule["team_rule_id"]: evaluate_rule(rule, facts, as_of) for rule in rules}
    initially_applies = {key for key, value in evaluated.items() if value["result"] == "applies"}
    supersedes_edges = []
    adj = {}
    for rule in rules:
        r_id = rule["team_rule_id"]
        if r_id not in initially_applies:
            continue
        for edge in rule.get("interactions", []):
            target_id = edge.get("target")
            if not target_id or not edge.get("evidence"):
                continue
            if edge.get("type") == "supersedes" and target_id in initially_applies:
                supersedes_edges.append((r_id, target_id, edge["evidence"]))
                adj.setdefault(r_id, set()).add(target_id)
            elif edge.get("type") == "possible_conflict":
                target = evaluated.get(target_id)
                if target and target["result"] in ("applies", "unknown"):
                    evaluated[r_id]["conflict_flag"] = target["conflict_flag"] = True
    in_cycle = set()
    def find_cycle(node, visited, path):
        visited.add(node)
        path.append(node)
        for neighbor in adj.get(node, []):
            if neighbor in path:
                cycle_start = path.index(neighbor)
                in_cycle.update(path[cycle_start:])
            elif neighbor not in visited:
                find_cycle(neighbor, visited, path)
        path.pop()
    visited_nodes = set()
    for node in list(adj.keys()):
        if node not in visited_nodes:
            find_cycle(node, visited_nodes, [])
    for r_id in in_cycle:
        evaluated[r_id]["conflict_flag"] = True
        evaluated[r_id]["review_required"].append("Supersession cycle requires review.")
    for source_id, target_id, evidence in supersedes_edges:
        if source_id not in in_cycle and target_id not in in_cycle:
            target = evaluated.get(target_id)
            if target and target["result"] == "applies":
                target["result"] = "superseded"
                target["explanation"] = "Superseded by " + source_id + ": " + evidence
    return [record for record in evaluated.values() if record["result"] is not None]
