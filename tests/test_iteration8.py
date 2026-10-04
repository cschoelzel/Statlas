"""Iteration 8: Regressionstests aus unabhaengigem 10/10-Audit (P7-B3, P8-B1, P10-B1)."""
import json

import pytest

from navigator.changes import evaluate_changes
from navigator.engine import evaluate_rule


def _rule(rule_id):
    rules = json.load(open("data/rules.json"))
    return [r for r in rules if r.get("team_rule_id") == rule_id][0]


def test_applies_path_carries_evidence_quartet():
    # P7-B3: Positivpfad mit echten Fakten (kein Mock-Zitat) belegt das Beleg-Quartett.
    rule = _rule("D084-r001")
    facts = {"state": "CA", "legal_city": "Santa Ana", "rent_increase_planned": True,
             "lease_renewal_or_increase_date": "2026-10-01", "cpi_percent": 3.0}
    d = evaluate_rule(rule, facts, "2026-10-01")
    assert d["result"] == "applies", d
    assert float(d["computed_value"]["value"]) == pytest.approx(2.4)
    ev = d["evidence"]
    for key in ("citation", "quoted_span", "source_url", "retrieved_at"):
        assert ev.get(key), key


def test_exemption_exclusion_differs_from_coverage_exclusion():
    # P8-B1: Ausnahme-ausgeschlossen vs. Regel-ausgeschlossen sind unterscheidbar.
    rule = _rule("D084-r001")
    base = {"state": "CA", "legal_city": "Santa Ana", "rent_increase_planned": True,
            "lease_renewal_or_increase_date": "2026-10-01", "cpi_percent": 3.0}
    assert evaluate_rule(rule, base, "2026-10-01")["result"] == "applies"
    d = evaluate_rule(rule, dict(base, rent_increase_planned=False), "2026-10-01")
    assert d["result"] == "does_not_apply"
    assert "exemption" not in d["explanation"].lower()
    exempt_rule = json.loads(json.dumps(rule))
    exempt_rule["logic"] = {"coverage": rule["logic"]["coverage"],
                            "exemptions": {"all": [{"fact": "condominium", "op": "eq", "value": True}]}}
    d2 = evaluate_rule(exempt_rule, dict(base, condominium=True), "2026-10-01")
    assert d2["result"] == "does_not_apply"
    assert "exemption" in d2["explanation"].lower()
    assert d["explanation"] != d2["explanation"]


def test_changes_rejects_id_schema_with_hint():
    # P10-B1: Adressen ohne address_id geben ValueError mit Hinweis statt KeyError.
    rules = json.load(open("data/rules.json"))
    tests = json.load(open("participant-final-no-hour16 3/dev/change_tests.json"))
    addrs = json.load(open("addresses.json"))
    assert "address_id" not in addrs[0]
    with pytest.raises(ValueError, match="address_id"):
        evaluate_changes(rules, addrs, tests)
