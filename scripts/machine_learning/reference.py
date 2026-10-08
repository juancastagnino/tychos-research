"""Coordinate selection shared by single-body and cross-body diagnostics."""
import numpy as np

from analyze_ephemerides import equatorial_to_ecliptic


def reference_mode(config):
    mode = config.get('reference', 'icrf')
    if mode == 'apparent_of_date':
        mode = 'apparent-of-date'
    if mode not in ('icrf', 'apparent-of-date'):
        raise ValueError(f'Unsupported JPL reference: {mode}')
    return mode


def coordinates(config, dates, ty, jp):
    mode = reference_mode(config)
    suffix = 'app' if mode == 'apparent-of-date' else 'icrf'
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
    if reference_mode(config) == 'apparent-of-date':
        return ty_ra, ty_dec, jp_ra, jp_dec
    ty_lon, ty_lat = equatorial_to_ecliptic(ty_ra, ty_dec)
    jp_lon, jp_lat = equatorial_to_ecliptic(jp_ra, jp_dec)
    return ty_lon, ty_lat, jp_lon, jp_lat


def targets(config):
    if reference_mode(config) == 'apparent-of-date':
        return ('ra', 'declination', 'east', 'north')
    return ('longitude', 'latitude', 'east', 'north')
