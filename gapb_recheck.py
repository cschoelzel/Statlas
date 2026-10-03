import json
d = json.load(open('/tmp/gapfix_B.json'))
rules = {r.get('team_rule_id'): r for r in json.load(open('data/rules.json'))}
mismatch = []
for row in d:
    r = rules.get(row['team_rule_id'])
    if r is None: mismatch.append((row['team_rule_id'],'regel-weg'))
    elif row['gap_fact'] not in json.dumps(r.get('logic',{})): mismatch.append((row['team_rule_id'],'gap-leaf-weg'))
print('mismatch',mismatch if mismatch else 'keine - alle 20 Gap-Leaves noch vorhanden')
