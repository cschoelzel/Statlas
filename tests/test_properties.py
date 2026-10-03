"""Synthetic engine properties; these establish software behavior, not legal accuracy."""
import copy
import hashlib
import itertools
import json
import random
import unittest
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

from navigator.engine import evaluate_condition, evaluate_formula, evaluate_rule, evaluate_rules

SEED = 261003
REPORT = Path(__file__).resolve().parents[1] / 'reports/property_checks.json'


def oracle(tree, facts):
    if isinstance(tree, bool):
        return tree, set()
    if 'fact' in tree:
        name = tree['fact']
        value = facts.get(name)
        if value is None or value in ('declined', 'refused', 'unknown', ''):
            return None, {name}
        return value == tree['value'], set()
    if 'not' in tree:
        result, missing = oracle(tree['not'], facts)
        return (None if result is None else not result), missing
    operator = next(iter(tree))
    children = [oracle(c, facts) for c in tree[operator]]
    # Resolve uncertainty by all Boolean completions, rather than engine reducers.
    possibilities = set()
    for completion in itertools.product(*[(False, True) if v is None else (v,) for v, _ in children]):
        possibilities.add(all(completion) if operator == 'all' else any(completion))
    if len(possibilities) == 1:
        return possibilities.pop(), set()
    return None, set().union(*(missing for _, missing in children))


def sample_tree(rng, depth=0):
    if depth >= 3 or rng.random() < .35:
        return {'fact': 'f' + str(rng.randrange(8)), 'value': bool(rng.randrange(2))}
    operator = rng.choice(('all', 'any', 'not'))
    if operator == 'not':
        return {'not': sample_tree(rng, depth + 1)}
    return {operator: [sample_tree(rng, depth + 1) for _ in range(rng.randrange(2, 4))]}


def fixture(**updates):
    result = {'team_rule_id': 'synthetic', 'source_doc_id': 'synthetic-test-only',
              'jurisdiction': 'CA', 'level': 'state', 'status': 'in_force',
              'logic': {'coverage': True, 'exemptions': False}}
    result.update(updates)
    return result


class PropertyTests(unittest.TestCase):
    def test_independent_properties(self):
        rng = random.Random(SEED)
        fingerprints = set()
        families = {'nested_truth_unique': 0, 'irrelevant_fact': 0, 'child_order': 0,
                    'numeric_boundary': 0, 'date_boundary': 0, 'decimal_formula': 0,
                    'unit_rejection': 0, 'question_scenarios_unique': 0,
                    'synthetic_portfolio_repeat': 0}
        while len(fingerprints) < 20000:
            expr = sample_tree(rng)
            facts = {f'f{i}': rng.choice((True, False, None)) for i in range(8)}
            encoded = json.dumps([expr, facts], sort_keys=True, separators=(',', ':'))
            if encoded in fingerprints:
                continue
            fingerprints.add(encoded)
            expected = oracle(expr, facts)
            self.assertEqual(evaluate_condition(expr, facts), expected, encoded)
            families['nested_truth_unique'] += 1
            self.assertEqual(evaluate_condition(expr, {**facts, 'unreferenced': 194}), expected)
            families['irrelevant_fact'] += 1
            if 'all' in expr or 'any' in expr:
                op = next(iter(expr))
                self.assertEqual(evaluate_condition({op: list(reversed(expr[op]))}, facts), expected)
                families['child_order'] += 1
        operations = {'lt': lambda a,b: a < b, 'lte': lambda a,b: a <= b,
                      'gt': lambda a,b: a > b, 'gte': lambda a,b: a >= b,
                      'eq': lambda a,b: a == b, 'ne': lambda a,b: a != b}
        for threshold in range(100):
            for offset in (-1, 0, 1):
                for op, function in operations.items():
                    expr = {'fact': 'units', 'op': op, 'value': threshold}
                    self.assertEqual(evaluate_condition(expr, {'units': threshold+offset})[0], function(threshold+offset, threshold))
                    families['numeric_boundary'] += 1
            day = date(2026, 1, 1) + timedelta(days=threshold)
            for offset in (-1, 0, 1):
                actual = day + timedelta(days=offset)
                for op in ('lt', 'lte', 'gt', 'gte', 'eq'):
                    expr = {'fact': 'co', 'op': op, 'value': day.isoformat(), 'type': 'date'}
                    self.assertEqual(evaluate_condition(expr, {'co': actual.isoformat()})[0], operations[op](actual, day))
                    families['date_boundary'] += 1
            a, b = Decimal(threshold)/Decimal(10), Decimal('0.2')
            expr = {'op': 'add', 'args': [{'value': str(a)}, {'value': str(b)}]}
            self.assertEqual(Decimal(evaluate_formula(expr, {})['value']), a+b)
            families['decimal_formula'] += 1
            expr = {'op': 'add', 'args': [{'value': str(a), 'unit': 'USD'}, {'value': str(b), 'unit': 'percent'}]}
            self.assertIsNotNone(evaluate_formula(expr, {})['error'])
            families['unit_rejection'] += 1
        # 100 unique thresholds test refusal, decisive branches and recalculation.
        for threshold in range(100):
            rule = fixture(logic={'coverage': {'fact': 'units', 'op': 'gt', 'value': threshold},
                                  'exemptions': {'fact': 'owner_occupied', 'value': True}})
            initial = evaluate_rule(rule, {'state': 'CA'})
            self.assertEqual(set(initial['missing_facts']), {'unit_count', 'owner_occupied'})
            self.assertEqual({q['fact'] for q in initial['targeted_questions']}, {'unit_count', 'owner_occupied'})
            self.assertTrue(all(q['may_decline'] and q['source_doc_id'] == 'synthetic-test-only' for q in initial['targeted_questions']))
            self.assertEqual(evaluate_rule(rule, {'state': 'CA', 'units': 'declined'})['result'], 'unknown')
            irrelevant = evaluate_rule(rule, {'state': 'CA', 'units': threshold})
            self.assertEqual(irrelevant['result'], 'does_not_apply')
            self.assertEqual(irrelevant['targeted_questions'], [])
            resolved = evaluate_rule(rule, {'state': 'CA', 'units': threshold+1, 'owner_occupied': False})
            self.assertEqual(resolved['result'], 'applies')
            exempt = evaluate_rule(rule, {'state': 'CA', 'units': threshold+1, 'owner_occupied': True})
            self.assertEqual(exempt['result'], 'does_not_apply')
            families['question_scenarios_unique'] += 1
        portfolio = [fixture(team_rule_id=f'synthetic-{i}', logic={'coverage': {'fact': 'units', 'op': 'gt', 'value': i}, 'exemptions': False}) for i in range(100)]
        baseline = evaluate_rules(portfolio, {'state': 'CA', 'units': 50})
        for _ in range(100):
            self.assertEqual(evaluate_rules(portfolio, {'state': 'CA', 'units': 50}), baseline)
            families['synthetic_portfolio_repeat'] += 1
        # Curated critical changes must produce an observable counterexample.
        mutations = {}
        base = fixture(logic={'coverage': {'fact': 'units', 'op': 'gt', 'value': 2}, 'exemptions': {'fact': 'owner_occupied', 'value': True}})
        mutated = copy.deepcopy(base); mutated['logic']['coverage']['op'] = 'lt'
        mutations['reverse_comparison'] = evaluate_rule(base, {'state': 'CA','units':3,'owner_occupied':False})['result'] != evaluate_rule(mutated, {'state': 'CA','units':3,'owner_occupied':False})['result']
        mutated = copy.deepcopy(base); mutated['logic']['exemptions'] = False
        mutations['remove_exemption'] = evaluate_rule(base, {'state':'CA','units':3,'owner_occupied':True})['result'] != evaluate_rule(mutated, {'state':'CA','units':3,'owner_occupied':True})['result']
        base = fixture(effective_date='2026-10-01'); mutated = fixture(effective_date='2026-10-02')
        mutations['shift_effective_date'] = evaluate_rule(base, {'state':'CA'})['result'] != evaluate_rule(mutated, {'state':'CA'})['result']
        mutations['and_to_or'] = evaluate_condition({'all':[True,False]}, {}) != evaluate_condition({'any':[True,False]}, {})
        self.assertTrue(all(mutations.values()))
        digest = hashlib.sha256('\n'.join(sorted(fingerprints)).encode()).hexdigest()
        REPORT.parent.mkdir(exist_ok=True)
        REPORT.write_text(json.dumps({'status':'passed','seed':SEED,'families':families,
            'unique_nested_input_sha256':digest,'oracle':'Independent Boolean completion oracle with relevant missing-fact propagation',
            'mutations_detected':mutations,'limitations':['Synthetic software checks are not legal gold labels.',
            'Portfolio repetitions use 100 synthetic rules, not extracted-source portfolio.',
            'Source-id integrity must be independently validated against source manifest.'],
            'question_assertions_per_scenario':9}, indent=2)+'\n')


if __name__ == '__main__':
    unittest.main()
