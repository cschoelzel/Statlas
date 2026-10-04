"""Punkt 4 aus reports/ziel_100_prozent.md: Fakt-Vokabular geschlossen.

Jeder coverage-/exemption-/formula-Fakt aus data/rules.json muss auf genau
eine Kategorie des Registers data/canonical_facts.json fallen
(Prioritaet: Gap > Alias > supplied-only > kanonischer Eintrag).
Tote Register-Fakten sind nur als dokumentierte Ausnahme erlaubt.
year_built darf nie als Besiedlungs-/Nutzungsdatum wirken (P5-Abgrenzung).
"""
import json
import unittest
from pathlib import Path

from navigator import engine
from navigator.geography import resolve_address

ROOT = Path(__file__).resolve().parents[1]
RULES = json.load(open(ROOT / "data" / "rules.json"))
REGISTER = json.load(open(ROOT / "data" / "canonical_facts.json"))
ENTRIES = set(REGISTER["entries"])
GAP_FACTS = set(REGISTER["gap_facts"]["facts"])
SUPPLIED = list(REGISTER["supplied_by_geography"]["facts"])
ALIAS_GROUPS = REGISTER["alias_groups"]
ALIAS_MEMBERS = {a for g in ALIAS_GROUPS for a in g["aliases"]}
ALIAS_TARGETS = {g["canonical"] for g in ALIAS_GROUPS}

# Bewusste Ausnahmen: Register-Fakten ohne Regelverwendung.
# Parzellendatensatz-Felder, die geography.py liefert, aber (derzeit) keine
# Regel als coverage-Bedingung liest. year_built ist Baujahr laut Assessor
# und darf nie als occupancy-/certificate-Datum interpretiert werden.
ALLOWED_DEAD = {
    "county": "Census-Jurisdiktion liegt vor, wird aber von keiner Regel als coverage-Fakt gelesen.",
    "supplied_state": "Reine Post-/Datensatz-Herkunftsangabe; Jurisdiktion nutzt nur Census-state.",
    "use_code": "Assessor-Nutzungsschluessel, unverified, von keiner Regel gelesen.",
    "use_description": "Assessor-Nutzungsbeschreibung, unverified, von keiner Regel gelesen.",
    "year_built": "Assessor-Baujahr, unverified; darf nie als occupancy-Datum verwendet werden (P5).",
}
# Registrierte Eingabe-Schreibweisen, die nie wortwoertlich im Regeltext
# stehen, sondern von der Engine auf kanonisch normalisiert werden.
ALLOWED_UNUSED_ALIAS_INPUTS = {
    "units": "Alias-Eingabe fuer kanonisch unit_count; Engine normalisiert Keys und Blaetter.",
}


def _walk_facts(node, out):
    if isinstance(node, dict):
        fact = node.get("fact")
        if isinstance(fact, str) and not any(k in node for k in ("all", "any", "not")):
            out.add(fact)
        for key, value in node.items():
            if key == "fact":
                continue
            _walk_facts(value, out)
    elif isinstance(node, list):
        for item in node:
            _walk_facts(item, out)


def collect_rule_facts(rule):
    """Alle Fakt-Blattwerte aus logic (rekursiv durch all/any/not,
    einschliesslich coverage/exemptions) plus formula-Referenzen
    (fact/unit). Das Register wurde per jq-Volltextinventar gebaut;
    logic enthaelt weitere Branches mit Fakt-Blaettern
    (z.B. prohibited_screening_factors, relocation_triggered_by),
    die mitlaufen muessen, sonst gaebe es Schein-Tote."""
    out = set()
    logic = rule.get("logic", {})
    if isinstance(logic, dict):
        _walk_facts(logic, out)
    _walk_facts(rule.get("formula"), out)
    # Legacy-Spiegel neben logic (falls vorhanden) zaehlen mit.
    _walk_facts(rule.get("coverage_conditions"), out)
    legacy_ex = rule.get("exemptions")
    _walk_facts(legacy_ex if isinstance(legacy_ex, (dict, list)) else None, out)
    return out


ALL_RULE_FACTS = set()
for _rule in RULES:
    ALL_RULE_FACTS |= collect_rule_facts(_rule)


def classify(fact):
    """Genau eine Kategorie pro Fakt (Prioritaet Gap > Alias > supplied-only > Eintrag)."""
    if fact in GAP_FACTS:
        return "gap"
    if fact in ALIAS_MEMBERS:
        return "alias"
    if fact in ENTRIES:
        return "canonical"
    if fact in SUPPLIED:
        return "supplied-only"
    return None


def jurisdiction_base(rule):
    if rule.get("level") == "city":
        city, _, state = rule.get("jurisdiction", "").rpartition(",")
        return {"state": state.strip(), "legal_city": city.strip()}
    if rule.get("jurisdiction"):
        return {"state": rule["jurisdiction"]}
    return {}


class FactVocabularyTests(unittest.TestCase):
    def test_formula_references_collected(self):
        formula_rules = [r for r in RULES
                         if isinstance(r.get("logic"), dict) and r["logic"].get("formula")]
        self.assertGreaterEqual(len(formula_rules), 1)
        self.assertIn("rental_debt_owed", ALL_RULE_FACTS)

    def test_every_rule_fact_has_exactly_one_category(self):
        unclassified = sorted(f for f in ALL_RULE_FACTS if classify(f) is None)
        self.assertEqual(unclassified, [])
        cats = {}
        for fact in ALL_RULE_FACTS:
            cats.setdefault(classify(fact), []).append(fact)
        self.assertEqual(sum(len(v) for v in cats.values()), len(ALL_RULE_FACTS))

    def test_aliases_normalize_to_canonical(self):
        self.assertGreaterEqual(len(ALIAS_GROUPS), 1)
        for group in ALIAS_GROUPS:
            canonical = group["canonical"]
            self.assertIn(canonical, ENTRIES)
            for alias in group["aliases"]:
                self.assertEqual(engine._canonical_fact(alias), canonical)
                self.assertEqual(engine._normalize_facts({alias: 4}),
                                 {canonical: 4})
                self.assertEqual(engine._normalize_facts({canonical: 4}),
                                 {canonical: 4})
                leaf_alias = {"fact": alias, "op": "gte", "value": 3}
                leaf_canon = {"fact": canonical, "op": "gte", "value": 3}
                self.assertEqual(
                    engine.evaluate_condition(leaf_alias, {alias: 4}),
                    engine.evaluate_condition(leaf_canon, {canonical: 4}))
                self.assertEqual(
                    engine.evaluate_condition(leaf_alias, {canonical: 4})[0], True)

    def test_gap_facts_fail_closed_with_research_task(self):
        gaps_in_rules = sorted(f for f in ALL_RULE_FACTS if f in GAP_FACTS)
        self.assertEqual(sorted(GAP_FACTS), gaps_in_rules)
        for gap in gaps_in_rules:
            with self.subTest(gap=gap):
                probe = {"team_rule_id": "p4-gap-probe", "jurisdiction": "CA",
                         "level": "state", "status": "in_force",
                         "logic": {"coverage": {"fact": gap, "op": "eq", "value": True},
                                    "exemptions": False},
                         "questions": {}}
                for facts in ({"state": "CA"}, {"state": "CA", gap: True}):
                    result = engine.evaluate_rule(probe, dict(facts))
                    self.assertNotEqual(result["result"], "applies")
                    self.assertEqual(result["result"], "unknown")
                    questions = [q for q in result["targeted_questions"]
                                 if q["fact"] == gap]
                    self.assertEqual(len(questions), 1)
                    self.assertTrue(questions[0].get("research_task"))
                    self.assertTrue(questions[0].get("why_needed"))
                    self.assertTrue(any(gap in r for r in result["review_required"]))

    def test_supplied_facts_filled_by_geography(self):
        geo_src = (ROOT / "navigator" / "geography.py").read_text()
        app_src = (ROOT / "navigator" / "app.py").read_text()
        for fact in SUPPLIED:
            with self.subTest(fact=fact):
                self.assertTrue("'%s'" % fact in geo_src or '"%s"' % fact in geo_src
                                or "'%s'" % fact in app_src or '"%s"' % fact in app_src)
        resolved = resolve_address(
            {"address_id": "P4-PROBE-NONEXISTENT", "state": "CA",
             "year_built": "1990", "units": "4", "use_code": "101",
             "use_description": "Single Family",
             "source_dataset": "p4-probe", "retrieved_at": "2026-10-04"})
        self.assertEqual(resolved["facts"].get("supplied_state"), "CA")
        self.assertEqual(resolved["facts"].get("year_built"), 1990)
        self.assertEqual(resolved["facts"].get("units"), 4)
        self.assertEqual(resolved["facts"].get("unit_count"), 4)
        self.assertEqual(resolved["facts"].get("use_code"), "101")

    def test_dead_facts_snapshot(self):
        # Alias-Schreibweisen laufen ueber test_aliases_normalize und
        # zaehlen hier nicht als tot (units steht nie im Regeltext,
        # wird aber von der Engine auf unit_count normalisiert).
        register_universe = set(ENTRIES) | set(GAP_FACTS) | set(SUPPLIED)
        dead = sorted(register_universe - ALL_RULE_FACTS - set(ALIAS_MEMBERS))
        self.assertEqual(dead, sorted(ALLOWED_DEAD))
        unused_alias = sorted(set(ALIAS_MEMBERS) - ALL_RULE_FACTS)
        self.assertEqual(unused_alias, sorted(ALLOWED_UNUSED_ALIAS_INPUTS))

    def test_year_built_is_inert(self):
        # Nur tote Parzell-Fakten: units/unit_count sind lebendige
        # coverage-Fakten (z.B. D036) und wuerden Entscheidungen zu Recht aendern.
        parcel = {"year_built": 1960, "use_code": "101",
                  "use_description": "x", "county": "Los Angeles",
                  "supplied_state": "CA"}
        for rule in RULES:
            with self.subTest(rule=rule["team_rule_id"]):
                base = jurisdiction_base(rule)
                before = engine.evaluate_rule(rule, dict(base))
                after = engine.evaluate_rule(rule, {**base, **parcel})
                self.assertEqual((after["result"], after["missing_facts"]),
                                 (before["result"], before["missing_facts"]))

    def test_occupancy_rules_need_occupancy_date(self):
        occupancy_rules = [r for r in RULES
                           if any("ccupancy" in f for f in collect_rule_facts(r))]
        self.assertGreaterEqual(len(occupancy_rules), 10)
        for rule in occupancy_rules:
            with self.subTest(rule=rule["team_rule_id"]):
                facts = jurisdiction_base(rule)
                facts.update({"year_built": 1980, "units": 4, "unit_count": 4})
                result = engine.evaluate_rule(rule, facts)
                self.assertNotEqual(result["result"], "applies")


if __name__ == "__main__":
    unittest.main()
