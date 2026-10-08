import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from dataset import read_export, prepare


class ExportValidationTests(unittest.TestCase):
    def test_prepare_requests_apparent_coordinates_only(self):
        with tempfile.TemporaryDirectory() as directory:
            args = SimpleNamespace(profile=Path(directory), start='2000-06-21 00:00',
                                   stop='2000-06-21 06:00', wait=0.2)
            prepare(args)
            script = (Path(directory)/'scripts/export.ssc').read_text()
            self.assertIn('setFlagLightTravelTime(true)', script)
            self.assertIn('"StelCore.flagUseNutation", true', script)
            self.assertIn('"StelCore.flagUseAberration", true', script)
            self.assertNotIn('raJ2000', script)

    def test_geometric_profile_and_disabled_corrections_rejected(self):
        manifest, entries = self.fixture()
        manifest.pop('reference_mode')
        with self.assertRaisesRegex(ValueError, 'Old geometric'):
            self.read(manifest, entries)
        manifest['reference_mode'] = 'apparent-of-date'
        for field in ('light_travel_time', 'aberration', 'nutation'):
            entries[0][field] = False
            with self.assertRaisesRegex(ValueError, 'settings'):
                self.read(manifest, entries)
            entries[0][field] = True

    def fixture(self):
        dates = ['2000-06-21T00:00:00', '2000-06-21T06:00:00']
        manifest = {'dates': dates, 'bodies': ['moon'], 'run_id': 'test', 'reference_mode': 'apparent-of-date'}
        entries = [{'kind': 'metadata', 'source': 'Stellarium', 'run_id': 'test', 'planetocentric': True,
                    'light_travel_time': True, 'aberration': True, 'nutation': True,
                    'aberration_factor': 1.0, 'atmosphere': False, 'reference_mode': 'apparent-of-date'}]
        for i, date in enumerate(dates):
            entries.append({'kind': 'position', 'date': date, 'actual_date': date,
                            'body': 'moon', 'ra': 317+i*3, 'dec': -18+i,
                            'ra_date': 317+i*3, 'dec_date': -18+i, 'delta_t_seconds': 64})
        entries.append({'kind': 'complete', 'count': 2})
        return manifest, entries

    def read(self, manifest, entries):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'export.jsonl'
            path.write_text('\n'.join(json.dumps(x) for x in entries))
            return read_export(path, manifest)

    def test_complete_export(self):
        manifest, entries = self.fixture()
        self.assertEqual(len(self.read(manifest, entries)[1]), 2)

    def test_missing_completion(self):
        manifest, entries = self.fixture()
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            self.read(manifest, entries[:-1])

    def test_wrong_date(self):
        manifest, entries = self.fixture()
        entries[2]['actual_date'] = entries[1]['actual_date']
        with self.assertRaisesRegex(ValueError, 'date'):
            self.read(manifest, entries)

    def test_stale_positions(self):
        manifest, entries = self.fixture()
        entries[2]['ra_date'], entries[2]['dec_date'] = entries[1]['ra_date'], entries[1]['dec_date']
        with self.assertRaisesRegex(ValueError, 'Repeated'):
            self.read(manifest, entries)

    def test_wrong_observer(self):
        manifest, entries = self.fixture()
        entries[0]['planetocentric'] = False
        with self.assertRaisesRegex(ValueError, 'settings'):
            self.read(manifest, entries)

    def test_previous_export_rejected(self):
        manifest, entries = self.fixture()
        entries[0]['run_id'] = 'previous'
        with self.assertRaisesRegex(ValueError, 'earlier run'):
            self.read(manifest, entries)


if __name__ == '__main__':
    unittest.main()
