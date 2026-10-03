import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
ch = json.loads((ROOT / "output" / "changes.json").read_text())
t4 = newset = set(ch["T4"]["affected_address_ids"])
print("T4 affected:", sorted(t4))
print("unres8 in T4 aff:", sorted(t4 & {"A0098","A0128","A0295","A0346","A0352","A0376","A0380","A0384"}))
for tid in ("T1","T2","T3"):
    print(tid, "unresolved:", sorted(ch[tid]["unresolved_address_ids"]))
print("T2 affected sample:", ch["T2"]["affected_address_ids"][:12])
print("T3 flags sample:", ch["T3"]["conflict_flag_address_ids"][:12])
