"""Local demo and reproducible CLI. No model or network calls during evaluation."""
import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'participant-final-no-hour16 3'
DISCLAIMER = 'Not legal advice. Source gaps and unresolved interpretations require qualified review.'


@lru_cache(maxsize=16)
def _cached_json(path, modified, size):
    return json.loads(Path(path).read_text())

def read_json(path, default=None):
    if not path.exists():
        return default
    stat=path.stat()
    return _cached_json(str(path),stat.st_mtime_ns,stat.st_size)


def load_rules():
    raw = read_json(ROOT / 'data/rules.json', [])
    return raw.get('rules', []) if isinstance(raw, dict) else raw


def source_coverage():
    raw = read_json(ROOT / 'data/sources/index.json', [])
    records = raw.get('sources', []) if isinstance(raw, dict) else raw
    supplemental = []
    for meta_path in sorted((ROOT / 'data/sources_new').glob('*.meta.json')):
        metadata = read_json(meta_path, {})
        stem = meta_path.name.removesuffix('.meta.json')
        text_path = meta_path.parent / (stem + '.txt')
        expected_hash = metadata.get('text_sha256')
        text_verified = bool(expected_hash and text_path.is_file()
                             and hashlib.sha256(text_path.read_bytes()).hexdigest() == expected_hash)
        original_path = next((meta_path.parent / (stem + suffix) for suffix in ('.html', '.pdf')
                              if (meta_path.parent / (stem + suffix)).is_file()), None)
        raw_verified = bool(metadata.get('raw_sha256') and original_path
                            and hashlib.sha256(original_path.read_bytes()).hexdigest() == metadata['raw_sha256'])
        supplemental.append({'raw_sha256_verified': raw_verified,
                             'source_doc_id': metadata.get('doc_id') or stem,
                             'source_url': metadata.get('source_url') or metadata.get('url'),
                             'text_sha256_verified': text_verified,
                             'capture_quartet_complete': bool((metadata.get('source_url') or metadata.get('url'))
                                 and metadata.get('retrieved_at') and text_verified),
                             'metadata': {key: metadata[key] for key in
                             ('doc_id', 'source_url', 'retrieved_at', 'raw_sha256', 'text_sha256')
                             if key in metadata},
                             'metadata_file': str(meta_path.relative_to(ROOT)),
                             'text_available': (meta_path.parent / (stem + '.txt')).is_file(),
                             'rule_import_status': 'not_verified'})
    return {'supplemental_sources': supplemental,
            'supplemental_inventory': len(supplemental),
            'inventory': len(records), 'statuses': dict(Counter(r.get('status','unknown') for r in records)),
            'review_status': 'External qualified legal review remains open.',
            'sources': records}


def address_list():
    from navigator.geography import load_addresses
    return load_addresses()


def lookup(address_id, as_of='2026-10-01', supplied=None):
    from navigator.geography import resolve_address
    from navigator.engine import evaluate_rules
    addresses = {r['address_id']:r for r in address_list()}
    if address_id not in addresses:
        raise ValueError('Unknown address_id')
    supplied = supplied or {}
    if not isinstance(supplied, dict):
        raise ValueError('facts must be an object')
    geo = resolve_address(addresses[address_id])
    facts = dict(geo.get('facts', {}))
    # User claims are never promoted to authoritative location evidence.
    protected = {'state', 'legal_city', 'address_id', 'coordinates', 'jurisdiction'}
    for key, value in supplied.items():
        if key not in protected and isinstance(value, (str,int,float,bool,type(None))):
            facts[key] = None if value in ('unknown', 'declined', '') else value
    rules = load_rules()
    decisions = evaluate_rules(rules, facts, as_of)
    by_id = {r['team_rule_id']:r for r in rules}
    for decision in decisions:
        decision['rule'] = by_id[decision['team_rule_id']]
    # Ehrlich: ohne Jurisdiktion kann keine Entscheidung kippen, solange die Gemeinde
    # unbekannt ist. Jede fraglose unknown-Entscheidung erhaelt die Geo-Rueckfrage,
    # damit Punkt 6 des Ziels (unknown nur mit Rueckfrage) auch hier gilt.
    # Gap-Research-Fragen bleiben daneben erhalten (keine Maskierung): Geo zuerst,
    # Research danach. Eine getippte Antwort allein begruendet keine Jurisdiktion
    # (protected-Facts) — Heilung nur per Parzellen-/Gemeindenachweis ins Dataset.
    if geo.get('status') != 'matched':
        geo_question = (geo.get('questions') or [{}])[0]
        for decision in decisions:
            if decision.get('result') == 'unknown':
                existing = decision.get('targeted_questions') or []
                facts_asked = {item.get('fact') for item in existing if isinstance(item, dict)}
                if 'legal_city' not in facts_asked:
                    decision['targeted_questions'] = [{
                        'fact': geo_question.get('fact', 'legal_city'),
                        'question': geo_question.get('question', 'What municipality legally contains this property?'),
                        'why_needed': 'Without legal jurisdiction no rule can be applied or excluded. A typed answer is recorded as unverified and does not alone establish jurisdiction; healing requires a parcel or municipal boundary record reviewed into the dataset.',
                        'source_doc_id': decision.get('team_rule_id'),
                        'acceptable_evidence': 'Parcel record or municipal boundary evidence reviewed into the dataset (a typed answer alone is insufficient)',
                        'may_decline': True, 'research_task': True}] + existing
                decision['missing_facts'] = sorted(set(decision.get('missing_facts', [])) | {'legal_city'})
    provenance = {key:{'value': value, 'status':'user_reported' if key in supplied and key not in protected else 'imported',
                        'verified':False} for key,value in facts.items()}
    questions = {}
    for decision in decisions:
        for question in decision.get('targeted_questions', []):
            fact = question['fact']
            item = questions.setdefault(fact, {**question, 'rule_ids':[], 'citations':[],
                   'evidence_needed':'Provide an official record when available; user answers remain unverified.'})
            item['rule_ids'].append(decision['team_rule_id'])
            item['citations'].append(decision.get('evidence', {}).get('citation'))
    for question in geo.get('questions', []):
        if isinstance(question, dict):
            questions.setdefault(question.get('fact','legal_city'), question)
    return {'address':addresses[address_id], 'geography':geo, 'as_of':as_of,
            'decisions':decisions, 'questions':sorted(questions.values(), key=lambda q:(-len(q.get('rule_ids',[])),q.get('fact',''))),
            'facts':provenance, 'coverage':source_coverage(), 'disclaimer':DISCLAIMER}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':'))


def export(as_of='2026-10-01'):
    from navigator.changes import evaluate_changes
    output = ROOT / 'output'; output.mkdir(exist_ok=True)
    rules = load_rules()
    full = {a['address_id']:lookup(a['address_id'],as_of) for a in address_list()}
    results = {aid: bundle['decisions'] for aid, bundle in full.items()}
    facts = {aid: {'facts': bundle['geography'].get('facts', {}),
                   'fact_provenance': bundle['geography'].get('fact_provenance', {}),
                   'geography_status': bundle['geography'].get('status'),
                   'jurisdiction': bundle['geography'].get('jurisdiction')} for aid, bundle in full.items()}
    changes = evaluate_changes(rules,address_list())
    for name,value in [('rules.json',rules),('rules.wrapped.json',{'rules':rules}),
                       ('lookups.json',{'as_of':as_of,'lookups':results,'disclaimer':DISCLAIMER}),
                       ('facts.json',{'as_of':as_of,'facts':facts,'disclaimer':DISCLAIMER}),('changes.json',changes)]:
        (output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    fingerprint = hashlib.sha256(canonical({'rules':rules,'lookups':results,'changes':changes}).encode()).hexdigest()
    manifest = {'as_of':as_of,'rules':len(rules),'addresses':len(results),'sha256':fingerprint,
                'generated_at':datetime.now(timezone.utc).isoformat(),'disclaimer':DISCLAIMER}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


class Handler(BaseHTTPRequestHandler):
    def send_json(self, value, status=200):
        content=json.dumps(value,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(content))); self.end_headers(); self.wfile.write(content)
    def do_GET(self):
        parsed=urlsplit(self.path)
        path=parsed.path
        query=parse_qs(parsed.query)
        as_of=query.get('as_of',['2026-10-01'])[0]
        if path=='/api/health':
            return self.send_json({'status':'ready' if load_rules() else 'preparation_incomplete','rules':len(load_rules()),'coverage':source_coverage(),'disclaimer':DISCLAIMER})
        if path=='/api/addresses':
            return self.send_json({'addresses':address_list(),'disclaimer':DISCLAIMER})
        if path=='/api/changes':
            from navigator.changes import evaluate_changes
            return self.send_json(evaluate_changes(load_rules(),address_list()))
        if path=='/api/portfolio':
            rows=[]
            for address in address_list():
                item=lookup(address['address_id'],as_of)
                rows.append({'address':address,'geography_status':item['geography']['status'],
                             'results':dict(Counter(d['result'] for d in item['decisions'])),
                             'questions':len(item['questions']),
                             'conflicts':sum(d['conflict_flag'] for d in item['decisions'])})
            return self.send_json({'as_of':as_of,'properties':rows,'disclaimer':DISCLAIMER})
        if path=='/api/sources':
            return self.send_json(source_coverage())
        target_name = 'index.html' if path == '/' else ('results.html' if path == '/results' else path.lstrip('/'))
        target=(ROOT/'web'/target_name).resolve()
        if not target.is_relative_to(ROOT/'web') or not target.is_file():
            return self.send_json({'error':'Not found'},404)
        content=target.read_bytes(); mime={'.html':'text/html','.js':'application/javascript','.css':'text/css'}.get(target.suffix,'application/octet-stream')
        self.send_response(200); self.send_header('Content-Type',mime+'; charset=utf-8')
        self.send_header('Content-Length',str(len(content))); self.end_headers(); self.wfile.write(content)
    def do_POST(self):
        if urlsplit(self.path).path!='/api/lookup':
            return self.send_json({'error':'Not found'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length>32768: raise ValueError('Request too large')
            request=json.loads(self.rfile.read(length))
            return self.send_json(lookup(request['address_id'],request.get('as_of','2026-10-01'),request.get('facts')))
        except (ValueError,KeyError,TypeError) as exc:
            return self.send_json({'error':str(exc),'disclaimer':DISCLAIMER},400)
    def log_message(self,fmt,*args):
        pass


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['serve','export','lookup'])
    parser.add_argument('--port',type=int,default=8765); parser.add_argument('--as-of',default='2026-10-01')
    parser.add_argument('--address',default='A0001'); args=parser.parse_args()
    if args.command=='serve':
        print(f'Navigator: http://127.0.0.1:{args.port}',flush=True)
        ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
    elif args.command=='export': print(json.dumps(export(args.as_of)))
    else: print(json.dumps(lookup(args.address,args.as_of),ensure_ascii=False,indent=2))

if __name__=='__main__': main()
