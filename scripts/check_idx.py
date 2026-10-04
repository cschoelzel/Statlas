import json
idx = json.load(open('data/sources/index.json'))
want = ('D045', 'D046', 'D047', 'D025', 'D027', 'D067')
for s in idx:
    if s.get('doc_id') in want:
        print(s.get('doc_id'), '|', s.get('status'), '|', s.get('text_file'))
