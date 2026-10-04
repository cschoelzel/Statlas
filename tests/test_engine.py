import unittest

from navigator.engine import evaluate_condition, evaluate_rule, evaluate_rules, evaluate_formula


def rule(**updates):
    value = {"team_rule_id": "r1", "jurisdiction": "CA", "level": "state",
             "status": "in_force", "logic": {"coverage": True, "exemptions": False}}
    value.update(updates)
    return value


class EngineTests(unittest.TestCase):
    def test_three_valued_decisive_branches(self):
        unknown = {"fact": "owner_occupied", "value": True}
        self.assertEqual(evaluate_condition({"all": [False, unknown]}, {}), (False, set()))
        self.assertEqual(evaluate_condition({"any": [True, unknown]}, {}), (True, set()))
        self.assertEqual(evaluate_condition({"not": unknown}, {}), (None, {"owner_occupied"}))

    def test_unknown_exception_does_not_assert_applies(self):
        value = rule(logic={"coverage": True, "exemptions": {"all": [
            {"fact": "units", "op": "lte", "value": 2},
            {"fact": "owner_occupied", "value": True}]}})
        result = evaluate_rule(value, {"state": "CA", "units": 2})
        self.assertEqual(result["result"], "unknown")
        self.assertEqual(result["missing_facts"], ["owner_occupied"])
        self.assertEqual(evaluate_rule(value, {"state": "CA", "units": 3})["result"], "applies")

    def test_legal_city_not_postal_city(self):
        value = rule(jurisdiction="Los Angeles, CA", level="city")
        self.assertEqual(evaluate_rule(value, {"state": "CA", "postal_city": "Van Nuys"})["result"], "unknown")
        self.assertEqual(evaluate_rule(value, {"state": "CA", "legal_city": "Los Angeles"})["result"], "applies")
        self.assertIsNone(evaluate_rule(value, {"state": "CA", "legal_city": "San Diego"})["result"])

    def test_temporal_statuses(self):
        value = rule(status="not_yet_effective", effective_date="2027-07-01")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-10-01")["result"], "not_yet_effective")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2027-07-01")["result"], "applies")
        self.assertEqual(evaluate_rule(rule(status="pending"), {"state": "CA"})["result"], "pending")
        self.assertIsNone(evaluate_rule(rule(status="failed"), {"state": "CA"})["result"])
        self.assertEqual(evaluate_rule(rule(effective_date="2026"), {"state": "CA"})["result"], "unknown")

    def test_prose_not_silently_interpreted(self):
        value = rule(coverage_conditions="Older buildings")
        del value["logic"]
        self.assertEqual(evaluate_rule(value, {"state": "CA"})["result"], "unknown")

    def test_superseding_requires_evidence_and_coverage(self):
        local = rule(team_rule_id="local", interactions=[{"target": "r1", "type": "supersedes"}])
        results = evaluate_rules([rule(), local], {"state": "CA"})
        self.assertEqual(results[0]["result"], "applies")
        local["interactions"][0]["evidence"] = "Section 2 preserves stricter local cap."
        results = evaluate_rules([rule(), local], {"state": "CA"})
        self.assertEqual(results[0]["result"], "superseded")
        local["logic"]["coverage"] = {"fact": "owner_occupied", "value": False}
        results = evaluate_rules([rule(), local], {"state": "CA"})
        self.assertEqual(results[0]["result"], "applies")

    def test_possible_conflict_never_suppresses(self):
        local = rule(team_rule_id="local", interactions=[{"target": "r1", "type": "possible_conflict", "evidence": "Possible preemption."}])
        results = evaluate_rules([rule(), local], {"state": "CA"})
        self.assertTrue(all(result["conflict_flag"] for result in results))
        self.assertTrue(all(result["result"] == "applies" for result in results))

    def test_decimal_exact_addition(self):
        self.assertEqual(evaluate_formula({"op": "add", "args": [{"value": "0.1"}, {"value": "0.2"}]}, {})["value"], "0.3")

    def test_formula_min_cap(self):
        expr = {"op": "min", "args": [{"fact": "cpi", "unit": "percent"}, {"value": "4", "unit": "percent"}]}
        self.assertEqual(evaluate_formula(expr, {"cpi": "6"})["value"], "4")

    def test_formula_max_floor(self):
        expr = {"op": "max", "args": [{"value": "1", "unit": "percent"}, {"value": "0", "unit": "percent"}]}
        self.assertEqual(evaluate_formula(expr, {})["value"], "1")

    def test_formula_mixed_units_rejected(self):
        expr = {"op": "add", "args": [{"value": "1", "unit": "USD"}, {"value": "2", "unit": "percent"}]}
        self.assertIsNotNone(evaluate_formula(expr, {})["error"])

    def test_formula_scalar_multiplication(self):
        expr = {"op": "mul", "args": [{"value": "1.5"}, {"fact": "rent", "unit": "USD"}]}
        self.assertEqual(evaluate_formula(expr, {"rent": "2000"})["value"], "3000.0")

    def test_formula_dimension_multiplication_rejected(self):
        expr = {"op": "mul", "args": [{"value": "2", "unit": "USD"}, {"value": "2", "unit": "USD"}]}
        self.assertIsNotNone(evaluate_formula(expr, {})["error"])

    def test_formula_divide_by_zero(self):
        self.assertIsNotNone(evaluate_formula({"op": "div", "args": [{"value": "2"}, {"value": "0"}]}, {})["error"])

    def test_formula_missing_input(self):
        self.assertEqual(evaluate_formula({"fact": "rent", "unit": "USD"}, {})["missing_facts"], ["rent"])

    def test_formula_nonfinite_rejected(self):
        self.assertIsNotNone(evaluate_formula({"value": "NaN"}, {})["error"])

    def test_formula_subtract_and_divide(self):
        expr = {"op": "div", "args": [{"op": "sub", "args": [{"value": "12", "unit": "USD"}, {"value": "2", "unit": "USD"}]}, {"value": "5", "unit": "USD"}]}
        self.assertEqual(evaluate_formula(expr, {})["value"], "2")
        self.assertEqual(evaluate_formula(expr, {})["unit"], "scalar")

    def test_missing_formula_changes_result(self):
        value = rule(logic={"coverage": True, "exemptions": False, "formula": {"fact": "rent", "unit": "USD"}})
        self.assertEqual(evaluate_rule(value, {"state": "CA"})["result"], "unknown")

    def test_source_timing_is_review_not_property_question(self):
        result = evaluate_rule(rule(status="not_yet_effective"), {"state": "CA"})
        self.assertEqual(result["result"], "unknown")
        self.assertEqual(result["targeted_questions"], [])
        self.assertTrue(result["review_required"])

    def test_unknown_jurisdiction_future_rule(self):
        result = evaluate_rule(rule(effective_date="2027-01-01"), {})
        self.assertEqual(result["result"], "unknown")
        self.assertIsNone(result["dimensions"]["jurisdiction"])

    def test_enactment_boundary(self):
        value = rule(enacted_at="2026-07-20", effective_date="2027-07-01")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-07-19")["result"], "pending")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-07-20")["result"], "not_yet_effective")

    def test_end_date_inclusive(self):
        value = rule(end_date="2026-10-01")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-10-01")["result"], "applies")
        self.assertIsNone(evaluate_rule(value, {"state": "CA"}, "2026-10-02")["result"])

    def test_conflicting_dates_only_ambiguous_between(self):
        value = rule(effective_date="2026-03-01", effective_date_candidates=["2026-01-01", "2026-03-01"])
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-02-01")["result"], "unknown")
        self.assertEqual(evaluate_rule(value, {"state": "CA"}, "2026-03-01")["result"], "applies")

    def test_exact_co_boundary(self):
        expr = {"fact": "certificate_of_occupancy_date", "op": "lte", "value": "1979-06-13", "type": "date"}
        self.assertTrue(evaluate_condition(expr, {"certificate_of_occupancy_date": "1979-06-13"})[0])
        self.assertFalse(evaluate_condition(expr, {"certificate_of_occupancy_date": "1979-06-14"})[0])

    def test_partial_co_date_not_inferred(self):
        expr = {"fact": "certificate_of_occupancy_date", "op": "lte", "value": "1979-06-13", "type": "date"}
        self.assertIsNone(evaluate_condition(expr, {"year_built": 1978})[0])
        self.assertIsNone(evaluate_condition(expr, {"certificate_of_occupancy_date": "1979"})[0])

    def test_refusal_remains_unknown(self):
        self.assertIsNone(evaluate_condition({"fact": "owner_occupied", "value": True}, {"owner_occupied": "declined"})[0])

    def test_question_has_evidence_and_refusal_option(self):
        result = evaluate_rule(rule(logic={"coverage": {"fact": "units", "op": "gt", "value": 2}, "exemptions": False}), {"state": "CA"})
        self.assertTrue(result["targeted_questions"][0]["may_decline"])
        self.assertTrue(result["targeted_questions"][0]["acceptable_evidence"])

    def test_invalid_date_does_not_crash(self):
        result = evaluate_rule(rule(effective_date="2026-99-99"), {"state": "CA"})
        self.assertEqual(result["result"], "unknown")

    def test_missing_translation_is_unknown(self):
        value = rule()
        del value["logic"]
        result = evaluate_rule(value, {"state": "CA"})
        self.assertEqual(result["result"], "unknown")
        self.assertTrue(result["review_required"])
        self.assertEqual(result["targeted_questions"], [])

    def test_withdrawn_is_not_operative(self):
        self.assertIsNone(evaluate_rule(rule(status="withdrawn"), {"state": "CA"})["result"])

    def test_invalid_status_closed(self):
        self.assertEqual(evaluate_rule(rule(status="invented"), {"state": "CA"})["result"], "unknown")

    def test_operative_date_alias(self):
        self.assertEqual(evaluate_rule(rule(operative_date="2027-01-01"), {"state": "CA"})["result"], "not_yet_effective")

    def test_unknown_jurisdiction_preserves_temporal_dimension(self):
        result = evaluate_rule(rule(effective_date="2027-01-01"), {})
        self.assertEqual(result["dimensions"]["temporal_status"], "not_yet_effective")

    def test_supersession_chain_independent_of_order(self):
        a = rule(team_rule_id="a", interactions=[{"type": "supersedes", "target": "b", "evidence": "Statute A"}])
        b = rule(team_rule_id="b", interactions=[{"type": "supersedes", "target": "c", "evidence": "Statute B"}])
        c = rule(team_rule_id="c")
        first = {r["team_rule_id"]: r["result"] for r in evaluate_rules([a, b, c], {"state": "CA"})}
        second = {r["team_rule_id"]: r["result"] for r in evaluate_rules([c, b, a], {"state": "CA"})}
        self.assertEqual(first, second)
        self.assertEqual(first, {"a": "applies", "b": "superseded", "c": "superseded"})

    def test_malformed_condition_operands(self):
        self.assertEqual(evaluate_condition({"all": None}, {}), (None, {"coverage_review"}))

    def test_huge_formula_number_refused(self):
        expr = {"op": "mul", "args": [{"value": "1e999999"}, {"value": "1e999999"}]}
        self.assertIsNotNone(evaluate_formula(expr, {})["error"])

    def test_malformed_formula_operands(self):
        self.assertIsNotNone(evaluate_formula({"op": "add", "args": None}, {})["error"])

    def test_malformed_logic_unknown(self):
        self.assertEqual(evaluate_rule(rule(logic="prose"), {"state": "CA"})["result"], "unknown")

    def test_in_and_not_in_operators(self):
        self.assertTrue(evaluate_condition({"fact": "legal_city", "op": "in", "value": ["Hoboken", "Jersey City"]}, {"legal_city": "Hoboken"})[0])
        self.assertFalse(evaluate_condition({"fact": "legal_city", "op": "in", "value": ["Hoboken"]}, {"legal_city": "Newark"})[0])
        self.assertIsNone(evaluate_condition({"fact": "legal_city", "op": "in", "value": ["Hoboken"]}, {})[0])
        self.assertTrue(evaluate_condition({"fact": "legal_city", "op": "not_in", "value": ["Newark"]}, {"legal_city": "Hoboken"})[0])
        self.assertFalse(evaluate_condition({"fact": "legal_city", "op": "not_in", "value": ["Hoboken"]}, {"legal_city": "Hoboken"})[0])
        self.assertIsNone(evaluate_condition({"fact": "legal_city", "op": "not_in", "value": ["Hoboken"]}, {})[0])

    def test_exists_operator(self):
        self.assertTrue(evaluate_condition({"fact": "rent", "op": "exists"}, {"rent": "2000"})[0])
        self.assertFalse(evaluate_condition({"fact": "rent", "op": "exists"}, {})[0])

    def test_refused_facts_stay_unknown(self):
        for expr in ({"fact": "units", "value": 2},
                     {"fact": "units", "op": "in", "value": [2, 3]},
                     {"fact": "units", "op": "gt", "value": 2}):
            self.assertIsNone(evaluate_condition(expr, {"units": "refused"})[0])
            self.assertIsNone(evaluate_condition(expr, {"units": "declined"})[0])
        result = evaluate_rule(rule(logic={"coverage": {"fact": "units", "op": "gt", "value": 2}, "exemptions": False}), {"state": "CA", "units": "refused"})
        self.assertEqual(result["result"], "unknown")
        self.assertEqual(result["missing_facts"], ["unit_count"])

    def test_gap_flags_force_unknown_not_applies(self):
        value = rule(logic={"coverage": {"all": [{"fact": "state", "value": "CA"}, {"fact": "unresolved_legal_evidence_D001_1", "value": True}]}, "exemptions": False})
        result = evaluate_rule(value, {"state": "CA"})
        self.assertEqual(result["result"], "unknown")
        self.assertEqual(result["missing_facts"], ["unresolved_legal_evidence_D001_1"])
        self.assertEqual(len(result["targeted_questions"]), 1)
        research = result["targeted_questions"][0]
        self.assertTrue(research.get("research_task"))
        self.assertTrue(research.get("why_needed"))
        self.assertTrue(research.get("acceptable_evidence"))
        self.assertTrue(any("unresolved_legal_evidence_D001_1" in note for note in result["review_required"]))
    def test_gap_flags_under_not_force_unknown(self):
        value = rule(logic={"coverage": {"not": {"fact": "unresolved_legal_evidence_D001_9", "value": True}}, "exemptions": False})
        result = evaluate_rule(value, {"state": "CA", "unresolved_legal_evidence_D001_9": True})
        self.assertEqual(result["result"], "unknown")
        self.assertEqual(result["missing_facts"], ["unresolved_legal_evidence_D001_9"])
    def test_gaps_survive_unknown_jurisdiction(self):
        value = rule(logic={"coverage": {"all": [{"fact": "state", "value": "CA"}, {"fact": "unresolved_legal_evidence_D003_1", "value": True}]}, "exemptions": False})
        result = evaluate_rule(value, {})
        self.assertEqual(result["result"], "unknown")
        self.assertIn("unresolved_legal_evidence_D003_1", result["missing_facts"])
        self.assertTrue(any(item.get("research_task") for item in result["targeted_questions"]))
    def test_explicit_none_logic_stays_unknown(self):
        value = rule(logic={"coverage": None, "exemptions": False})
        result = evaluate_rule(value, {"state": "CA"})
        self.assertEqual(result["result"], "unknown")
        self.assertTrue(any("executable" in note for note in result["review_required"]))
        value = rule(logic={"coverage": True, "exemptions": None})
        result = evaluate_rule(value, {"state": "CA"})
        self.assertEqual(result["result"], "unknown")
        exempt_gap = rule(logic={"coverage": True, "exemptions": {"fact": "unresolved_legal_condition_state_notice_exemption", "value": True}})
        self.assertEqual(evaluate_rule(exempt_gap, {"state": "CA"})["result"], "unknown")

    def test_unknown_jurisdiction_beats_pending_and_future(self):
        self.assertEqual(evaluate_rule(rule(status="pending"), {})["result"], "unknown")
        future = evaluate_rule(rule(status="pending", effective_date="2027-01-01"), {})
        self.assertEqual(future["result"], "unknown")
        self.assertEqual(future["dimensions"]["temporal_status"], "not_yet_effective")



    def test_open_gap_beats_false_coverage(self):
        value = rule(logic={"coverage": {"all": [{"fact": "is_covered", "value": True},
            {"fact": "unresolved_legal_evidence_D001_9", "value": True}]}, "exemptions": False})
        result = evaluate_rule(value, {"state": "CA", "is_covered": False})
        self.assertEqual(result["result"], "unknown")
        self.assertTrue(result["targeted_questions"])

    def test_open_gap_beats_established_exemption(self):
        value = rule(logic={"coverage": {"all": [{"fact": "state", "value": "CA"},
            {"fact": "unresolved_legal_evidence_D001_9", "value": True}]},
            "exemptions": {"fact": "is_exempt", "value": True}})
        result = evaluate_rule(value, {"state": "CA", "is_exempt": True})
        self.assertEqual(result["result"], "unknown")
        self.assertTrue(result["targeted_questions"])

    def test_decisive_results_unchanged_without_gaps(self):
        value = rule(logic={"coverage": True, "exemptions": False})
        self.assertEqual(evaluate_rule(value, {"state": "CA"})["result"], "applies")
        negative = rule(logic={"coverage": {"fact": "is_covered", "value": True}, "exemptions": False})
        self.assertEqual(evaluate_rule(negative, {"state": "CA", "is_covered": False})["result"], "does_not_apply")

if __name__ == "__main__":
    unittest.main()
