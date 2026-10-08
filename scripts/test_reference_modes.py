import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze_ephemerides
import generate_report
import run_analysis
import compare_ephemerides
import download_jpl
from ephemeris_io import validate_jpl_header


class ReferenceModeTests(unittest.TestCase):
    def write_comparison(self, path):
        fields = [
            "date", "ty_ra_deg", "ty_dec_deg",
            "jpl_ra_icrf_deg", "jpl_dec_icrf_deg", "ddec_icrf_deg", "sep_icrf_deg",
            "jpl_ra_app_deg", "jpl_dec_app_deg", "ddec_app_deg", "sep_app_deg",
        ]
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for day in range(1, 9):
                ty_ra = 10.0 + day
                ty_dec = -5.0 + day * 0.1
                writer.writerow({
                    "date": f"2000-01-{day:02d} 00:00:00",
                    "ty_ra_deg": ty_ra,
                    "ty_dec_deg": ty_dec,
                    "jpl_ra_icrf_deg": ty_ra - 0.2,
                    "jpl_dec_icrf_deg": ty_dec + 0.1,
                    "ddec_icrf_deg": -0.1,
                    "sep_icrf_deg": 0.22,
                    "jpl_ra_app_deg": ty_ra - 0.05,
                    "jpl_dec_app_deg": ty_dec + 0.02,
                    "ddec_app_deg": -0.02,
                    "sep_app_deg": 0.054,
                })

    def test_apparent_is_default_and_ignores_fixed_frame_columns(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            comparison = root / "mercury_comparison.csv"
            self.write_comparison(comparison)

            analyze_ephemerides.main([
                str(comparison), "--body", "mercury",
                "--prefix", "mercury_apparent_of_date", "--out-dir", str(root),
            ])

            apparent = json.loads(
                (root / "mercury_apparent_of_date_summary.json").read_text(encoding="utf-8")
            )

            self.assertEqual(apparent["reference_mode"], "apparent-of-date")
            self.assertNotIn("ecliptic_longitude_residual", apparent)
            self.assertAlmostEqual(apparent["ra_residual"]["rms_deg"], 0.05)

            annual = root / "mercury_apparent_of_date_annual_stats.csv"
            with annual.open(encoding="utf-8", newline="") as stream:
                fields = csv.DictReader(stream).fieldnames
            self.assertIn("rms_dra_deg", fields)
            self.assertNotIn("rms_dlon_deg", fields)

            report = root / "mercury_apparent_of_date_ephemeris_report.md"
            generate_report.main([
                "--summary", str(root / "mercury_apparent_of_date_summary.json"),
                "--annual", str(annual), "--output", str(report),
            ])
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("true-equator/equinox-of-date", report_text)
            self.assertIn("J2000 ecliptic residuals are intentionally omitted", report_text)

    def test_fixed_frame_modes_are_rejected(self):
        with self.assertRaises(SystemExit):
            analyze_ephemerides.main(['unused.csv', '--body', 'sun', '--reference', 'icrf'])
        with self.assertRaises(SystemExit):
            run_analysis.main(['--reference', 'both'])

    def test_new_horizons_format_and_legacy_bundle_have_same_apparent_values(self):
        header = ('Target body name: Sun (10)\nCenter body name: Earth (399)\n'
                  'Center-site name: GEOCENTRIC\nDate__(UT)__HR:MN:SS, ')
        new = header + 'R.A.____(a-app), DEC_____(a-app)\n$$SOE\n2000-Jan-01 00:00:00, , , 01 00 00, +10 00 00,\n$$EOE'
        legacy = header + 'R.A._____(ICRF), DEC____(ICRF), R.A.____(a-app), DEC_____(a-app)\n$$SOE\n2000-Jan-01 00:00:00, , , 02 00 00, +20 00 00, 01 00 00, +10 00 00,\n$$EOE'
        validate_jpl_header(new)
        first = compare_ephemerides.parse_jpl(new, strict=True)
        self.assertEqual(first, compare_ephemerides.parse_jpl(legacy, strict=True))
        self.assertEqual(set(next(iter(first.values()))), {'ra_app', 'dec_app'})
        self.assertIn('QUANTITIES=%272%27', download_jpl.build_url('10', '2000-01-01', '2000-01-02', '3 h'))

    def test_run_analysis_publishes_only_apparent_report_set(self):
        with tempfile.TemporaryDirectory(dir=run_analysis.ROOT / "data") as temporary:
            root = Path(temporary)
            tychos = root / "tychos.txt"
            jpl = root / "jpl.txt"
            tychos_lines = ["PLANET: SUN"]
            jpl_lines = [
                "Target body name: Sun (10)",
                "Center body name: Earth (399)",
                "Center-site name: GEOCENTRIC",
                "Date__(UT)__HR:MN:SS, R.A._____(ICRF), R.A.____(a-app)",
                "$$SOE",
            ]
            for day in range(1, 9):
                tychos_lines.append(
                    f"2000-01-{day:02d} | 00:00:00 | 01h00m00.000s | +10°00'00.000\""
                )
                jpl_lines.append(
                    f" 2000-Jan-{day:02d} 00:00:00, , , 00 59 59.000000, +10 00 01.00000, "
                    "00 59 59.500000, +10 00 00.50000,"
                )
            jpl_lines.append("$$EOE")
            tychos.write_text("\n".join(tychos_lines) + "\n", encoding="utf-8")
            jpl.write_text("\n".join(jpl_lines) + "\n", encoding="utf-8")

            original_reports, original_derived = run_analysis.REPORTS, run_analysis.DERIVED
            try:
                run_analysis.REPORTS = root / "reports"
                run_analysis.DERIVED = root / "derived"
                run_analysis.main([
                    "sun", "--tychos", str(tychos), "--jpl", str(jpl),
                    "--label", "apparent-only smoke test",
                ])
            finally:
                run_analysis.REPORTS = original_reports
                run_analysis.DERIVED = original_derived

            self.assertFalse((root / "reports/sun_summary.json").exists())
            self.assertTrue((root / "reports/sun_apparent_of_date_summary.json").exists())
            self.assertFalse((root / "reports/sun_ephemeris_report.md").exists())
            self.assertTrue((root / "reports/sun_apparent_of_date_ephemeris_report.md").exists())
            overview = (root / "reports/ephemeris_overview.md").read_text(encoding="utf-8")
            self.assertNotIn("JPL ICRF astrometric RA/Dec", overview)
            comparison = (root / 'derived/sun_comparison.csv').read_text(encoding='utf-8')
            self.assertNotIn('icrf', comparison)
            self.assertIn("true-equator/equinox-of-date", overview)


if __name__ == "__main__":
    unittest.main()
