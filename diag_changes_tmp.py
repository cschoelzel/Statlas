import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
ch = json.loads((ROOT / "output" / "changes.json").read_text())
for tid, v in ch.items():
    print(tid, "aff", len(v.get("affected_address_ids", [])), "unres", len(v.get("unresolved_address_ids", [])), "flag", len(v.get("conflict_flag_address_ids", [])), v.get("status"))
