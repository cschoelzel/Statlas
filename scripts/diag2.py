import json
rules = json.load(open('data/rules.json'))
by = {r.get('team_rule_id'): r for r in rules}
for tid in ('D069-r001', 'D007-r005', 'D007-r009', 'D007-r010', 'D041-r002',
            'D041-r003', 'D052-r002', 'D041-r005', 'D042-r002', 'D001-r001',
            'D017-r001'):
    r = by.get(tid)
    if not r:
        print(tid, 'MISSING'); continue
    print(tid, '|', r.get('status'), '| eff', r.get('effective_date'),
          '| end', r.get('end_date'), '| op', r.get('operative_date'),
          '| src', r.get('source_doc_id'), '| title', (r.get('title') or '')[:60])
print('total', len(rules))
