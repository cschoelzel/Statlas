import json, re, shutil
from collections import Counter
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
def doctext(doc):
    p = ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")
    return norm(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
rules = json.load(open(ROOT / "data/rules.json"))
print("vorher:", len(rules))
cache = {}
def verified(rule):
    doc = rule.get("source_doc_id")
    if doc not in cache:
        cache[doc] = doctext(doc)
    q, t = norm(rule.get("quoted_span")), cache.get(doc)
    return bool(q) and len(q) >= 40 and t is not None and q[:60] in t and q[-60:] in t
shutil.copy(ROOT / "data/rules.json", "/tmp/rules.backup.178.json")
# 1. Regeln ohne Korpustext entfernen (D017)
gone = [r.get("team_rule_id") for r in rules if doctext(r.get("source_doc_id")) is None]
rules = [r for r in rules if doctext(r.get("source_doc_id")) is not None]
print("entfernt ohne Korpustext:", gone)
# 2. Kurzform-Jurisdiktionen nur nach Zitatpruefung
fix = {"Los Angeles": "Los Angeles, CA", "San Diego": "San Diego, CA",
       "San Francisco": "San Francisco, CA", "Boston": "Boston, MA", "California": "CA"}
nf = ns = 0
for r in rules:
    j = r.get("jurisdiction")
    if j in fix:
        if verified(r):
            r["jurisdiction"] = fix[j]; nf += 1
        else:
            ns += 1; print("SKIP:", r.get("team_rule_id"), j)
print("juris fixed:", nf, "skipped:", ns)
# 3. Doppel-IDs nach Zitatpruefung neu vergeben
used = set(r.get("team_rule_id") for r in rules)
for tid, cnt in Counter(r.get("team_rule_id") for r in rules).items():
    if cnt < 2:
        continue
    recs = [r for r in rules if r.get("team_rule_id") == tid]
    n = 0
    for r in recs[1:]:
        print(tid, "extra_verified" if verified(r) else "extra_UNBELEGT", (r.get("title") or "")[:50])
        while True:
            n += 1
            cand = tid.rsplit("-", 1)[0] + ("-r%03d" % n)
            if cand not in used:
                break
        r["team_rule_id"] = cand; used.add(cand)
# 4. D022 Pseudo-Exemption (kein Ausnahmetext im Korpus, per grep verifiziert)
for r in rules:
    if r.get("team_rule_id") == "D022-r001":
        lg = r.get("logic", {})
        if isinstance(lg.get("exemptions"), dict) and lg["exemptions"].get("fact") == "false":
            lg["exemptions"] = False
            if r.get("exemptions") == {"fact": "false", "op": "eq", "value": True}:
                r["exemptions"] = False
            print("D022 exemptions -> false")
ids = [r.get("team_rule_id") for r in rules]
print("dups:", [k for k, v in Counter(ids).items() if v > 1], "nachher:", len(rules))
json.dump(rules, open(ROOT / "data/rules.json", "w"), ensure_ascii=False, indent=2)
print("gespeichert")
