"""Independent synthetic regressions; these are not legal gold cases."""
import unittest
from itertools import product
from navigator.engine import evaluate_condition, evaluate_rule, evaluate_rules


def rule(**extra):
    return {"team_rule_id":"r", "jurisdiction":"CA", "level":"state", "status":"in_force",
            "logic":{"coverage":True,"exemptions":False}, **extra}


class IndependentRedteam(unittest.TestCase):
    def test_truth_tables(self):
        for op, values in product(('all','any'), product((True, False, None), repeat=2)):
            children=[v if v is not None else {'fact':'absent','value':True} for v in values]
            if op=='all': expected=False if False in values else None if None in values else True
            else: expected=True if True in values else None if None in values else False
            actual, missing=evaluate_condition({op:children}, {})
            self.assertIs(actual, expected)
            self.assertEqual(missing, {'absent'} if expected is None else set())

    def test_missing_translation_is_unknown(self):
        r=rule(); del r['logic']
        self.assertEqual(evaluate_rule(r, {'state':'CA'})['result'], 'unknown')

    def test_unrecognized_status_is_not_operative(self):
        self.assertNotEqual(evaluate_rule(rule(status='withdrawn'), {'state':'CA'})['result'], 'applies')

    def test_operative_date(self):
        self.assertEqual(evaluate_rule(rule(operative_date='2027-01-01'), {'state':'CA'})['result'], 'not_yet_effective')

    def test_conflicting_effective_date(self):
        self.assertEqual(evaluate_rule(rule(effective_date='2027-01-01', effective_date_candidates=['2025-01-01','2027-01-01']), {'state':'CA'})['result'], 'unknown')

    def test_interaction_order_invariance(self):
        a=rule(team_rule_id='a', interactions=[{'target':'b','type':'supersedes','evidence':'Section A'}])
        b=rule(team_rule_id='b', interactions=[{'target':'c','type':'supersedes','evidence':'Section B'}])
        c=rule(team_rule_id='c')
        results=lambda rs: {x['team_rule_id']:x['result'] for x in evaluate_rules(rs, {'state':'CA'})}
        self.assertEqual(results([a,b,c]), results([b,a,c]))
