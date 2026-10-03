import json
rules = json.load(open('data/rules.json'))
for r in rules:
    sid = r.get('source_doc_id','')
    if sid in ('D040','D041','D042','D043'):
        logic = json.dumps(r.get('logic', {}))
        if 'unresolved' in logic:
            print('### ' + str(r.get('team_rule_id')))
            print('COV: ' + json.dumps(r['logic'].get('coverage')))
            print('EX: ' + json.dumps(r['logic'].get('exemptions')))
            print('REQ: ' + str(r.get('requirement',''))[:500])
            print('QS: ' + str(r.get('quoted_span',''))[:300])
            print('')
