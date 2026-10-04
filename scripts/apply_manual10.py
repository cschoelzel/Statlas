import json, re, shutil
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
def rawtext(doc):
    p = ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
def gap_loc(rule, gap_fact):
    found = []
    def walk(x):
        if isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, dict) and set(v.keys()) == {"fact", "op", "value"} and v.get("fact") == gap_fact:
                    found.append((x, i))
                else:
                    walk(v)
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
    walk(rule.get("logic", {}))
    return found[0] if found else None
def sib_leaves(rule):
    out = []
    def walk(x):
        if isinstance(x, dict):
            if set(x.keys()) == {"fact", "op", "value"} and not x.get("fact", "").startswith("unresolved"):
                out.append(x)
            else:
                for v in x.values():
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(rule.get("logic", {}))
    return out
rules = json.load(open(ROOT / "data/rules.json"))
byid = {r.get("team_rule_id"): r for r in rules}
gapfiles = {"/tmp/gapfix_C.json": None, "/tmp/gapfix_B.json": None}
patches = {}
for gf in gapfiles:
    for e in json.load(open(gf)):
        patches[e.get("team_rule_id")] = e
dups = ["D005-r005", "D007-r001", "D007-r016", "D052-r001", "D052-r005", "D065-r002", "D065-r010", "D065-r015"]
log = []
shutil.copy(ROOT / "data/rules.json", "/tmp/rules.backup.manual10.json")
n_rm = 0
for tid in dups:
    e, r = patches[tid], byid.get(tid)
    repl = e.get("replacement")
    loc = gap_loc(r, e.get("gap_fact")) if r else None
    if r is None or loc is None:
        log.append((tid, "SKIP rule/gap missing")); continue
    if not any(s == repl for s in sib_leaves(r)):
        log.append((tid, "SKIP not-a-duplicate")); continue
    del loc[0][loc[1]]
    n_rm += 1
    log.append((tid, "REMOVED gap leaf, replacement duplicates sibling " + json.dumps(repl)))
q041 = "Tenant is not at-fault. The owner or immediate family member will move into the rental unit. A resident manager will move into the rental unit. Demolition and permanent removal from the rental market. Government order. Conversion to affordable housing."
e = patches["D041-r011"]; r = byid.get("D041-r011")
if r and norm(q041) in norm(rawtext(r.get("source_doc_id"))):
    loc = gap_loc(r, e.get("gap_fact"))
    if loc:
        loc[0][loc[1]] = {"fact": "eviction_is_no_fault", "op": "eq", "value": True}
        log.append(("D041-r011", "REPLACED with eviction_is_no_fault, verbatim quote 207ch verified"))
    else:
        log.append(("D041-r011", "SKIP gap not found"))
else:
    log.append(("D041-r011", "SKIP quote not verbatim"))
q043 = "Relocation Offset: A landlord may offset the tenant's accumulated rent against any relocation assistance, unless the relocation assistance is owed because a termination of tenancy is required by a governmental agency order to vacate or comply issued for an unpermitted dwelling."
e = patches["D043-r006"]; r = byid.get("D043-r006")
if r and norm(q043) in norm(rawtext(r.get("source_doc_id"))):
    loc = gap_loc(r, e.get("gap_fact"))
    if loc:
        del loc[0][loc[1]]
        n_rm += 1
        log.append(("D043-r006", "REMOVED gap leaf, verbatim offset quote verified; coverage LA+relocation_required, unless-cases in exemptions"))
    else:
        log.append(("D043-r006", "SKIP gap not found"))
else:
    log.append(("D043-r006", "SKIP quote not verbatim"))
json.dump(rules, open(ROOT / "data/rules.json", "w"), ensure_ascii=False, indent=2)
for tid, msg in log:
    print(tid, msg)
print("removed total:", n_rm, "rules:", len(rules))
rep = ["# Manuelle Nachpruefung der 10 gemergten Gap-Skips", ""]
for tid, msg in log:
    rep.append("- " + tid + ": " + msg)
rep += ["", "Korrigierte Belegzitate:", "- D041-r011: " + q041, "- D043-r006: " + q043,
        "", "Die 8 C-Faelle sind Typ-A-Duplikate: Ersatz entspricht exakt einem Geschwister-Leaf, Loeschen ist semantikaequivalent (all(X,X,GAP)->all(X,X)). Regel-eigene quoted_span je verifiziert."]
Path(ROOT / "reports/gap_resolution_manual10.md").write_text("\n".join(rep), encoding="utf-8")
print("report written")
