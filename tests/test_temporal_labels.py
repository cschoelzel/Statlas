"""Regression Iteration 4: dates take precedence over status labels (P3)."""
import json
import unittest
from datetime import date
from navigator.engine import _temporal_state

AS_OF = "2026-10-01"

def rules():
    data = json.load(open("data/rules.json"))
    return data if isinstance(data, list) else list(data.values())

class TemporalLabels(unittest.TestCase):
    def test_past_effective_never_not_yet_effective(self):
        q = date.fromisoformat(AS_OF)
        for r in rules():
            eff = r.get("effective_date") or r.get("operative_date")
            end = r.get("end_date")
            if eff and eff <= AS_OF and not (end and end < AS_OF):
                st = _temporal_state(r, q)
                self.assertNotEqual(st["terminal"], "not_yet_effective", r.get("team_rule_id"))

    def test_future_effective_is_not_yet_effective(self):
        q = date.fromisoformat(AS_OF)
        for r in rules():
            eff = r.get("effective_date") or r.get("operative_date")
            if eff and eff > AS_OF:
                st = _temporal_state(r, q)
                self.assertEqual(st["terminal"], "not_yet_effective", r.get("team_rule_id"))

    def test_ended_before_query(self):
        q = date.fromisoformat(AS_OF)
        for r in rules():
            end = r.get("end_date")
            if end and end < AS_OF:
                st = _temporal_state(r, q)
                self.assertEqual(st["terminal"], "ended", r.get("team_rule_id"))

    def test_no_stale_not_yet_effective_label(self):
        for r in rules():
            eff = r.get("effective_date") or r.get("operative_date")
            end = r.get("end_date")
            if r.get("status") == "not_yet_effective" and eff and eff <= AS_OF and not (end and end < AS_OF):
                self.fail("stale label: " + str(r.get("team_rule_id")))

if __name__ == "__main__":
    unittest.main()
