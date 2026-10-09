"""Compare short/full intervals and test one shared small-angle frame rotation.

Uses apparent-of-date coordinates. The fitted rotation is diagnostic only;
it never changes exports and cannot establish a physical cause.
"""
import argparse
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

from compare_ephemerides import parse_tychos, parse_jpl, wrap_deg
from ephemeris_io import tychos_blocks, jpl_blocks, validate_jpl_header

ROOT = Path(__file__).resolve().parents[1]


def vectors(coords):
    ra, dec = np.radians(coords).T
    return np.column_stack((np.cos(dec)*np.cos(ra), np.cos(dec)*np.sin(ra), np.sin(dec)))


def separation(a, b):
    u, v = vectors(a), vectors(b)
    return np.degrees(np.arctan2(np.linalg.norm(np.cross(u, v), axis=1), np.sum(u*v, axis=1)))


def metrics(a, b):
    residual = np.column_stack((wrap_deg(a[:, 0]-b[:, 0]), a[:, 1]-b[:, 1], separation(a, b)))
    return {'mean_deg': residual.mean(axis=0).tolist(),
            'rms_deg': np.sqrt(np.mean(residual**2, axis=0)).tolist(),
            'p95_abs_deg': np.percentile(np.abs(residual), 95, axis=0).tolist()}


def rotation_design(ref):
    ra, dec = np.radians(ref).T
    east = np.column_stack((-np.cos(ra)*np.sin(dec), -np.sin(ra)*np.sin(dec), np.cos(dec)))
    north = np.column_stack((np.sin(ra), -np.cos(ra), np.zeros(len(ra))))
    return np.stack((east, north), axis=1).reshape(-1, 3)


def fit_rotation(data, bodies, mask):
    x, y = [], []
    for body in bodies:
        ty, ref = data[body]
        ref, ty = ref[mask], ty[mask]
        x.append(rotation_design(ref))
        y.append(np.column_stack((wrap_deg(ty[:, 0]-ref[:, 0])*np.cos(np.radians(ref[:, 1])),
                                  ty[:, 1]-ref[:, 1])).ravel())
    omega, _, rank, _ = np.linalg.lstsq(np.vstack(x), np.concatenate(y), rcond=None)
    if rank != 3:
        raise ValueError('Rotation fit is not identifiable')
    return omega


def corrected(coords, omega_deg):
    omega = np.radians(omega_deg)
    angle = np.linalg.norm(omega)
    if angle == 0:
        return coords.copy()
    x, y, z = omega/angle
    skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    rotation = np.eye(3)+np.sin(angle)*skew+(1-np.cos(angle))*(skew@skew)
    v = vectors(coords) @ rotation
    return np.column_stack((np.degrees(np.arctan2(v[:, 1], v[:, 0])) % 360,
                            np.degrees(np.arcsin(np.clip(v[:, 2], -1, 1)))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tychos', type=Path, default=ROOT/'00-backup/tychos_ephemerides.txt')
    parser.add_argument('--stellarium', type=Path, default=ROOT/'00-backup/stellarium_ephemerides.jsonl')
    parser.add_argument('--jpl', type=Path, default=ROOT/'data/raw/jpl_ephemerides.txt')
    parser.add_argument('--out-dir', type=Path, default=ROOT/'reports/first-year-frame-check')
    args = parser.parse_args()
    manifest_path = ROOT/'data/stellarium/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    provenance = json.loads((ROOT/'data/stellarium/reference_provenance.json').read_text(encoding='utf-8'))
    paths = {'tychos': args.tychos, 'stellarium': args.stellarium, 'jpl': args.jpl,
             'stellarium_manifest': manifest_path}
    hashes = {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in paths.items()}
    if hashes['stellarium'] != provenance['sha256']['stellarium_export.jsonl']:
        raise ValueError('Stellarium export does not match saved provenance')
    registry = json.loads((ROOT/'scripts/bodies.json').read_text(encoding='utf-8'))
    bodies = [body for body in registry if body in manifest['bodies']]
    dates = [datetime.fromisoformat(s) for s in manifest['dates']]
    index = {s: i for i, s in enumerate(manifest['dates'])}
    stellar = {body: np.full((len(dates), 2), np.nan) for body in bodies}
    with args.stellarium.open(encoding='utf-8-sig') as stream:
        metadata = json.loads(next(stream))
        if metadata != provenance['settings'] or metadata['run_id'] != manifest['run_id']:
            raise ValueError('Stellarium metadata mismatch')
        complete = None
        for line in stream:
            row = json.loads(line)
            if row['kind'] == 'complete':
                complete = row['count']
                continue
            if complete is not None or row['kind'] != 'position':
                raise ValueError('Unexpected Stellarium row')
            body, i = row['body'], index[row['date']]
            if np.isfinite(stellar[body][i]).any():
                raise ValueError('Duplicate Stellarium sample')
            if abs((datetime.fromisoformat(row['actual_date'].removesuffix('Z'))-dates[i]).total_seconds()) > 1:
                raise ValueError('Stellarium date mismatch')
            stellar[body][i] = row['ra_date'], row['dec_date']
    if complete != len(dates)*len(bodies) or not all(np.isfinite(v).all() for v in stellar.values()):
        raise ValueError('Incomplete Stellarium grid')
    tb = tychos_blocks(args.tychos.read_text(encoding='utf-8-sig'))
    jb = jpl_blocks(args.jpl.read_text(encoding='utf-8-sig'))
    tychos, jpl = {}, {}
    for body in bodies:
        t = parse_tychos(tb[body], strict=True)
        block = jb[registry[body]['target_id']]
        validate_jpl_header(block)
        j = parse_jpl(block, strict=True)
        if set(dates) != set(t) or set(dates) != set(j):
            raise ValueError(f'{body}: mismatched sample grid')
        tychos[body] = np.array([[t[d]['ra'], t[d]['dec']] for d in dates])
        jpl[body] = np.array([[j[d]['ra_app'], j[d]['dec_app']] for d in dates])
    first = np.array([datetime(2000, 6, 21) <= d < datetime(2001, 6, 21) for d in dates])
    if first.sum() != 2920:
        raise ValueError('Expected a complete first year at 3-hour cadence')
    masks = {'first_year': first, 'full_interval': np.ones(len(dates), dtype=bool),
             'last_year': np.array([datetime(2025, 6, 21) <= d < datetime(2026, 6, 21) for d in dates])}
    pairs = {'tychos_vs_jpl': (tychos, jpl), 'tychos_vs_stellarium': (tychos, stellar),
             'stellarium_vs_jpl': (stellar, jpl)}
    result = {'inputs': {key: {'path': str(paths[key]), 'sha256': value} for key, value in hashes.items()},
              'first_year': '[2000-06-21, 2001-06-21) UTC', 'first_year_samples': int(first.sum()),
              'coordinate_order': ['RA', 'declination', 'angular_separation'], 'metrics': {}, 'rotation_tests': {}}
    for name, (a, b) in pairs.items():
        result['metrics'][name] = {body: {label: metrics(a[body][mask], b[body][mask])
                                          for label, mask in masks.items()} for body in bodies}
    result['reference_timing_checks'] = {}
    for body in bodies:
        errors = separation(stellar[body], jpl[body])
        bad = np.flatnonzero(first & (errors > 1/3600))
        bad = bad[(bad > 0) & (bad < len(dates)-1)]
        if not len(bad):
            continue
        offsets = (-1, 0, 1)
        shifted = np.column_stack([separation(stellar[body][bad], jpl[body][bad+offset])
                                   for offset in offsets])
        best = np.argmin(shifted, axis=1)
        result['reference_timing_checks'][body] = {
            'outliers_above_one_arcsecond': len(bad),
            'first_outlier': dates[bad[0]].isoformat(), 'last_outlier': dates[bad[-1]].isoformat(),
            'best_offset_counts_hours': {str(3*offset): int(np.sum(best == i))
                                         for i, offset in enumerate(offsets)},
            'rms_arcsec_by_offset_hours': {str(3*offset): float(np.sqrt(np.mean(shifted[:, i]**2))*3600)
                                          for i, offset in enumerate(offsets)}}
    first_indices = np.flatnonzero(first)
    train = first.copy()
    train[first_indices[len(first_indices)//2:]] = False
    test = first & ~train
    groups = {'all_ten': bodies, 'without_mercury_pluto': [b for b in bodies if b not in ('mercury', 'pluto')]}
    for name, (a, b) in pairs.items():
        data = {body: (a[body], b[body]) for body in bodies}
        result['rotation_tests'][name] = {}
        for group, selected in groups.items():
            omega = fit_rotation(data, selected, train)
            per_body = {body: {'before_deg': metrics(a[body][test], b[body][test])['rms_deg'][2],
                              'after_deg': metrics(corrected(a[body][test], omega), b[body][test])['rms_deg'][2]}
                        for body in bodies}
            before = np.sqrt(np.mean([per_body[b]['before_deg']**2 for b in selected]))
            after = np.sqrt(np.mean([per_body[b]['after_deg']**2 for b in selected]))
            result['rotation_tests'][name][group] = {'omega_deg': omega.tolist(),
                'angle_deg': float(np.linalg.norm(omega)), 'held_out_before_deg': float(before),
                'held_out_after_deg': float(after), 'per_body': per_body}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    lines = ['# First-year apparent-of-date frame check', '',
             'Current TYCHOS export. First year: 21 June 2000 to 21 June 2001 (end exclusive), 2,920 samples per body.',
             'The exports do not cover January–June 2000. Full interval: 21 June 2000 to 21 June 2026.', '',
             'RMS and means below are in degrees. Rotation is a diagnostic, not an applied correction.', '']
    for name, by_body in result['metrics'].items():
        lines += [f'## {name}', '', '| Body | First-year mean RA | Mean Dec | RMS RA | RMS Dec | RMS separation | Full RMS separation | Last-year RMS separation |',
                  '|---|---:|---:|---:|---:|---:|---:|---:|']
        for body, values in by_body.items():
            f = values['first_year']
            nums = [*f['mean_deg'][:2], *f['rms_deg'], values['full_interval']['rms_deg'][2], values['last_year']['rms_deg'][2]]
            lines.append('| '+body+' | '+' | '.join(f'{v:.6f}' for v in nums)+' |')
        lines.append('')
    lines += ['## Shared rotation — temporal validation', '',
              'Fit one three-axis rotation on the first half of the first year; evaluate on the second half.',
              'All bodies receive the same rotation. Values are pooled angular RMS with equal sample counts.', '',
              '| Comparison | Fit group | Rotation magnitude | Held-out RMS before | Held-out RMS after |', '|---|---|---:|---:|---:|']
    for name, groups_result in result['rotation_tests'].items():
        for group, values in groups_result.items():
            lines.append(f"| {name} | {group} | {values['angle_deg']:.6f}° | {values['held_out_before_deg']:.6f}° | {values['held_out_after_deg']:.6f}° |")
    lines += ['', '## Reference timestamp quality checks', '',
              'For first-year Stellarium/JPL disagreements above 1 arcsecond, compare adjacent JPL timestamps (3-hour cadence).', '']
    for body, check in result['reference_timing_checks'].items():
        lines += [f"- {body}: {check['outliers_above_one_arcsecond']} affected samples; {check['first_outlier']} through {check['last_outlier']}.",
                  f"  Best JPL offset counts (hours): {check['best_offset_counts_hours']}.",
                  f"  RMS disagreement (arcseconds) by JPL offset: {check['rms_arcsec_by_offset_hours']}."]
    lines += ['', 'These samples are flagged, not shifted or repaired. A match to an earlier timestamp is evidence of a timing/update issue, not proof of its software cause.', '',
              '## Interpretation limits', '',
              '- A short interval reduces some accumulated drift; it does not eliminate a fixed frame offset or orbital errors.',
              '- A fitted rotation can absorb model errors; its success alone does not establish a reference-frame cause.',
              '- Inspect results.json for per-body effects, rotation components and input hashes.',
              '- Strong changes between bodies or degradation on held-out dates argue against a single constant rotation being the main explanation.',
              '- No export or model configuration was changed.']
    (args.out_dir/'report.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
