import json, re
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
for c in json.load(open("/tmp/candidates.json")):
    t = norm(Path(ROOT / ("participant-final-no-hour16 3/corpus/text/" + c["doc"] + ".txt")).read_text(encoding="utf-8", errors="replace"))
    q = norm(c["quote"])
    print(c["doc"], "len:", len(q), "verbatim:", q in t, "|", c["quote"][:70])
