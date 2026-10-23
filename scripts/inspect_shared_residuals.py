"""Read-only exploratory residual-phase regressions for the saved research CSVs."""
import argparse
from pathlib import Path
import numpy as np


def design(angle):
    return np.column_stack([np.ones(len(angle)), np.cos(angle), np.sin(angle),
                            np.cos(2 * angle), np.sin(2 * angle)])


def fit_and_validate(x, y, train, test):
    coef = np.linalg.lstsq(x[train], y[train], rcond=None)[0]
    errors = y[test] - x[test] @ coef
    control = y[test] - np.mean(y[train])
    denominator = np.mean(control ** 2)
    return coef, 1 - np.mean(errors ** 2) / denominator if denominator else float('nan')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('folder', type=Path)
    args = p.parse_args()
    bodies = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    frames = {b: np.genfromtxt(args.folder / f'{b}_apparent_of_date_residuals.csv', delimiter=',', names=True, dtype=None, encoding='utf-8') for b in bodies}
    sun = frames['sun']
    for body, frame in frames.items():
        if not np.array_equal(frame['date'], sun['date']):
            raise ValueError(f'{body}: timestamps do not match Sun')
        date = frame['date'].astype('datetime64[s]')
        train = date < np.datetime64('1913-01-01')
        test = ~train
        days = (date - np.datetime64('2000-01-01T00:00:00')) / np.timedelta64(1, 'D')
        year_angle = 2*np.pi*days/365.2425
        # This is equatorial RA separation, a proxy, not ecliptic elongation.
        relative = np.deg2rad(frame['jpl_ra_deg'] - sun['jpl_ra_deg'])
        model_relative = np.deg2rad(frame['ty_ra_deg'] - sun['ty_ra_deg'])
        print(f'\n{body}: n={len(frame)} train={sum(train)} test={sum(test)}')
        for key in ['dra_deg', 'ddec_deg']:
            y = frame[key]
            c, score = fit_and_validate(design(year_angle), y, train, test)
            c2, _ = fit_and_validate(design(year_angle), y, test, train)
            amp, amp2 = np.hypot(c[1], c[2]), np.hypot(c2[1], c2[2])
            phase = np.degrees(np.arctan2(c[2], c[1]))
            phase2 = np.degrees(np.arctan2(c2[2], c2[1]))
            line = f'  {key}: annual amplitude train/test={amp:.4f}/{amp2:.4f} deg, phases={phase:.1f}/{phase2:.1f} deg; heldout R2={score:.3f}'
            if body != 'sun':
                _, score2 = fit_and_validate(design(relative), y, train, test)
                _, score3 = fit_and_validate(design(model_relative), y, train, test)
                line += f'; Sun-relative RA-phase heldout R2 JPL/model={score2:.3f}/{score3:.3f}'
            print(line)


if __name__ == '__main__': main()
