import re, sys
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
doc, quote = sys.argv[1], sys.argv[2]
t = norm(Path(ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")).read_text(encoding="utf-8", errors="replace"))
print("len:", len(norm(quote)), "verbatim:", norm(quote) in t)
