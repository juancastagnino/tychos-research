# TYCHOS Mercury Ephemeris Audit

**Model:** TYCHOS mercury / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-23T12:35:07.856422+00:00
- Export configuration: paired radial 3D  vs JPL
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0139° | 2.2435° | 4.7339° | 6.8843° |
| Declination | 0.3646° | 1.0019° | 1.8897° | 4.1082° |
| Angular separation | 1.9296° | 2.3852° | 4.9627° | 7.7149° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 2.3764° | 0.9272° | 2.4445° |
| 2001 | 2920 | 2.2706° | 0.9231° | 2.3661° |
| 2002 | 2920 | 2.1267° | 0.9817° | 2.2741° |
| 2003 | 2920 | 2.1562° | 1.0629° | 2.3402° |
| 2004 | 2928 | 2.2295° | 1.0947° | 2.4226° |
| 2005 | 2920 | 2.3095° | 1.0315° | 2.4612° |
| 2006 | 2920 | 2.3223° | 0.9453° | 2.4293° |
| 2007 | 2920 | 2.3057° | 0.9048° | 2.3905° |
| 2008 | 2928 | 2.2068° | 0.9473° | 2.3230° |
| 2009 | 2920 | 2.1168° | 1.0147° | 2.2829° |
| 2010 | 2920 | 2.2047° | 1.0943° | 2.3978° |
| 2011 | 2920 | 2.2523° | 1.0751° | 2.4345° |
| 2012 | 2928 | 2.3278° | 0.9948° | 2.4584° |
| 2013 | 2920 | 2.3142° | 0.9181° | 2.4078° |
| 2014 | 2920 | 2.2851° | 0.9174° | 2.3763° |
| 2015 | 2920 | 2.1425° | 0.9747° | 2.2835° |
| 2016 | 2928 | 2.1387° | 1.0518° | 2.3199° |
| 2017 | 2920 | 2.2287° | 1.1014° | 2.4243° |
| 2018 | 2920 | 2.2988° | 1.0460° | 2.4595° |
| 2019 | 2920 | 2.3246° | 0.9589° | 2.4379° |
| 2020 | 2928 | 2.3081° | 0.9056° | 2.3938° |
| 2021 | 2920 | 2.2307° | 0.9415° | 2.3406° |
| 2022 | 2920 | 2.1171° | 1.0051° | 2.2783° |
| 2023 | 2920 | 2.1904° | 1.0875° | 2.3820° |
| 2024 | 2928 | 2.2429° | 1.0852° | 2.4310° |
| 2025 | 2920 | 2.3304° | 1.0115° | 2.4689° |
| 2026 | 1369 | 2.2503° | 0.9045° | 2.3721° |

## Interpretation notes

- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
- Compare RA, declination and angular separation using the same epochs and declared export settings.
- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.

