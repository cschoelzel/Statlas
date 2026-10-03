import json, re, sys
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
tid = sys.argv[1]
gapfile = sys.argv[2]
patches = json.load(open(gapfile))
entry = next(x for x in patches if x.get("team_rule_id") == tid)
rules = json.load(open(ROOT / "data/rules.json"))
r = next(x for x in rules if x.get("team_rule_id") == tid)
doc = r.get("source_doc_id")
t = norm(Path(ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")).read_text(encoding="utf-8", errors="replace"))
q = norm(entry.get("evidence_quote"))
print("quote len norm:", len(q))
print("in text:", q in t)
# longest prefix present
for n in range(len(q), 0, -20):
    if q[:n] in t:
        print("longest prefix:", n, repr(entry.get("evidence_quote")[:120]))
        # find break
        print("break context:", repr(q[max(0,n-40):n+60]))
        break
