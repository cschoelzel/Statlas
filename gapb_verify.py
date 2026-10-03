import json
d = json.load(open('/tmp/gapfix_B.json'))
canon = set(x[2:] for x in open('gapb_canon.py').read().split() if x.startswith('F:'))
import subprocess
canon = set(subprocess.run(['python3','gapb_canon.py'],capture_output=True,text=True).stdout.split('F:')[1:])
canon = set(x.split()[0] for x in canon)
bad = []
for r in d:
    q = r.get('evidence_quote','')
    if len(q) > 300: bad.append((r['team_rule_id'],'quote>300'))
    rep = r.get('replacement')
    if rep and rep.get('fact') not in canon: bad.append((r['team_rule_id'],'factnichtkanonisch:'+str(rep.get('fact'))))
    if r['status'] not in ('resolved','open'): bad.append((r['team_rule_id'],'status'))
print('rows',len(d),'bad',bad)
