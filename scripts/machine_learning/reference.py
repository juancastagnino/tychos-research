"""Coordinate selection shared by single-body and cross-body diagnostics."""
import numpy as np

def reference_mode(config):
    mode = config.get('reference', 'apparent-of-date')
    if mode == 'apparent_of_date':
        mode = 'apparent-of-date'
    if mode != 'apparent-of-date':
        raise ValueError(f'Unsupported JPL reference: {mode}')
    return mode


def coordinates(config, dates, ty, jp):
    mode = reference_mode(config)
    suffix = 'app'
    ty_ra = np.array([ty[d]['ra'] for d in dates])
    ty_dec = np.array([ty[d]['dec'] for d in dates])
    try:
        jp_ra = np.array([jp[d]['ra_' + suffix] for d in dates])
        jp_dec = np.array([jp[d]['dec_' + suffix] for d in dates])
    except KeyError as error:
        raise ValueError(f'Missing coordinates for JPL reference {mode}: {error}') from error
    if not all(np.all(np.isfinite(a)) for a in (ty_ra, ty_dec, jp_ra, jp_dec)):
        raise ValueError('Non-finite reference coordinates')
    return ty_ra, ty_dec, jp_ra, jp_dec


def diagnostic_coordinates(config, ty_ra, ty_dec, jp_ra, jp_dec):
    reference_mode(config)
    return ty_ra, ty_dec, jp_ra, jp_dec


def targets(config):
    reference_mode(config)
    return ('ra', 'declination', 'east', 'north')
