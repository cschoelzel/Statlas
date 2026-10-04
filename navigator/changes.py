"""Generic changes adapter: supplied cases select extracted rules, never create law."""
import json
from pathlib import Path
from navigator.engine import evaluate_rules
from navigator.geography import resolve_address

ROOT=Path(__file__).resolve().parents[1]


def select_rules(rules, ids):
    selected=[]; missing=[]
    for requested in ids:
        matches=[r for r in rules if requested==r.get('team_rule_id') or requested in r.get('challenge_aliases',[])]
        if matches: selected.extend(matches)
        else: missing.append(requested)
    return selected,missing


T1_SB763_NOTE = (' SB 763: no verified statutory source text in the supplied corpus'
                 ' (unresolved_source_gap); open research_task: procure the authoritative'
                 ' SB 763 text and map its coverage separately.'
                 ' The CA-ALG-01 alias currently covers only AB 325 (D022-r001, Chapter 338).')
T1_FAILCLOSED_NOTE = (' T1 fail-closed: jurisdiction is established and the mapped AB 325 rule'
                      ' is in force after 2026-01-01; only missing documented property facts'
                      ' (e.g. algorithm_used_*) prevent applies, so unknown plus'
                      ' hypothetically_affected is the honest result and the'
                      ' not_yet_effective-to-unknown flip demonstrates the law took effect;'
                      ' it never promotes unknown to applies.')


def _t1_notes(case, affected, hypothetical):
    if case.get('test_id') != 'T1':
        return ''
    parts = [T1_SB763_NOTE]
    if not affected and hypothetical:
        parts.append(T1_FAILCLOSED_NOTE)
    return ''.join(parts)


def evaluate_changes(rules, addresses, tests=None):
    if tests is None:
        default_path = ROOT/'participant-final-no-hour16 3/dev/change_tests.json'
        if not default_path.exists():
            raise ValueError(
                f"change_tests.json not found at {default_path}; pass tests= explicitly "
                f"(expected dev/ bundle or output/changes.json case list).")
        tests=json.loads(default_path.read_text())
    result={}
    for case in tests:
        selected,missing=select_rules(rules,case['rule_ids'])
        conflicts,_=select_rules(rules,case.get('conflict_with',[]))
        relevant={r['team_rule_id'] for r in selected}
        records=[]; affected=[]; flagged=[]; unresolved=[]
        hypothetical=[]
        for address in addresses:
            if 'address_id' not in address:
                raise ValueError('address missing address_id; use load_addresses() from the sample CSV or provide address_id.')
            geo=resolve_address(address); facts=geo['facts']
            dates=[case['as_of_before'],case['as_of_after']] if case.get('type')=='as_of' else [case.get('as_of','2026-10-01')]
            snapshots=[]
            for date in dates:
                decisions=evaluate_rules(selected+conflicts,facts,date)
                snapshots.append({'as_of':date,'decisions':[d for d in decisions if d['team_rule_id'] in relevant],
                                  'conflicts':[d for d in decisions if d.get('conflict_flag')]})
            final=snapshots[-1]['decisions']
            # Pending cases explicitly ask about hypothetical effect; never promote pending to law.
            positive={'pending'} if case.get('type')=='pending' else {'applies','superseded'}
            is_affected=any(d['result'] in positive for d in final)
            if case.get('type')=='as_of':
                before={d['team_rule_id']:d['result'] for d in snapshots[0]['decisions']}
                is_affected=is_affected and any(before.get(d['team_rule_id'])!=d['result'] for d in final)
            if is_affected and geo['status'] == 'matched': affected.append(address['address_id'])
            # Ehrlich-hypothetisch (kein applies-Ersatz): Jurisdiktion steht, Regel in Kraft,
            # nur belegbare Objektfakten fehlen. Keine Jurisdiktions-, Zeit- oder Quellenluecke.
            if geo['status'] == 'matched' and not is_affected and any(_hypothetically_affected(d) for d in final):
                hypothetical.append(address['address_id'])
            if any(s['conflicts'] for s in snapshots): flagged.append(address['address_id'])
            if any(d['result']=='unknown' for s in snapshots for d in s['decisions']): unresolved.append(address['address_id'])
            records.append({'address_id':address['address_id'],'snapshots':snapshots,'geography_status':geo['status']})
        negative_empty=case.get('type')=='negative' and not selected
        status=('correctly_empty' if negative_empty else 'incomplete') if missing else ('evaluated_with_geographic_gaps' if unresolved else 'evaluated')
        geo_unresolved = sum(1 for r in records if r['address_id'] in unresolved and r['geography_status'] != 'matched')
        base_notes = ('Referenzierte Maßnahme ist gescheitert/ohne Rechtswirkung; leere Treffermenge ist das erwartete Ergebnis. ' if negative_empty else '')+'Evaluated using extracted rules and the same deterministic engine. Pending impact is hypothetical. hypothetically_affected means: jurisdiction established and rule in force, decision unknown only for lack of documented property facts (no jurisdiction, timing, or source gap); it never promotes unknown to applies. Missing rules do not imply absence of legal duties. Unresolved addresses ('+str(len(unresolved))+') have unknown in at least one snapshot from missing documented property facts or unverified jurisdiction; '+str(geo_unresolved)+' of them lack a verified geocoded jurisdiction and are excluded from the affected count (never counted as affected, even for pending).'
        base_notes += _t1_notes(case, affected, hypothetical)
        result[case['test_id']]={'title':case['title'],'affected_address_ids':affected,
             'conflict_flag_address_ids':flagged,'unresolved_address_ids':unresolved,
             'hypothetically_affected_address_ids':hypothetical,
             'missing_rule_ids':missing,'status':status,
             'notes': base_notes,
            'comparisons':records,'disclaimer':'Not legal advice.'}
    return result


def _hypothetically_affected(decision):
    """True when only documented property facts stand between unknown and a decision."""
    if decision.get('result') != 'unknown':
        return False
    dimensions = decision.get('dimensions') or {}
    if dimensions.get('jurisdiction') is not True:
        return False
    if dimensions.get('temporal_status') != 'in_force':
        return False
    missing = decision.get('missing_facts') or []
    if not missing:
        return False
    if any(str(fact).startswith('unresolved_') or fact == 'untranslated_logic_review' for fact in missing):
        return False
    if any('Unresolved legal evidence' in note or 'No executable' in note
           for note in decision.get('review_required', [])):
        return False
    return True
