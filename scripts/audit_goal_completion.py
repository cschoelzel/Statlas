#!/usr/bin/env python3
"""Local evidence gate; passing existing tests alone does not prove completion.

Official run evidence: reports/official_score_run.json with command, exit_code,
script, report, and sha256 values for script/report/output artifacts.
Video URLs alone remain unverified; supply three local video recordings.
This gate checks these deliverables only, not all jury criteria or legal accuracy.
"""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    try:
        return json.loads(path.read_text()), None
    except (OSError, ValueError) as error:
        return None, str(error)


def audit(root):
    checks = {}
    source_rules, source_error = read_json(root / 'data/rules.json')
    exported_rules, export_error = read_json(root / 'output/rules.json')
    checks['rules_export_current'] = {
        'pass': not source_error and not export_error and source_rules == exported_rules,
        'source_error': source_error, 'export_error': export_error,
        'note': 'Exact rule equality is necessary but does not prove lookup or change regeneration.'}
    changes, error = read_json(root / 'output/changes.json')
    for number in range(1, 7):
        name = f'T{number}'
        case = changes.get(name) if isinstance(changes, dict) else None
        gaps = []
        if not isinstance(case, dict):
            gaps.append('case_missing_or_invalid')
            case = {}
        if case.get('status') not in {'evaluated', 'evaluated_with_geographic_gaps', 'correctly_empty'}:
            gaps.append('status_not_evaluated')
        if case.get('missing_rule_ids') != []:
            gaps.append('missing_rule_ids_not_empty')
        if not isinstance(case.get('comparisons'), list) or not case['comparisons']:
            gaps.append('comparison_evidence_missing')
        checks[name] = {'pass': not gaps, 'status': case.get('status'),
                        'missing_rule_ids': case.get('missing_rule_ids'), 'gaps': gaps}
    if error:
        checks['changes_file'] = {'pass': False, 'error': error}

    run, error = read_json(root / 'reports/official_score_run.json')
    gaps = []
    if not isinstance(run, dict):
        run = {}
        gaps.append('official_run_evidence_missing')
    if run.get('exit_code') != 0 or not run.get('command'):
        gaps.append('successful_command_missing')
    for field in ('script', 'report'):
        value = run.get(field)
        path = root / value if isinstance(value, str) and value else None
        if not path or not path.is_file() or not path.stat().st_size:
            gaps.append(f'{field}_file_missing')
        elif digest(path) != run.get(f'{field}_sha256'):
            gaps.append(f'{field}_hash_missing_or_mismatch')
        if field == 'script' and path and path.name != 'score.py':
            gaps.append('script_is_not_score.py')
    artifact_hashes = run.get('artifacts_sha256', {})
    for name in ('rules.json', 'lookups.json', 'changes.json'):
        path = root / 'output' / name
        if not path.is_file() or digest(path) != artifact_hashes.get(name):
            gaps.append(f'{name}_scored_version_unverified')
    checks['official_score'] = {'pass': not gaps, 'gaps': gaps,
                                'note': 'Local run evidence does not establish scorer provenance.'}

    videos = []
    for directory in ('videos', 'output/videos', 'reports/videos'):
        folder = root / directory
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob('*')):
            if path.suffix.lower() not in {'.mp4', '.mov', '.webm', '.mkv'} or not path.is_file():
                continue
            with path.open('rb') as stream:
                header = stream.read(64)
            valid = len(header) >= 16 and (header[4:8] == b'ftyp' or header[:4] == b'\x1aE\xdf\xa3')
            videos.append({'path': str(path.relative_to(root)), 'container_signature_valid': valid,
                           'sha256': digest(path) if valid else None})
    recordings = {v['sha256'] for v in videos if v['container_signature_valid']}
    checks['videos'] = {'pass': len(recordings) >= 3, 'distinct_local_recordings': len(recordings),
                        'files': videos, 'note': 'Remote URLs unverified; signatures do not prove playback, duration, or content.'}
    return {'complete_for_checked_deliverables': all(c['pass'] for c in checks.values()),
            'scope': 'T1-T6 completeness, official score run evidence, three distinct local video containers',
            'checks': checks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    evidence = audit(args.root.resolve())
    print(json.dumps(evidence, ensure_ascii=False, indent=2))
    raise SystemExit(0 if evidence['complete_for_checked_deliverables'] else 1)
