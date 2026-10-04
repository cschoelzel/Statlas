"""P7-Regression: D084-r001 (Santa Ana Rent Increase Cap) liefert mit vollen
Objektfakten `applies` inkl. Beleg-Quartett; ohne Objektfakten ehrlich `unknown`.
Sichert ab, dass 0 applies im 500er-Export Design (fail-closed) ist, kein Bug."""
import json
import os
import unittest

from navigator.engine import evaluate_rule

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FULL_FACTS = {
    "state": "CA",
    "legal_city": "Santa Ana",
    "rent_increase_planned": True,
    "lease_renewal_or_increase_date": "2026-10-01",
    "cpi_percent": 3.0,
}


def load_rule():
    with open(os.path.join(BASE, "data", "rules.json"), encoding="utf-8") as f:
        rules = json.load(f)
    for r in rules:
        if r.get("team_rule_id") == "D084-r001":
            return r
    raise AssertionError("D084-r001 fehlt in data/rules.json")


class AppliesD084(unittest.TestCase):
    def test_applies_mit_vollen_fakten(self):
        res = evaluate_rule(load_rule(), dict(FULL_FACTS))
        self.assertEqual(res["result"], "applies")
        self.assertEqual(res.get("missing_facts"), [])
        comp = res.get("computed_value") or {}
        self.assertAlmostEqual(float(comp.get("value")), 2.40, places=2)
        ev = res.get("evidence") or {}
        for field in ("citation", "quoted_span", "source_url", "retrieved_at"):
            self.assertTrue(ev.get(field), "Belegfeld fehlt: %s" % field)

    def test_zitat_steht_im_korpus(self):
        res = evaluate_rule(load_rule(), dict(FULL_FACTS))
        span = res["evidence"]["quoted_span"]
        corpus = os.path.join(BASE, "participant-final-no-hour16 3", "corpus", "text", "D084.txt")
        with open(corpus, encoding="utf-8") as f:
            text = f.read()
        norm = lambda s: " ".join(s.split())
        self.assertIn(norm(span), norm(text))

    def test_unknown_ohne_objektfakten(self):
        res = evaluate_rule(load_rule(), {"state": "CA", "legal_city": "Santa Ana"})
        self.assertEqual(res["result"], "unknown")
        self.assertTrue(res.get("missing_facts"))


if __name__ == "__main__":
    unittest.main()
