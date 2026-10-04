import json, re, shutil, sys
from pathlib import Path
ROOT = Path("/Users/constantinscholzel/Documents/Projekte/Aktiv/hacknation26")
def norm(s):
    return re.sub("[^a-z0-9]", "", (s or "").lower())
def doctext(doc):
    p = ROOT / ("participant-final-no-hour16 3/corpus/text/" + doc + ".txt")
    return norm(p.read_text(encoding="utf-8", errors="replace")) if p.exists() else None
def find_gap_leaf(node, gap_fact):
    """Return (parent_list, index) of leaf with fact==gap_fact, or None."""
    found = []
    def walk(x):
        if isinstance(x, dict):
            if set(x.keys()) == {"fact", "op", "value"} and x.get("fact") == gap_fact:
                return x
            for v in x.values():
                r = walk(v)
                if r is not None:
                    return r
        elif isinstance(x, list):
            for i, v in enumerate(x):
                if isinstance(v, dict) and set(v.keys()) == {"fact", "op", "value"} and v.get("fact") == gap_fact:
                    found.append((x, i))
                else:
                    r = walk(v)
                    if r is not None:
                        return r
        return None
    walk(node.get("logic", {}))
    return found[0] if found else None
rules = json.load(open(ROOT / "data/rules.json"))
byid = {r.get("team_rule_id"): r for r in rules}
canon = set()
def collect(x):
    if isinstance(x, dict):
        if set(x.keys()) == {"fact", "op", "value"} and isinstance(x.get("fact"), str):
            if not x["fact"].startswith("unresolved"):
                canon.add(x["fact"])
        for v in x.values():
            collect(v)
    elif isinstance(x, list):
        for v in x:
            collect(v)
for r in rules:
    collect(r.get("logic", {}))
print("canonical facts:", len(canon))
files = sys.argv[1:] or ["/tmp/gapfix_A.json", "/tmp/gapfix_B.json"]
patches = []
for f in files:
    try:
        patches += json.load(open(f))
    except FileNotFoundError:
        print("missing:", f)
cache = {}
applied, removed, skipped = 0, 0, []
shutil.copy(ROOT / "data/rules.json", "/tmp/rules.backup.merge.json")
for p in patches:
    tid, gap, repl, st, q = p.get("team_rule_id"), p.get("gap_fact"), p.get("replacement"), p.get("status"), p.get("evidence_quote") or ""
    r = byid.get(tid)
    if r is None:
        skipped.append((tid, gap, "rule-missing"))
        continue
    if st != "resolved":
        skipped.append((tid, gap, "open"))
        continue
    doc = r.get("source_doc_id")
    if doc not in cache:
        cache[doc] = doctext(doc)
    t = cache.get(doc)
    if not t or norm(q) not in t:
        skipped.append((tid, gap, "quote-unverified"))
        continue
    loc = find_gap_leaf(r, gap)
    if loc is None:
        skipped.append((tid, gap, "gap-not-found"))
        continue
    plist, idx = loc
    if repl is None:
        del plist[idx]
        removed += 1
    else:
        if repl.get("fact") not in canon:
            skipped.append((tid, gap, "fact-not-canonical"))
            continue
        plist[idx] = repl
        applied += 1
print("replaced:", applied, "removed:", removed, "skipped:", len(skipped))
for s in skipped:
    print("SKIP:", s)
json.dump(rules, open(ROOT / "data/rules.json", "w"), ensure_ascii=False, indent=2)
print("saved, rules:", len(rules))
