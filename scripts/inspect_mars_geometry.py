"""Diagnose Mars angular residuals relative to the modeled Sun direction."""
import argparse
from pathlib import Path
import numpy as np
from inspect_shared_residuals import design, fit_and_validate


def vectors(ra, dec):
    a, d = np.deg2rad(ra), np.deg2rad(dec)
    return np.column_stack((np.cos(d)*np.cos(a), np.cos(d)*np.sin(a), np.sin(d)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('folder', type=Path)
    p.add_argument('--split', default='1913-01-01', help='UTC split date')
    args = p.parse_args()
    folder = args.folder
    def load(body):
        return np.genfromtxt(folder / f'{body}_apparent_of_date_residuals.csv', delimiter=',', names=True, dtype=None, encoding='utf-8')
    m, s = load('mars'), load('sun')
    if not np.array_equal(m['date'], s['date']): raise ValueError('Dates do not align')
    model = vectors(m['ty_ra_deg'], m['ty_dec_deg'])
    reference = vectors(m['jpl_ra_deg'], m['jpl_dec_deg'])
    sun = vectors(s['ty_ra_deg'], s['ty_dec_deg'])
    # Difference in the tangent plane at modeled Mars; to-Sun basis is ill-defined
    # at conjunction and opposition, so exclude the closest 5 degrees.
    projection = np.sum(sun*model, axis=1)
    tangent = sun - projection[:, None]*model
    norm = np.linalg.norm(tangent, axis=1)
    valid = norm > np.sin(np.deg2rad(5))
    tangent[valid] /= norm[valid, None]
    normal = np.cross(model, tangent)
    residual = reference - model
    along = np.rad2deg(np.sum(residual*tangent, axis=1))
    across = np.rad2deg(np.sum(residual*normal, axis=1))
    date = m['date'].astype('datetime64[s]')
    train = (date < np.datetime64(args.split)) & valid
    test = (date >= np.datetime64(args.split)) & valid
    if not np.any(train) or not np.any(test): raise ValueError('Split must have samples on both sides')
    # Signed RA separation is only a direction proxy, not the 3D Sun-Mars vector.
    angle = np.deg2rad(m['ty_ra_deg']-s['ty_ra_deg'])
    for label, y in [('toward Sun', along), ('perpendicular to Sun direction', across)]:
        _, score = fit_and_validate(design(angle), y, train, test)
        print(f'{label}: test RMS={np.sqrt(np.mean(y[test]**2)):.4f} deg; heldout R2={score:.4f}; samples={sum(test)}')
    print(f'excluded near conjunction/opposition: {sum(~valid)} of {len(m)}')


if __name__ == '__main__': main()
