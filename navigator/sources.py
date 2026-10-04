"""Immutable source inventory; no legal conclusions inferred from retrieval timestamps."""
from __future__ import annotations
import csv, hashlib, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'participant-final-no-hour16 3'
LANDING = {'D045', 'D046', 'D047'}
CATEGORIES = ['rent_increase_limits', 'just_cause_eviction', 'security_deposits', 'application_screening_fees', 'screening_restrictions', 'algorithmic_rent_setting']

def freeze(content: bytes, suffix: str, base: Path) -> tuple[str,str]:
    digest = hashlib.sha256(content).hexdigest()
    path = base / 'originals' / (digest + suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise ValueError('Immutable source collision')
    if not path.exists():
        path.write_bytes(content)
        path.chmod(0o444)
    return digest, str(path.relative_to(ROOT))

def build_inventory(package: Path = PACKAGE, output: Path | None = None) -> list[dict]:
    output = output or ROOT / 'data/sources'
    output.mkdir(parents=True, exist_ok=True)
    existing = {r['doc_id']: r for r in json.loads((output/'index.json').read_text())} if (output/'index.json').exists() else {}
    records=[]
    for row in csv.DictReader((package/'corpus/corpus_manifest.csv').open()):
        text_path = package/'corpus'/row['text_file'] if row['text_file'] else None
        ready = bool(text_path and text_path.is_file())
        record = dict(doc_id=row['doc_id'],url=row['url'],jurisdictions=row['jurisdictions'],
            publisher=row['url'].split('/')[2],source_type=row['source_type'],document_type='supplied_text',
            upstream_hash=row['sha256'] or None,retrieved_at=row['retrieved_at'] or None,
            status='landing_page_only' if ready and row['doc_id'] in LANDING else 'full_text_ready' if ready else 'missing',
            original_file=None,text_file=None,sha256=None,text_sha256=None,parser_version='challenge-supplied-text-v1',
            historical_verification='unverified',temporal_status='unverified',legal_as_of=None,
            interpretation_status='not_reviewed',conflicts=[],capture_policy=row['capture'])
        if ready:
            digest,filename=freeze(text_path.read_bytes(),'.txt',output)
            record.update(sha256=digest,text_sha256=digest,original_file=filename,text_file=filename)
            if row['sha256'] and row['sha256'] != digest:
                record['conflicts'].append('upstream_hash_differs_from_supplied_text_bytes; upstream_hash_semantics_unknown')
        if row['capture']=='check-terms':
            record['access_note']='Publisher terms require verification before acquisition; use official alternatives.'
        if record['doc_id'] in existing and existing[record['doc_id']].get('previous_versions'):
            record = existing[record['doc_id']]
        records.append(record)
    (output/'index.json').write_text(json.dumps(records,indent=2)+'\n')
    coverage=defaultdict(list)
    for r in records: coverage[r['jurisdictions']].append(r)
    report={'total':len(records),'status_counts':dict(Counter(r['status'] for r in records)),
      'integrity_note':'SHA256 authenticates retained bytes only; upstream hashes are separate and unverified.',
      'historical_note':'Retrieval time is not an effective date. All historical applicability awaits source review.',
      'jurisdictions':{j:{'documents':[r['doc_id'] for r in rs],
          'missing':[r['doc_id'] for r in rs if r['status']=='missing'],
          'landing_only':[r['doc_id'] for r in rs if r['status']=='landing_page_only'],
          'categories':{c:{'status':'not_reviewed','reason':'Category coverage requires extraction and legal review; source presence is not legal completeness.'} for c in CATEGORIES}} for j,rs in coverage.items()}}
    (ROOT/'reports/sources_coverage.json').write_text(json.dumps(report,indent=2)+'\n')
    return records

if __name__ == '__main__':
    records=build_inventory()
    print(json.dumps({'total':len(records),'status_counts':dict(Counter(r['status'] for r in records))}))

def retain_acquisition(doc_id: str, content: bytes, url: str, retrieved_at: str, text: str,
                       parser_version: str, suffix: str = '.html') -> dict:
    """Add an immutable retrieval; preserve the original package record as provenance."""
    base=ROOT/'data/sources'
    records=json.loads((base/'index.json').read_text())
    record=next(r for r in records if r['doc_id']==doc_id)
    digest,original=freeze(content,suffix,base)
    text_digest,text_file=freeze(text.encode(),'.txt',base)
    record.setdefault('previous_versions',[]).append({k:record[k] for k in
        ['url','original_file','text_file','sha256','text_sha256','retrieved_at','parser_version','status']})
    record.update(url=url,original_file=original,text_file=text_file,sha256=digest,
        text_sha256=text_digest,retrieved_at=retrieved_at,parser_version=parser_version,
        status='full_text_ready',document_type='official_current_consolidated_statute',
        publisher=url.split('/')[2],source_type='official',historical_verification='unverified',
        historical_note='Current consolidated web retrieval requires amendment/effective-date review for 2026-10-01.')
    (base/'index.json').write_text(json.dumps(records,indent=2)+'\n')
    return record
