# TYCHOS Mars Ephemeris Audit

**Model:** TYCHOS mars / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:50:56.957742+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.2211° | 0.5525° | 1.1263° | 2.0963° |
| Declination | -0.2613° | 0.3433° | 0.7085° | 1.0739° |
| Angular separation | 0.5262° | 0.6215° | 1.1807° | 2.0801° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.2997° | 0.2830° | 0.4047° |
| 2001 | 2920 | 1.0656° | 0.1935° | 0.9885° |
| 2002 | 2920 | 0.2463° | 0.2677° | 0.3601° |
| 2003 | 2920 | 0.6019° | 0.2535° | 0.6233° |
| 2004 | 2928 | 0.2928° | 0.2600° | 0.3861° |
| 2005 | 2920 | 0.6077° | 0.3920° | 0.7038° |
| 2006 | 2920 | 0.4293° | 0.2737° | 0.4891° |
| 2007 | 2920 | 0.4615° | 0.4499° | 0.6219° |
| 2008 | 2928 | 0.5699° | 0.3600° | 0.6283° |
| 2009 | 2920 | 0.3292° | 0.3597° | 0.4729° |
| 2010 | 2920 | 0.5015° | 0.4321° | 0.6376° |
| 2011 | 2920 | 0.3061° | 0.3091° | 0.4209° |
| 2012 | 2928 | 0.5742° | 0.4334° | 0.6978° |
| 2013 | 2920 | 0.2840° | 0.2972° | 0.4004° |
| 2014 | 2920 | 0.8556° | 0.5020° | 0.9672° |
| 2015 | 2920 | 0.2560° | 0.2894° | 0.3801° |
| 2016 | 2928 | 1.1250° | 0.3377° | 1.1008° |
| 2017 | 2920 | 0.2529° | 0.2748° | 0.3696° |
| 2018 | 2920 | 0.7471° | 0.2368° | 0.7342° |
| 2019 | 2920 | 0.2900° | 0.2609° | 0.3857° |
| 2020 | 2928 | 0.6108° | 0.3513° | 0.6893° |
| 2021 | 2920 | 0.3950° | 0.2629° | 0.4613° |
| 2022 | 2920 | 0.5297° | 0.4807° | 0.6898° |
| 2023 | 2920 | 0.5512° | 0.3182° | 0.5959° |
| 2024 | 2928 | 0.3328° | 0.4121° | 0.5168° |
| 2025 | 2920 | 0.5293° | 0.4238° | 0.6446° |
| 2026 | 1369 | 0.1736° | 0.1399° | 0.2160° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
