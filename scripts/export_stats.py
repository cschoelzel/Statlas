import json
from pathlib import Path
from collections import Counter
ROOT = Path(__file__).resolve().parent.parent
out = json.load(open(ROOT / "output/lookups.json"))
looks = out.get("lookups", out) if isinstance(out, dict) else out
c = Counter()
n_unknown_noq = 0
gap_unknown = 0
applies = Counter()
n_total = 0
per_addr = Counter()
for aid, recs in looks.items():
    per_addr[aid] = len(recs)
    for r in recs:
        n_total += 1
        res = r.get("result")
        c[res] += 1
        if res == "applies":
            applies[r.get("team_rule_id")] += 1
        if res == "unknown":
            mf = r.get("missing_facts", []) or []
            tq = r.get("targeted_questions", []) or []
            rev = " ".join(str(x) for x in (r.get("review_required", []) or []))
            has_gap = any("nresolved" in str(m) for m in mf) or "nresolved" in rev
            if not tq:
                n_unknown_noq += 1
            if has_gap:
                gap_unknown += 1
print("total:", n_total, dict(c))
print("unknown without question:", n_unknown_noq)
print("unknown with gap-cause:", gap_unknown)
print("applies by rule:", dict(applies))
import statistics
print("decisions/addr min/max:", min(per_addr.values()), max(per_addr.values()))
addrs_zero = [a for a, n in per_addr.items() if n == 0]
print("addrs with 0 decisions:", len(addrs_zero), addrs_zero[:10])
