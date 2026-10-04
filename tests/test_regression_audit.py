import json
import unittest
from pathlib import Path
from navigator.engine import evaluate_rule
ROOT = Path(__file__).resolve().parents[1]
class TestAuditRegression(unittest.TestCase):
    def test_pending_empty_facts_is_unknown(self):
        r = {'team_rule_id': 't1', 'jurisdiction': 'CA', 'level': 'state', 'status': 'pending', 'logic': {'coverage': True, 'exemptions': False}}
        self.assertEqual(evaluate_rule(r, {}, '2026-10-01')['result'], 'unknown')
    def test_ended_beats_pending(self):
        r = {'team_rule_id': 't2', 'jurisdiction': 'CA', 'level': 'state', 'status': 'pending', 'end_date': '2020-01-01', 'logic': {'coverage': True, 'exemptions': False}}
        self.assertIsNone(evaluate_rule(r, {'state': 'CA'}, '2026-10-01')['result'])
    def test_no_boolean_coverage_in_rules(self):
        rules = json.loads((ROOT / 'data' / 'rules.json').read_text())
        bad = [x.get('team_rule_id') for x in rules if isinstance(x.get('logic'), dict) and x['logic'].get('coverage') is True]
        self.assertEqual(bad, [])
    def test_d022_unverified_commencement_blocks_applies(self):
        from navigator.engine import evaluate_rule
        rules = json.loads((ROOT / 'data/rules.json').read_text())
        rule = next(r for r in rules if r['team_rule_id'] == 'D022-r001')
        facts = {'state': 'CA', 'algorithm_used_as_part_of_contract_combination_or_conspiracy': True}
        for date in ('2025-12-31', '2026-01-02'):
            decision = evaluate_rule(rule, facts, date)
            self.assertEqual(decision['result'], 'unknown')
            self.assertEqual(decision['targeted_questions'], [])
            self.assertTrue(decision['review_required'])

    def test_negative_change_requires_recorded_failed_measure(self):
        from navigator.changes import evaluate_changes
        case = {'test_id': 'T5', 'title': 'Failed rent-control ballot',
                'type': 'negative', 'rule_ids': ['MA-RENT-P1'], 'as_of': '2026-10-01'}
        result = evaluate_changes([], [], [case])['T5']
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['missing_rule_ids'], ['MA-RENT-P1'])
        self.assertNotIn('gescheitert/ohne Rechtswirkung', result['notes'])
        failed = {'team_rule_id': 'MA-RENT-P1', 'jurisdiction': 'MA',
                  'level': 'state', 'status': 'failed',
                  'logic': {'coverage': {'fact': 'state', 'op': 'eq', 'value': 'MA'}}}
        from unittest.mock import patch
        with patch('navigator.changes.resolve_address', return_value={'status': 'matched', 'facts': {'state': 'MA'}}):
            result = evaluate_changes([failed], [{'address_id': 'ma-test'}], [case])['T5']
        self.assertEqual(result['status'], 'correctly_empty')
        self.assertEqual(result['missing_rule_ids'], [])
        self.assertEqual(result['affected_address_ids'], [])
        failed['status'] = 'pending'
        result = evaluate_changes([failed], [], [case])['T5']
        self.assertNotEqual(result['status'], 'correctly_empty')
    def test_changes_unresolved_never_affected(self):
        from navigator.changes import evaluate_changes
        from navigator.geography import load_addresses
        rules = json.loads((ROOT / 'data' / 'rules.json').read_text())
        got = evaluate_changes(rules, load_addresses())
        for tid, case in got.items():
            overlap = set(case['affected_address_ids']) & set(case['unresolved_address_ids'])
            self.assertEqual(overlap, set(), tid)
if __name__ == '__main__':
    unittest.main()
