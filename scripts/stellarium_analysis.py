"""Analyze TYCHOS against a validated, reusable Stellarium reference."""
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

import analyze_ephemerides
import compare_ephemerides
import generate_report
from ephemeris_io import tychos_blocks
from stellarium.dataset import read_export

ROOT = Path(__file__).resolve().parents[1]


def run(args, registry, defaults):
    # Import here to reuse atomic publication without a module import cycle.
    from run_analysis import fingerprint, publish_file

    reference = args.stellarium.resolve()
    if not reference.is_file():
        raise ValueError(
            f'Stellarium dataset not found: {reference}. '
            'Restore the separately shared stellarium_ephemerides.jsonl beside manifest.json, '
            'or specify its location with --stellarium. Metadata alone cannot generate comparisons.'
        )
    manifest_path = reference.with_name('manifest.json')
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    else:
        # Existing pilot exports stored the manifest inside report.json.
        manifest_path = reference.with_name('report.json')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))['manifest']
    paths = {'tychos': args.tychos.resolve(), 'stellarium': reference,
             'stellarium_manifest': manifest_path}
    inputs = {name: {'path': str(path), 'sha256': fingerprint(path)}
              for name, path in paths.items()}
    settings, rows = read_export(reference, manifest)
    blocks = tychos_blocks(paths['tychos'].read_text(encoding='utf-8-sig'))
    bodies = args.bodies or defaults['bodies']
    if args.all:
        bodies = [body for body in registry if body in blocks and body in manifest['bodies']]
    bodies = list(dict.fromkeys(bodies))
    if not bodies or set(bodies) - set(registry):
        raise ValueError('Select registered bodies available in both exports')
    dates = [datetime.fromisoformat(date) for date in manifest['dates']]
    if dates != sorted(set(dates)) or len(dates) < 2:
        raise ValueError('Stellarium dates must be unique, increasing and nonempty')
    step = dates[1] - dates[0]
    if any(b - a != step for a, b in zip(dates, dates[1:])):
        raise ValueError('Stellarium reference has irregular cadence')
    tychos = {}
    for body in bodies:
        if body not in blocks or body not in manifest['bodies']:
            raise ValueError(f'{body}: missing from TYCHOS or Stellarium')
        tychos[body] = compare_ephemerides.parse_tychos(blocks[body], strict=True)
        if set(dates) - set(tychos[body]):
            raise ValueError(f'{body}: TYCHOS must contain every reference timestamp; no interpolation')
    output = (args.out_dir or ROOT/'reports/stellarium').resolve()
    if output == reference.parent or reference.parent in output.parents:
        raise ValueError('Keep analysis reports outside the saved reference directory')
    summaries = {}
    with tempfile.TemporaryDirectory(prefix='stellarium-analysis-') as temporary:
        stage = Path(temporary)
        for body in bodies:
            prefix = body + '_apparent_of_date'
            comparison = stage / (body + '_comparison.csv')
            with comparison.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(['date', 'ty_ra_deg', 'ty_dec_deg', 'stellarium_ra_deg',
                                 'stellarium_dec_deg', 'dra_deg', 'ddec_deg', 'sep_deg'])
                for date, iso in zip(dates, manifest['dates']):
                    ty = tychos[body][date]
                    ref = rows[(iso, body)]
                    ra, dec = ref['ra_date'], ref['dec_date']
                    writer.writerow([date.strftime('%Y-%m-%d %H:%M:%S'), ty['ra'], ty['dec'],
                                     ra, dec, compare_ephemerides.wrap_deg(ty['ra']-ra), ty['dec']-dec,
                                     compare_ephemerides.angular_separation_deg(ty['ra'], ty['dec'], ra, dec)])
            analyze_ephemerides.main([str(comparison), '--body', body, '--source', 'stellarium',
                                      '--prefix', prefix, '--out-dir', str(stage)])
            summary_path = stage / (prefix + '_summary.json')
            summary = json.loads(summary_path.read_text(encoding='utf-8'))
            summary['input_file'] = str(output / comparison.name)
            summary['provenance'] = {
                'analyzed_at_utc': datetime.now(timezone.utc).isoformat(), 'inputs': inputs,
                'export_label': args.label or 'TYCHOS export settings not recorded',
                'declared_export_settings': json.loads(args.export_settings.read_text(encoding='utf-8'))
                    if args.export_settings else None,
                'reference_settings': settings,
                'settings_note': 'TYCHOS settings are user-declared; Stellarium settings are recorded in its export.'}
            summary_path.write_text(json.dumps(summary, indent=2), encoding='utf-8')
            generate_report.main(['--summary', str(summary_path), '--annual',
                                  str(stage / (prefix + '_annual_stats.csv')), '--output',
                                  str(stage / (prefix + '_ephemeris_report.md'))])
            summaries[body] = summary
        lines = ['# TYCHOS versus Stellarium — apparent of date', '',
                 f'Reference: `{reference}`. Each comparison uses the complete saved reference interval.', '',
                 '| Body | Samples | RMS RA | RMS Dec | RMS separation |', '|---|---:|---:|---:|---:|']
        for body, summary in summaries.items():
            values = [summary[key]['rms_deg'] for key in
                      ('ra_residual', 'declination_residual', 'angular_separation')]
            lines.append(f"| [{body}]({body}_apparent_of_date_ephemeris_report.md) | {summary['n_samples']} | "
                         + ' | '.join(f'{value:.6f}°' for value in values) + ' |')
        (stage/'ephemeris_overview.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
        for name, path in paths.items():
            if fingerprint(path) != inputs[name]['sha256']:
                raise ValueError('Input changed during analysis; reports were not replaced')
        for path in stage.iterdir():
            publish_file(path, output/path.name)
    print(f'Stellarium analysis saved to {output}')
    return summaries
