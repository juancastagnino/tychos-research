# TYCHOS Moon Ephemeris Audit

**Model:** TYCHOS moon / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-23T14:32:40.650947+00:00
- Export configuration: mercury tests vs JPL
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.2299° | 0.3225° | 0.6054° | 0.9525° |
| Declination | -0.0015° | 0.2070° | 0.4018° | 0.7318° |
| Angular separation | 0.3351° | 0.3717° | 0.6208° | 0.8875° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.3787° | 0.1541° | 0.3940° |
| 2001 | 2920 | 0.3006° | 0.1804° | 0.3372° |
| 2002 | 2920 | 0.3129° | 0.2013° | 0.3601° |
| 2003 | 2920 | 0.3276° | 0.2018° | 0.3746° |
| 2004 | 2928 | 0.3277° | 0.2051° | 0.3725° |
| 2005 | 2920 | 0.3001° | 0.2408° | 0.3683° |
| 2006 | 2920 | 0.3157° | 0.2558° | 0.3920° |
| 2007 | 2920 | 0.3552° | 0.2302° | 0.4113° |
| 2008 | 2928 | 0.3574° | 0.2185° | 0.4050° |
| 2009 | 2920 | 0.3204° | 0.2458° | 0.3887° |
| 2010 | 2920 | 0.3137° | 0.2472° | 0.3879° |
| 2011 | 2920 | 0.3431° | 0.2065° | 0.3917° |
| 2012 | 2928 | 0.3426° | 0.1800° | 0.3792° |
| 2013 | 2920 | 0.3067° | 0.1943° | 0.3543° |
| 2014 | 2920 | 0.2971° | 0.1812° | 0.3397° |
| 2015 | 2920 | 0.3192° | 0.1435° | 0.3428° |
| 2016 | 2928 | 0.3302° | 0.1377° | 0.3520° |
| 2017 | 2920 | 0.3141° | 0.1493° | 0.3406° |
| 2018 | 2920 | 0.3133° | 0.1513° | 0.3369° |
| 2019 | 2920 | 0.2999° | 0.1703° | 0.3329° |
| 2020 | 2928 | 0.3162° | 0.1968° | 0.3621° |
| 2021 | 2920 | 0.3269° | 0.2016° | 0.3744° |
| 2022 | 2920 | 0.3236° | 0.2097° | 0.3710° |
| 2023 | 2920 | 0.2971° | 0.2507° | 0.3732° |
| 2024 | 2928 | 0.3292° | 0.2580° | 0.4043° |
| 2025 | 2920 | 0.3615° | 0.2389° | 0.4214° |
| 2026 | 1369 | 0.2339° | 0.2572° | 0.3420° |

## Interpretation notes

- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
- Compare RA, declination and angular separation using the same epochs and declared export settings.
- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.

