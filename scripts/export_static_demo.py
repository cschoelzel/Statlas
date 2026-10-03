"""Static-Demo-Export (Option B): legt pro Adresse web/data/<AID>.json mit der
vollen lookup()-Antwort ab, damit web/results.html auch ohne Python-Server
(static hosting, file://) auswerten kann. Deterministisch: gleiche Eingaben,
gleicher Export. Lauf: python3 scripts/export_static_demo.py [--as-of YYYY-MM-DD]"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from navigator.app import lookup, address_list
as_of = sys.argv[sys.argv.index('--as-of')+1] if '--as-of' in sys.argv else '2026-10-01'
outdir = ROOT / 'web' / 'data'
outdir.mkdir(exist_ok=True)
addrs = address_list()
for i, a in enumerate(addrs):
    aid = a['address_id']
    (outdir / (aid + '.json')).write_text(json.dumps(lookup(aid, as_of), ensure_ascii=False))
    if (i+1) % 100 == 0:
        print(f'{i+1}/{len(addrs)}', flush=True)
print(f'done: {len(addrs)} adressen, as_of={as_of}')
