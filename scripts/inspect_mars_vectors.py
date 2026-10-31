"""Regress Mars angular residuals against precise model vector phases, diagnostically."""
import argparse
from pathlib import Path
import numpy as np
from inspect_shared_residuals import design, fit_and_validate


def main():
    p = argparse.ArgumentParser()
    p.add_argument('folder', type=Path)
    args = p.parse_args()
    def read(name):
        return np.genfromtxt(args.folder / name, delimiter=',', names=True, dtype=None, encoding='utf-8')
    vectors = read('sun-mars-binary.csv')
    residuals = read('mars_apparent_of_date_residuals.csv')
    dates = np.char.add(np.char.add(vectors['date'], ' '), vectors['time'])
    if not np.array_equal(dates, residuals['date']):
        raise ValueError('Vector and residual timestamps differ')
    split = residuals['date'].astype('datetime64[s]') < np.datetime64('2013-06-21')
    names = set(vectors.dtype.names or [])
    # Earlier diagnostics exported Sun→Mars directly.  The current TYCHOS
    # binary CSV exports both world positions, which is preferable: derive the
    # same vector rather than requiring a legacy-only column.
    if all(f'sun_to_mars_{axis}' in names for axis in 'xyz'):
        sm = np.column_stack([vectors[f'sun_to_mars_{axis}'] for axis in 'xyz'])
    elif all(f'{body}_world_{axis}' in names for body in ('sun', 'mars') for axis in 'xyz'):
        sm = np.column_stack([
            vectors[f'mars_world_{axis}'] - vectors[f'sun_world_{axis}']
            for axis in 'xyz'
        ])
    else:
        raise ValueError('CSV has neither Sun→Mars vector nor Sun/Mars world positions')

    es = np.column_stack([vectors[f'earth_sun_d{axis}'] for axis in 'xyz'])
    sm_length = np.linalg.norm(sm, axis=1)
    es_length = np.linalg.norm(es, axis=1)
    print(f'n={len(sm)}; Sun-Mars range={sm_length.min():.6f}–{sm_length.max():.6f} model units')
    sun_angle = np.arctan2(-es[:,2], es[:,0])
    mars_angle = np.arctan2(-sm[:,2], sm[:,0])
    features = {'Sun-Mars world-XZ angle': mars_angle,
                'Sun-Mars relative to Earth-Sun XZ angle': mars_angle - sun_angle}
    for label, angle in features.items():
        for metric in ['dra_deg', 'ddec_deg']:
            _, score = fit_and_validate(design(angle), residuals[metric], split, ~split)
            print(f'{label}; {metric}: heldout R2={score:.4f}')
    print(f'Earth-Sun range={es_length.min():.6f}–{es_length.max():.6f} model units')
    if 'mars_orbit_normal_x' in vectors.dtype.names:
        normal = np.column_stack([vectors[f'mars_orbit_normal_{a}'] for a in 'xyz'])
        def world_direction(prefix):
            ra = np.deg2rad(residuals[f'{prefix}_ra_deg'])
            dec = np.deg2rad(residuals[f'{prefix}_dec_deg'])
            local = np.column_stack([np.cos(dec)*np.sin(ra), np.sin(dec), np.cos(dec)*np.cos(ra)])
            axes = np.stack([np.column_stack([vectors[f'earth_equatorial_axis_{i}_{j}'] for j in 'xyz']) for i in 'xyz'], axis=1)
            return np.einsum('ni,nij->nj', local, axes)
        model = world_direction('ty')
        ref = world_direction('jpl')
        projected = normal - np.sum(normal*model, axis=1)[:, None]*model
        lengths = np.linalg.norm(projected, axis=1)
        valid = lengths > 0.1
        projected[valid] /= lengths[valid, None]
        inplane = np.cross(projected, model)
        displacement = ref - model
        phase = mars_angle - sun_angle
        for name, axis in [('projected-plane-normal', projected), ('in-plane sky direction', inplane)]:
            y = np.rad2deg(np.sum(displacement*axis, axis=1))
            train, test = split & valid, ~split & valid
            coef, score = fit_and_validate(design(phase), y, train, test)
            first_amplitude = np.hypot(coef[1], coef[2])
            first_phase = np.rad2deg(np.arctan2(coef[2], coef[1]))
            second_amplitude = np.hypot(coef[3], coef[4])
            second_phase = np.rad2deg(np.arctan2(coef[4], coef[3]))
            print(f'{name}: validation RMS={np.sqrt(np.mean(y[test]**2)):.4f} deg; heldout R2={score:.4f}; n={sum(test)}')
            print(f'  fitted Sun-Mars phase: offset={coef[0]:.4f} deg; first harmonic={first_amplitude:.4f} deg at {first_phase:.1f} deg; second harmonic={second_amplitude:.4f} deg at {second_phase:.1f} deg')
        print(f'excluded ill-conditioned projections={sum(~valid)}')


if __name__ == '__main__': main()
