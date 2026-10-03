import json, re
from pathlib import Path
from collections import Counter
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
rules = json.load(open(ROOT / "data/rules.json"))
def gaps(r):
    out = []
    def walk(x):
        if isinstance(x, dict):
            if set(x.keys()) == {"fact", "op", "value"} and isinstance(x.get("fact"), str) and x["fact"].startswith("unresolved"):
                out.append(x["fact"])
            else:
                for v in x.values():
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(r.get("logic", {}))
    return out
total = 0
bydoc = Counter()
for r in rules:
    g = gaps(r)
    total += len(g)
    for x in g:
        bydoc[r.get("source_doc_id")] += 1
print("rules:", len(rules), "gap leaves:", total)
print("by doc:", dict(sorted(bydoc.items())))
print("D025 ids:", sorted(x.get("team_rule_id") for x in rules if x.get("source_doc_id") == "D025"))
