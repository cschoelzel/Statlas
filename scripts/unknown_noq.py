import json
from pathlib import Path
from collections import Counter
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
out = json.load(open(ROOT / "output/lookups.json"))
looks = out.get("lookups", out) if isinstance(out, dict) else out
pat = Counter()
ex = {}
for aid, recs in looks.items():
    for r in recs:
        if r.get("result") == "unknown" and not (r.get("targeted_questions") or []):
            key = (r.get("team_rule_id"), tuple(sorted(r.get("missing_facts", []) or [])), tuple(sorted(str(x)[:60] for x in (r.get("review_required", []) or []))))
            pat[(r.get("team_rule_id"), str(sorted(r.get("missing_facts", []) or []))[:120])] += 1
            if r.get("team_rule_id") not in ex:
                ex[r.get("team_rule_id")] = {"addr": aid, "missing": r.get("missing_facts"), "review": [str(x)[:150] for x in (r.get("review_required", []) or [])], "expl": str(r.get("explanation"))[:200]}
print("patterns:", len(pat))
for k, n in pat.most_common(15):
    print(n, k)
import sys
for tid in sys.argv[1:]:
    print("=" * 60); print(tid, json.dumps(ex.get(tid), ensure_ascii=False)[:800])
