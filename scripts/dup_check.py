import json, sys
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
rules = {r.get("team_rule_id"): r for r in json.load(open(ROOT / "data/rules.json"))}
def leaves(x):
    out = []
    def walk(n):
        if isinstance(n, dict):
            if set(n.keys()) == {"fact", "op", "value"}:
                out.append(n)
            else:
                for v in n.values():
                    walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)
    walk(x.get("logic", {}))
    return out
for gf, tids in [(sys.argv[1], sys.argv[2:])]:
    todo = json.load(open(gf))
    for tid in tids:
        e = next(x for x in todo if x.get("team_rule_id") == tid)
        r = rules.get(tid)
        print("=" * 70)
        print(tid, "|", (r.get("title") or "")[:90] if r else "RULE-MISSING")
        print("gap:", e.get("gap_fact"))
        print("replacement:", json.dumps(e.get("replacement")))
        if r is None:
            continue
        ls = leaves(r)
        print("rule leaves now:", json.dumps(ls)[:600])
        dup = any(l == e.get("replacement") for l in ls)
        print("replacement-duplicates-sibling:", dup)
