import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
def doctext(doc):
    p = ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")
    if not p.exists():
        return None
    return norm(p.read_text(encoding="utf-8", errors="replace"))
rules = json.load(open(ROOT / "data/rules.json"))
want = sys.argv[1:] or None
cache, bad, ok, missing = {}, [], 0, []
for r in rules:
    tid = r.get("team_rule_id")
    if want and tid not in want and r.get("source_doc_id") not in want:
        continue
    doc = r.get("source_doc_id")
    if doc not in cache:
        cache[doc] = doctext(doc)
    q = norm(r.get("quoted_span"))
    t = cache.get(doc)
    if t is None:
        missing.append((tid, doc)); continue
    if q and len(q) >= 40 and q[:60] in t and q[-60:] in t:
        ok += 1
    else:
        bad.append((tid, doc))
print("verified:", ok, "unverifiable:", len(bad) + len(missing))
for tid, doc in bad:
    print("QUOTE-FAIL", tid, doc)
for tid, doc in missing:
    print("NO-TEXT", tid, doc)
