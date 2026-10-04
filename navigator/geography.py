"""Census-backed address jurisdiction lookup; postal cities are not legal proof."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ADDRESSES = ROOT / 'participant-final-no-hour16 3/data/sample_addresses.csv'
DEFAULT_GEOGRAPHY = ROOT / 'data/geography.json'


def load_addresses(path=None):
    with open(path or DEFAULT_ADDRESSES, newline='', encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def resolve_address(address, facts=None, geography_path=None):
    rows = load_addresses()
    if isinstance(address, str):
        address = next((row for row in rows if row['address_id'] == address),
                       {'address_id': address})
    path = Path(geography_path or DEFAULT_GEOGRAPHY)
    records = json.loads(path.read_text())['addresses'] if path.exists() else {}
    result = dict(records.get(address.get('address_id'), {
        'status': 'unresolved', 'jurisdiction': {'state': None, 'city': None, 'county': None},
        'coordinates': None, 'evidence': [],
        'uncertainty': ['No authoritative jurisdiction match available.'],
    }))
    result['address'] = address
    result['facts'] = {key: value for key, value in (facts or {}).items()
                       if key not in ('state', 'legal_city', 'county')}
    if address.get('state'):
        result['facts']['supplied_state'] = address['state']
    jurisdiction = result.get('jurisdiction', {})
    if result['status'] == 'matched':
        for field, key in (('state', 'state'), ('city', 'legal_city'), ('county', 'county')):
            if jurisdiction.get(field):
                result['facts'][key] = jurisdiction[field]
    # Assessor year built is never a certificate-of-occupancy date.
    for key in ('year_built', 'units', 'use_code', 'use_description'):
        value = address.get(key)
        if value not in (None, '') and key not in result['facts']:
            if key in ('year_built', 'units'):
                try:
                    value = int(value)
                except (TypeError, ValueError):
                    continue
            result['facts'][key] = value
    result['fact_provenance'] = {
        key: {'source': address.get('source_dataset'), 'retrieved_at': address.get('retrieved_at'),
              'status': 'supplied_dataset_unverified'}
        for key in ('year_built', 'units', 'use_code', 'use_description') if address.get(key)
    }
    # Ehrlicher Alias: Regeln fragen 'unit_count', Datensaetze liefern 'units'.
    # Identische Bedeutung (Wohneinheiten laut Parzellendatensatz), keine Schwelle geraten.
    # Leere Felder bleiben unbekannt (kein Default 0). Provenienz bleibt unverified.
    unit_value = result['facts'].get('units')
    if isinstance(unit_value, int) and unit_value >= 0 and 'unit_count' not in result['facts']:
        result['facts']['unit_count'] = unit_value
        result['fact_provenance']['unit_count'] = {
            'source': address.get('source_dataset'), 'retrieved_at': address.get('retrieved_at'),
            'status': 'derived_alias_of_units_unverified'}
    if address.get('state'):
        result['fact_provenance']['supplied_state'] = {
            'source': address.get('source_dataset'), 'status': 'supplied_dataset_unverified',
            'retrieved_at': address.get('retrieved_at')}
    if result['status'] == 'matched':
        for key in ('state', 'legal_city', 'county'):
            if key in result['facts']:
                result['fact_provenance'][key] = {
                    'source': 'U.S. Census Bureau', 'status': 'census_geography_matched',
                    'evidence': result.get('evidence', []),
                    'limitation': 'Street-range interpolation; historical parcel boundaries unverified.'}
    result['questions'] = [] if result['status'] == 'matched' else [{
        'field': 'legal_jurisdiction', 'fact': 'legal_city',
        'question': 'What municipality legally contains this property? Provide parcel or municipal boundary evidence.',
        'reason': 'Postal city does not establish municipal jurisdiction.',
        'why_needed': 'Without legal jurisdiction no rule can be applied or excluded.',
        'acceptable_evidence': 'Parcel record or municipal boundary evidence reviewed into the dataset (a typed answer alone is insufficient).',
    }]
    return result


def resolve_addresses(path=None):
    return [resolve_address(row) for row in load_addresses(path)]
