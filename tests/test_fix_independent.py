"""Independent synthetic interpreter tests, not legal gold labels."""
import itertools
import unittest
from navigator.engine import evaluate_condition, evaluate_rule, evaluate_rules, evaluate_formula


def rule(**extra):
    return {"team_rule_id": "base", "jurisdiction": "CA", "level": "state", "status": "in_force", "logic": {"coverage": True, "exemptions": False}, **extra}


class FixIndependent(unittest.TestCase):
    def test_three_value_nested(self):
        for a, b, c in itertools.product((True, False, None), repeat=3):
            child=lambda v: v if v is not None else {"fact": "missing", "value": True}
            left=False if False in (a,b) else None if None in (a,b) else True
            expected=True if True in (left,c) else None if None in (left,c) else False
            actual, missing=evaluate_condition({"any": [{"all": [child(a),child(b)]},child(c)]}, {})
            self.assertIs(actual, expected)
            self.assertEqual(missing, {"missing"} if expected is None else set())

    def test_missing_translation_and_malformed_logic(self):
        for logic in ("prose", [], {"coverage": "untranslated", "exemptions": False}):
            self.assertEqual(evaluate_rule(rule(logic=logic), {"state": "CA"})["result"], "unknown")

    def test_date_precision(self):
        expr={"fact": "date", "op": "lt", "type": "date", "value": "2026-10-01"}
        self.assertIs(evaluate_condition(expr, {"date": "2026-09"})[0], True)
        self.assertIs(evaluate_condition(expr, {"date": "2026"})[0], None)

    def test_operative_ambiguity_conservative(self):
        r=rule(effective_date="2025-01-01", operative_date="2027-01-01")
        self.assertEqual(evaluate_rule(r, {"state": "CA"})["result"], "unknown")
        self.assertTrue(evaluate_rule(r, {"state": "CA"})["review_required"])

    def test_formula_extreme_and_malformed(self):
        for expr in ({"value": "Infinity"}, {"value": "1e101"}, {"op": "add", "args": None}):
            self.assertIsNotNone(evaluate_formula(expr, {})["error"])

    def test_supersession_order(self):
        a=rule(team_rule_id="a", interactions=[{"target":"b","type":"supersedes","evidence":"synthetic A"}])
        b=rule(team_rule_id="b")
        expected={"a":"applies", "b":"superseded"}
        for ordering in ([a,b],[b,a]):
            self.assertEqual({x["team_rule_id"]:x["result"] for x in evaluate_rules(ordering,{"state":"CA"})}, expected)

    def test_ambiguous_condition_fails_closed(self):
        self.assertIsNone(evaluate_condition({"all": [], "any": [False]}, {})[0])

    def test_exact_date_not_equal(self):
        self.assertIs(evaluate_condition({"fact":"date","type":"date","op":"ne","value":"2026-10-01"},{"date":"2026-10-02"})[0], True)

    def test_supersession_cycle_requires_review(self):
        a=rule(team_rule_id="a", interactions=[{"target":"b","type":"supersedes","evidence":"synthetic A"}])
        b=rule(team_rule_id="b", interactions=[{"target":"a","type":"supersedes","evidence":"synthetic B"}])
        results=evaluate_rules([a,b], {"state":"CA"})
        self.assertFalse(all(x["result"] == "superseded" for x in results))
        self.assertTrue(all(x["conflict_flag"] or x["review_required"] for x in results))

if __name__ == "__main__":
    unittest.main()
