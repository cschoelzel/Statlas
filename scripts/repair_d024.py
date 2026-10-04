"""Repair D024 rejected rules.

Systematic model error: logic used wrong keys (formula / exemption singular /
requirement / remedial_provision instead of the required coverage+exemptions
pair). This script rebuilds valid logic DSL from the model's own conditions
and re-validates via navigator.extract.validate. No re-extraction, no combine.
"""
import json
import sys

sys.path.insert(0, '.')
from navigator.extract import validate
from navigator.sources import ROOT

EXEMPT_ANY = {'any': [
    {'fact': 'affordable_housing_restricted', 'op': 'eq', 'value': True},
    {'fact': 'institutional_dormitory', 'op': 'eq', 'value': True},
    {'fact': 'subject_to_stricter_local_rent_control', 'op': 'eq', 'value': True},
    {'fact': 'certificate_of_occupancy_within_15_years', 'op': 'eq', 'value': True},
    {'fact': 'single_family_noncorporate_owner', 'op': 'eq', 'value': True},
    {'fact': 'owner_occupied_two_unit', 'op': 'eq', 'value': True},
    {'fact': 'is_mobilehome_homeowner', 'op': 'eq', 'value': True},
]}
STATE_CA = {'fact': 'state', 'op': 'eq', 'value': 'CA'}
RES = {'fact': 'is_residential_property', 'op': 'eq', 'value': True}
JUNK_KEYS = (
    'exemption_from_cap',
    'total_rent_must_not_exceed',
    'calculation_methodology',
    'requirement',
    'remedial_provision',
)
VOLATILE_KEYS = (
    'team_rule_id', 'source_doc_id', 'source_url', 'retrieved_at',
    'query_date', 'review_status', 'evidence', 'evidence_gaps',
    'quote_alignment', 'temporal_conflict',
)


def fix_span(span):
    if isinstance(span, str):
        return span.replace(chr(92) + 'n', ' ').replace(chr(10), ' ')
    return span


QUOTE_SLICES = {
    7: ('Housing subject to rent or price control',
        'provided in subdivision (a).'),
    9: ('Residential real property that is alienable separate',
        'The owner is not any of the following:'),
    10: ('two separate dwelling units within a single',
        'neither unit is an accessory dwelling unit or a '
        'junior accessory dwelling unit.'),
    12: ('The tenants have been provided written notice',
        'Sections 1947.12 (d)(5) and 1946.2 (e)(8) of the Civil Code'),
}
QUOTE_TRUNCATE = {13: 420, 14: 369}


def slice_quote(text, start_anchor, end_anchor):
    start = text.find(start_anchor)
    if start < 0:
        return None
    end = text.find(end_anchor, start)
    if end < 0:
        return None
    return text[start:end + len(end_anchor)]


def truncate_quote(quote, limit):
    import re
    flat = re.sub(r'\s+', ' ', quote)
    cut = flat[:limit]
    space = cut.rfind(' ')
    return cut[:space] if space > 20 else cut


TITLE_ORDINAL = {
    'Exemption - Existing Local Rent Control': 8,
    'Exemption - Single-Family Rentals (Non-Corporate)': 10,
    'Exemption - Owner-Occupied Two-Unit Property': 11,
    'Rent Cap - Single-Family Exemption Notice Requirement': 13,
    'Transitional Provisions - Pre-April 1 2024 Increases': 14,
    'Transitional Provisions - Mobilehome Pre-Feb 18 2021 Increases': 15,
}


def strip_unresolved(expr):
    if isinstance(expr, dict) and len(expr) == 1:
        key = next(iter(expr))
        if key in ('all', 'any'):
            kept = []
            for item in expr[key]:
                if (isinstance(item, dict) and set(item) == {'fact', 'op', 'value'}
                        and str(item.get('fact', '')).startswith(
                            'unresolved_legal_evidence_')):
                    continue
                kept.append(strip_unresolved(item))
            return {key: kept}
        if key == 'not':
            return {'not': strip_unresolved(expr['not'])}
    return expr


def repair(index, rule):
    rule = {k: v for k, v in rule.items() if k not in VOLATILE_KEYS}
    logic = rule.get('logic', {}) or {}
    for key in JUNK_KEYS:
        logic.pop(key, None)
    if 'coverage' in logic:
        logic['coverage'] = strip_unresolved(logic['coverage'])
    rule['quoted_span'] = fix_span(rule.get('quoted_span', ''))
    for item in rule.get('field_evidence') or []:
        if isinstance(item, dict):
            item['quoted_span'] = fix_span(item.get('quoted_span', ''))
    if index in (0, 1, 3, 4):
        logic['exemptions'] = EXEMPT_ANY
    elif index in (2, 12, 13, 14):
        if index == 12 and 'coverage' in logic:
            extra = [STATE_CA] + logic['coverage'].get('all', [])
            logic['coverage'] = {'all': extra}
        logic['exemptions'] = False
    elif 5 <= index <= 11:
        exempt = logic.pop('exemption', None)
        logic['coverage'] = {'all': [STATE_CA, RES]}
        logic['exemptions'] = exempt
    rule['logic'] = logic
    return rule


def main():
    index = json.loads((ROOT / 'data/sources/index.json').read_text())
    source = next(e for e in index if e['doc_id'] == 'D024')
    text = (ROOT / source['text_file']).read_text()
    path = ROOT / 'data/extraction/D024.json'
    artifact = json.loads(path.read_text())
    # Pristine source: raw model response holds all 15 rules with logic_json /
    # evidence_json strings (the artifact's rejected entries were mangled by
    # an earlier misrouted repair pass, so rebuild from the response file).
    response = json.loads(
        (ROOT / 'data/extraction/D024.response.json').read_text())
    raw = ''.join(part.get('text', '') for part in response.get('content', []))
    result = json.loads(raw)
    pool = []
    for ordinal, rule in enumerate(result.get('rules', []), 1):
        try:
            rule['logic'] = json.loads(rule.pop('logic_json'))
            rule['field_evidence'] = json.loads(rule.pop('evidence_json'))
        except (ValueError, KeyError):
            rule['logic'] = {}
        pool.append((ordinal, rule))
    accepted = []
    rejected = []
    for ordinal, original in pool:
        pos = ordinal - 1
        rule = repair(pos, original)
        if pos in QUOTE_SLICES:
            fixed = slice_quote(text, *QUOTE_SLICES[pos])
            if fixed is None:
                rejected.append({'rule': rule,
                                 'errors': ['quote anchors not found']})
                print('FAIL D024-r%03d %s: quote anchors not found'
                      % (ordinal, rule.get('title')))
                continue
            rule['quoted_span'] = fixed
        elif pos in QUOTE_TRUNCATE:
            rule['quoted_span'] = truncate_quote(
                rule.get('quoted_span', ''), QUOTE_TRUNCATE[pos])
        valid, errors = validate(rule, source, text, ordinal)
        if errors:
            rejected.append({'rule': rule, 'errors': errors})
            print('FAIL D024-r%03d %s: %s'
                  % (ordinal, rule.get('title'), errors))
        else:
            accepted.append(valid)
            print('OK   %s %s' % (valid['team_rule_id'], valid['title']))
    artifact['rules'] = accepted
    artifact['rejected'] = rejected
    artifact['status'] = 'needs_review'
    path.write_text(json.dumps(artifact, indent=2) + chr(10))
    print('saved: %d accepted, %d still rejected' % (len(accepted), len(rejected)))


if __name__ == '__main__':
    main()
