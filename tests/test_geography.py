import json
import io
from unittest.mock import patch
from pathlib import Path
import tempfile
import unittest

from navigator.geography import ROOT, load_addresses, resolve_address
from navigator.geocode_worker import geocode


class GeographyTests(unittest.TestCase):
    def test_all_sample_addresses_loaded(self):
        self.assertEqual(len(load_addresses()), 500)

    def test_matched_jurisdiction_becomes_engine_fact_with_evidence(self):
        row = {'address_id': 'test', 'state': 'CA', 'postal_city': 'Postal City', 'year_built': '1927'}
        record = {'status': 'matched', 'jurisdiction': {
            'state': 'CA', 'city': 'Los Angeles', 'county': 'Los Angeles'},
            'evidence': [{'url': 'census-response'}]}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'geography.json'
            path.write_text(json.dumps({'addresses': {'test': record}}))
            result = resolve_address(row, {'state': 'NJ', 'legal_city': 'Newark'}, path)
        self.assertEqual(result['facts']['state'], 'CA')
        self.assertEqual(result['facts']['legal_city'], 'Los Angeles')
        self.assertEqual(result['fact_provenance']['legal_city']['evidence'], record['evidence'])
        self.assertEqual(result['facts']['year_built'], 1927)
        self.assertNotIn('occupancy_date', result['facts'])

    def test_ambiguous_coordinates_require_municipality_consensus(self):
        def candidate(city, geoid):
            return {'coordinates': {'x': -71, 'y': 42}, 'matchedAddress': 'candidate',
                    'geographies': {'States': [{'STUSAB': 'MA'}],
                                    'Incorporated Places': [{'BASENAME': city, 'GEOID': geoid}],
                                    'Counties': [{'BASENAME': 'Middlesex'}]}}
        row = {'address_id': 'test', 'street_address': '165 Cambridgepark Dr',
               'postal_city': 'Cambridge', 'state': 'MA', 'zip': ''}
        for other, expected in [(candidate('Cambridge', '1'), 'matched'),
                                (candidate('Boston', '2'), 'unresolved')]:
            payload = {'result': {'input': {}, 'addressMatches': [candidate('Cambridge', '1'), other]}}
            with tempfile.TemporaryDirectory(dir=ROOT / 'data') as folder:
                with patch('navigator.geocode_worker.urllib.request.urlopen',
                           return_value=io.BytesIO(json.dumps(payload).encode())):
                    result = geocode(row, Path(folder))
            self.assertEqual(result['status'], expected)
            self.assertIsNone(result['coordinates'])

    def test_unresolved_postal_city_and_supplied_state_are_not_legal_facts(self):
        row = {'address_id': 'missing', 'state': 'NJ', 'postal_city': 'Hoboken'}
        with tempfile.TemporaryDirectory() as folder:
            result = resolve_address(row, {'state': 'CA', 'legal_city': 'Los Angeles'}, Path(folder)/'none')
        self.assertEqual(result['facts']['supplied_state'], 'NJ')
        self.assertNotIn('state', result['facts'])
        self.assertNotIn('legal_city', result['facts'])
        self.assertEqual(result['questions'][0]['fact'], 'legal_city')


if __name__ == '__main__':
    unittest.main()
