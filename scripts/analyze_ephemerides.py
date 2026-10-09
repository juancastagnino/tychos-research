#!/usr/bin/env python3
"""Analyze apparent-of-date TYCHOS-minus-JPL RA/Dec and angular residuals.
No fixed-frame ecliptic rotation is performed."""
import argparse
import csv
import json
import math
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
import numpy as np

def wrap_deg(x):
    return (x + 180.0) % 360.0 - 180.0

def rms(a):
    a = np.asarray(a, dtype=float)
    return float(np.sqrt(np.mean(a * a)))

def percentile_abs(a, p):
    return float(np.percentile(np.abs(np.asarray(a, dtype=float)), p))

def stats(a):
    a = np.asarray(a, dtype=float)
    return {'mean_deg': float(np.mean(a)), 'rms_deg': rms(a), 'median_abs_deg': float(np.median(np.abs(a))), 'p95_abs_deg': percentile_abs(a, 95), 'max_abs_deg': float(np.max(np.abs(a)))}
REFERENCE_COLUMNS = {'apparent-of-date': {'ra': 'jpl_ra_app_deg', 'dec': 'jpl_dec_app_deg', 'ddec': 'ddec_app_deg', 'sep': 'sep_app_deg', 'label': 'JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)'}}

def read_comparison(path, reference='apparent-of-date', source='jpl'):
    columns = REFERENCE_COLUMNS[reference]
    if source == 'stellarium':
        columns = {'ra': 'stellarium_ra_deg', 'dec': 'stellarium_dec_deg',
                   'ddec': 'ddec_deg', 'sep': 'sep_deg'}
    rows = []
    with open(path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        required = {'date', 'ty_ra_deg', 'ty_dec_deg', columns['ra'], columns['dec'], columns['ddec'], columns['sep']}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'Missing required columns: {sorted(missing)}')
        for r in reader:
            rows.append({'date': datetime.strptime(r['date'], '%Y-%m-%d %H:%M:%S'), 'ty_ra_deg': float(r['ty_ra_deg']), 'ty_dec_deg': float(r['ty_dec_deg']), 'jpl_ra_deg': float(r[columns['ra']]), 'jpl_dec_deg': float(r[columns['dec']]), 'ddec_deg': float(r[columns['ddec']]), 'sep_deg': float(r[columns['sep']])})
    if not rows:
        raise ValueError('No rows found in comparison CSV')
    return rows

def fft_peaks(t_days, y_deg, min_period=1.0, max_period=500.0, n_peaks=20):
    t = np.asarray(t_days, dtype=float)
    y = np.asarray(y_deg, dtype=float)
    if len(t) < 8:
        return []
    dt = np.diff(t)
    step = float(np.median(dt))
    if np.max(np.abs(dt - step)) > max(1e-09, step * 1e-05):
        return []
    tc = t - np.mean(t)
    X = np.column_stack([np.ones_like(tc), tc])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    detrended = y - X @ coef
    window = np.hanning(len(y))
    yw = detrended * window
    spec = np.fft.rfft(yw)
    freq = np.fft.rfftfreq(len(y), d=step)
    amp = 2.0 * np.abs(spec) / np.sum(window)
    peaks = []
    for i in range(1, len(freq)):
        if freq[i] <= 0:
            continue
        period = 1.0 / freq[i]
        if min_period <= period <= max_period:
            peaks.append((float(amp[i]), float(period), float(freq[i])))
    peaks.sort(reverse=True)
    selected = []
    for amplitude, period, frequency in peaks:
        if any((abs(period - p['period_days']) / period < 0.01 for p in selected)):
            continue
        selected.append({'period_days': period, 'amplitude_deg': amplitude, 'frequency_cycles_per_day': frequency})
        if len(selected) >= n_peaks:
            break
    return selected

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison_csv')
    parser.add_argument('--out-dir', default='reports')
    parser.add_argument('--body', required=True)
    parser.add_argument('--profile', choices=('auto', 'none'), default='auto')
    parser.add_argument('--prefix', help='Output prefix; defaults to <body>_apparent_of_date')
    parser.add_argument('--reference', choices=tuple(REFERENCE_COLUMNS), default='apparent-of-date', help='JPL coordinate product to analyze (apparent-of-date only)')
    parser.add_argument('--source', choices=('jpl', 'stellarium'), default='jpl')
    args = parser.parse_args(argv)
    if not re.fullmatch('[a-z][a-z0-9_]*', args.body):
        parser.error('Body must be a lowercase identifier')
    prefix = args.prefix or args.body + '_apparent_of_date'
    if not re.fullmatch('[a-z][a-z0-9_]*', prefix):
        parser.error('Prefix must be a lowercase identifier')
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_comparison(args.comparison_csv, args.reference, args.source)
    dates = [r['date'] for r in rows]
    if dates != sorted(set(dates)):
        raise ValueError('Comparison dates must be unique and increasing')
    if not all((math.isfinite(v) for row in rows for k, v in row.items() if k != 'date')):
        raise ValueError('Comparison contains non-finite coordinates')
    t0 = dates[0]
    t_days = np.array([(d - t0).total_seconds() / 86400.0 for d in dates])
    ty_ra = np.array([r['ty_ra_deg'] for r in rows])
    ty_dec = np.array([r['ty_dec_deg'] for r in rows])
    jp_ra = np.array([r['jpl_ra_deg'] for r in rows])
    jp_dec = np.array([r['jpl_dec_deg'] for r in rows])
    dra = np.array([wrap_deg(v) for v in ty_ra - jp_ra])
    ddec = np.array([r['ddec_deg'] for r in rows])
    sep = np.array([r['sep_deg'] for r in rows])
    fft_values = dra
    fft_observable = 'right ascension residual'
    cadence_hours = None
    if len(dates) > 1:
        cadence_hours = float(np.median(np.diff(t_days)) * 24.0)
    summary = {'body': args.body, 'profile': 'none', 'input_file': str(args.comparison_csv), 'reference_mode': args.reference, 'reference': REFERENCE_COLUMNS[args.reference]['label'], 'ecliptic_rotation': 'Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity', 'n_samples': len(rows), 'start': dates[0].strftime('%Y-%m-%d %H:%M:%S'), 'stop': dates[-1].strftime('%Y-%m-%d %H:%M:%S'), 'cadence_hours_median': cadence_hours, 'cadence_regular': bool(len(t_days) < 2 or np.allclose(np.diff(t_days), np.diff(t_days)[0], rtol=0, atol=1e-09)), 'fft_period_range_days': [1.0, 500.0], 'fft_observable': fft_observable, 'ra_residual': stats(dra), 'declination_residual': stats(ddec), 'angular_separation': stats(sep)}
    summary['reference_source'] = args.source
    if args.source == 'stellarium':
        summary['reference'] = 'Stellarium Earth geocentric apparent equinox-of-date RA/Dec (airless)'
    with (out_dir / f'{prefix}_summary.json').open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    peaks = fft_peaks(t_days, fft_values)
    with (out_dir / f'{prefix}_fft_peaks.csv').open('w', newline='', encoding='utf-8') as f:
        fields = ['rank', 'period_days', 'amplitude_deg', 'frequency_cycles_per_day']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, p in enumerate(peaks, 1):
            w.writerow({'rank': i, **p})
    years = defaultdict(list)
    for i, d in enumerate(dates):
        years[d.year].append(i)
    with (out_dir / f'{prefix}_annual_stats.csv').open('w', newline='', encoding='utf-8') as f:
        fields = ['year', 'n', 'rms_dra_deg', 'rms_ddec_deg', 'rms_sep_deg']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for year in sorted(years):
            idx = np.array(years[year], dtype=int)
            row = {'year': year, 'n': len(idx), 'rms_ddec_deg': rms(ddec[idx]), 'rms_sep_deg': rms(sep[idx])}
            row['rms_dra_deg'] = rms(dra[idx])
            w.writerow(row)
    with (out_dir / f'{prefix}_residuals.csv').open('w', newline='', encoding='utf-8') as f:
        ref_ra, ref_dec = args.source + '_ra_deg', args.source + '_dec_deg'
        fields = ['date', 'ty_ra_deg', 'ty_dec_deg', ref_ra, ref_dec, 'dra_deg', 'ddec_deg', 'sep_deg']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for i, d in enumerate(dates):
            row = {'date': d.strftime('%Y-%m-%d %H:%M:%S'), 'ty_ra_deg': ty_ra[i], 'ty_dec_deg': ty_dec[i], ref_ra: jp_ra[i], ref_dec: jp_dec[i], 'dra_deg': dra[i], 'ddec_deg': ddec[i], 'sep_deg': sep[i]}
            w.writerow(row)
    print(f'Samples: {len(rows)}')
    print(f'Interval: {dates[0]} -> {dates[-1]}')
    print(f'Median cadence: {cadence_hours:.3f} h' if cadence_hours is not None else 'Median cadence: n/a')
    print(f"Reference     : {summary['reference']}")
    print(f'RA RMS        : {rms(dra):.6f} deg')
    print(f'Dec RMS      : {rms(ddec):.6f} deg')
    print(f'Separation RMS: {rms(sep):.6f} deg')
    print(f'Reports written to: {out_dir}')
if __name__ == '__main__':
    main()
