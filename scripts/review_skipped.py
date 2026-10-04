import json, re, sys
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
raw = {}
def doctext_raw(doc):
    if doc not in raw:
        p = ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")
        raw[doc] = p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
    return raw[doc]
rules = json.load(open(ROOT / "data/rules.json"))
byid = {r.get("team_rule_id"): r for r in rules}
todo = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
for tid in (sys.argv[2:] or [x.get("team_rule_id") for x in todo]):
    entries = [x for x in todo if x.get("team_rule_id") == tid]
    r = byid.get(tid)
    if not entries or r is None:
        print("=" * 70); print(tid, "rule-missing" if r is None else "no-entry"); continue
    e = entries[0]
    doc = r.get("source_doc_id")
    t_raw, t = doctext_raw(doc), norm(doctext_raw(doc))
    q_raw, q = e.get("evidence_quote"), norm(e.get("evidence_quote"))
    print("=" * 70)
    print(tid, "|", doc, "| gap:", e.get("gap_fact"), "| repl:", json.dumps(e.get("replacement"))[:160])
    print("QUOTE:", e.get("evidence_quote"))
    n = len(q)
    while n > 0 and q[:n] not in t:
        n -= 1
    print("prefix-match:", n, "/", len(q))
    if n > 30:
        idx = t.find(q[:n])
        # map norm index back is hard; instead find raw anchor: first 30 norm chars locate via search on raw lowered alnum
        anchor = q[:30]
        low = re.sub("[^a-z0-9]", "", t_raw.lower())
        # show raw text around: find position of anchor in spaceless raw
        print("DOC-CONTEXT:")
        # print raw lines containing distinctive words
        words = re.findall("[a-z]{5,}", e.get("evidence_quote").lower())[:6]
        for line in t_raw.splitlines():
            ll = line.lower()
            if sum(1 for w in words if w in ll) >= 2:
                print("   ", line.strip()[:200])
