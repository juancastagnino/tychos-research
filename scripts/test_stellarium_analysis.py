import contextlib
from datetime import datetime, timedelta
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_analysis
from stellarium.dataset import collect


class StellariumAnalysisTests(unittest.TestCase):
    def fixture(self, root):
        profile = root/'profile'
        (profile/'scripts').mkdir(parents=True)
        dates = [(datetime(2000, 1, 1)+timedelta(hours=3*i)).isoformat() for i in range(8)]
        manifest = {'source': 'Stellarium', 'reference_mode': 'apparent-of-date',
                    'dates': dates, 'bodies': ['sun'], 'run_id': 'test', 'tychos': 'missing.txt'}
        metadata = {'kind': 'metadata', 'source': 'Stellarium', 'reference_mode': 'apparent-of-date',
                    'run_id': 'test', 'planetocentric': True, 'light_travel_time': True,
                    'aberration': True, 'nutation': True, 'aberration_factor': 1, 'atmosphere': False}
        entries = [metadata] + [{'kind': 'position', 'body': 'sun', 'date': date,
            'actual_date': date, 'ra_date': 15+i/10, 'dec_date': 10, 'delta_t_seconds': 64}
            for i, date in enumerate(dates)] + [{'kind': 'complete', 'count': 8}]
        (profile/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        (profile/'scripts/export.ssc').write_text('// fixture', encoding='utf-8')
        (profile/'stellarium_export.jsonl').write_text('\n'.join(json.dumps(e) for e in entries), encoding='utf-8')
        tychos = root/'tychos.txt'
        lines = ['PLANET: SUN'] + [datetime.fromisoformat(date).strftime('%Y-%m-%d | %H:%M:%S')
                 + ' | 01h00m00.000s | +10°00\'00.000"' for date in dates]
        tychos.write_text('\n'.join(lines), encoding='utf-8')
        return profile, tychos

    def test_reference_collection_and_reusable_analysis(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            profile, tychos = self.fixture(root)
            reference_dir = root/'reference'
            args = SimpleNamespace(profile=profile, output=reference_dir, reference_only=True)
            collect(args)  # Succeeds even though the manifest's TYCHOS path is missing.
            reference = reference_dir/'stellarium_ephemerides.jsonl'
            before = reference.read_bytes()
            output = root/'reports'
            run_analysis.main(['--source', 'stellarium', '--all', '--tychos', str(tychos),
                               '--stellarium', str(reference), '--out-dir', str(output)])
            summary = json.loads((output/'sun_apparent_of_date_summary.json').read_text())
            self.assertEqual(summary['reference_source'], 'stellarium')
            self.assertEqual(summary['n_samples'], 8)
            self.assertEqual(summary['cadence_hours_median'], 3)
            self.assertIn('stellarium', summary['provenance']['inputs'])
            csv_text = (output/'sun_apparent_of_date_residuals.csv').read_text()
            self.assertIn('stellarium_ra_deg', csv_text)
            self.assertNotIn('jpl_ra_deg', csv_text)
            self.assertEqual(reference.read_bytes(), before)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                collect(args)

    def test_missing_tychos_sample_does_not_publish_reports(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            root = Path(directory)
            profile, tychos = self.fixture(root)
            lines = tychos.read_text(encoding='utf-8').splitlines()
            tychos.write_text('\n'.join(lines[:-1]), encoding='utf-8')
            output = root/'reports'
            with self.assertRaisesRegex(ValueError, 'every reference timestamp'):
                run_analysis.main(['--source', 'stellarium', '--all', '--tychos', str(tychos),
                    '--stellarium', str(profile/'stellarium_export.jsonl'), '--out-dir', str(output)])
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
