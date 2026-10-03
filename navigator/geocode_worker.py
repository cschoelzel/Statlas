"""Run on server: python3 -m navigator.geocode_worker. Free Census API only."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
import urllib.parse
import urllib.request
from .geography import ROOT, load_addresses

BASE = 'https://geocoding.geo.census.gov/geocoder'


def geocode(row, raw_dir, retry=False):
    params = {'address': ', '.join(row[k] for k in ('street_address', 'postal_city', 'state', 'zip')),
              'benchmark': 'Public_AR_Current', 'vintage': 'Current_Current', 'format': 'json'}
    url = BASE + '/geographies/onelineaddress?' + urllib.parse.urlencode(params)
    if retry:
        street = row['street_address']
        street = re.sub(r'^(\d+)-(?:\d+(?:\.\d+)?)\s+', r'\1 ', street)
        street = re.sub(r'\b0+(\d+(?:ST|ND|RD|TH))\b', r'\1', street, flags=re.I)
        params['address'] = ', '.join((street, row['postal_city'], row['state']))
        url = BASE + '/geographies/onelineaddress?' + urllib.parse.urlencode(params)
    fetched = datetime.now(timezone.utc).isoformat()
    result = {'status': 'unresolved', 'coordinates': None,
              'jurisdiction': {'state': None, 'city': None, 'county': None}, 'evidence': [],
              'uncertainty': []}
    try:
        with urllib.request.urlopen(url, timeout=25) as response:
            raw = response.read()
        path = raw_dir / (row['address_id'] + ('_retry' if retry else '') + '_' + hashlib.sha256(raw).hexdigest()[:12] + '.json')
        path.write_bytes(raw)
        payload = json.loads(raw)['result']
        result['evidence'] = [{'query_variant': 'normalized_street_without_zip' if retry else 'original', 'publisher': 'U.S. Census Bureau', 'url': url,
            'retrieved_at': fetched, 'raw_file': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(raw).hexdigest(), 'input': payload.get('input')}]
        matches = payload.get('addressMatches', [])
        if not matches:
            result['uncertainty'].append('No unique Census address match.')
            return result
        if len(matches) > 1:
            scopes = []
            for candidate in matches:
                areas = candidate.get('geographies', {})
                st = areas.get('States', [])
                towns = areas.get('Incorporated Places', [])
                if not towns and row['state'] == 'MA':
                    towns = [p for p in areas.get('County Subdivisions', []) if p.get('FUNCSTAT') == 'A']
                scopes.append((st[0].get('STUSAB') if len(st)==1 else None,
                               towns[0].get('GEOID') if len(towns)==1 else None))
            result['match_candidates'] = [{'matched_address': c.get('matchedAddress'),
                'coordinates': c.get('coordinates')} for c in matches]
            if len(set(scopes)) != 1 or scopes[0][1] is None:
                result['uncertainty'].append('Multiple address matches do not establish one municipality.')
                return result
            result['uncertainty'].append('Multiple address coordinates; all returned candidates share the same municipality. No unique property coordinate asserted.')
        match = matches[0]
        geo = match['geographies']
        states, counties = geo.get('States', []), geo.get('Counties', [])
        places = geo.get('Incorporated Places', [])
        if not places and row['state'] == 'MA':
            places = [p for p in geo.get('County Subdivisions', []) if p.get('FUNCSTAT') == 'A']
        state = states[0].get('STUSAB') if len(states) == 1 else None
        city = places[0].get('BASENAME') if len(places) == 1 else None
        result.update(coordinates=match['coordinates'] if len(matches)==1 else None, matched_address=match['matchedAddress'],
                      tiger_line=match.get('tigerLine'),
                      jurisdiction={'state': state, 'city': city,
                                    'county': counties[0].get('BASENAME') if len(counties)==1 else None},
                      geography_geoids={k: [p.get('GEOID') for p in geo.get(k, [])]
                                        for k in ('States','Counties','Incorporated Places','County Subdivisions')})
        # Census is street-range interpolation, not parcel-level spatial proof.
        result['status'] = 'matched' if state == row['state'] and city else 'uncertain'
        if retry:
            result['uncertainty'].append('Matched fallback query normalized street ranges/ordinals and omitted supplied ZIP; original address remains unchanged.')
        result['uncertainty'].append('Street-range interpolated coordinate; parcel boundaries and historical jurisdiction not independently confirmed.')
        if state != row['state']:
            result['uncertainty'].append('Matched state differs from supplied state.')
        if not city:
            result['uncertainty'].append('No unique active municipal geography; possible unincorporated property.')
    except Exception as error:
        result['uncertainty'].append(type(error).__name__ + ': ' + str(error))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int)
    parser.add_argument('--retry-unresolved', action='store_true')
    args = parser.parse_args()
    raw_dir = ROOT / 'data/geography_raw'
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = load_addresses()[:args.limit]
    output = ROOT / 'data/geography.json'
    records = json.loads(output.read_text())['addresses'] if output.exists() else {}
    if args.retry_unresolved:
        rows = [r for r in rows if records.get(r['address_id'], {}).get('status') != 'matched']
    with ThreadPoolExecutor(max_workers=4) as executor:
        jobs = {executor.submit(geocode, row, raw_dir, args.retry_unresolved): row['address_id'] for row in rows}
        for job in as_completed(jobs):
            new = job.result()
            old = records.get(jobs[job], {})
            if args.retry_unresolved:
                new['evidence'] = old.get('evidence', []) + new.get('evidence', [])
            records[jobs[job]] = new
            pending = output.with_suffix('.json.tmp')
            pending.write_text(json.dumps({'provider': 'U.S. Census Bureau',
                'benchmark_requested': 'Public_AR_Current', 'vintage_requested': 'Current_Current',
                'historical_boundary_verified': False, 'addresses': records}, indent=2))
            pending.replace(output)
    print(json.dumps({'total': len(records), 'matched': sum(r['status']=='matched' for r in records.values())}))

if __name__ == '__main__':
    main()
