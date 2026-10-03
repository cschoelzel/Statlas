import json
rules = json.load(open('data/rules.json'))
canon = set()
def walk(n):
    import collections
    if isinstance(n, dict):
        f = n.get('fact')
        if f and not str(f).startswith('unresolved'):
            canon.add(str(f))
        for v in n.values():
            walk(v)
    elif isinstance(n, list):
        for v in n:
            walk(v)
for r in rules:
    walk(r.get('logic', {}))
print('CANON_COUNT', len(canon))
for f in sorted(canon):
    print('F:' + f)
