# TYCHOS Neptune Ephemeris Audit

**Model:** TYCHOS neptune / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:40.151544+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.0310° | 0.0489° | 0.0786° | 0.0893° |
| Declination | -0.0784° | 0.0965° | 0.1758° | 0.1985° |
| Angular separation | 0.0995° | 0.1075° | 0.1829° | 0.2151° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.0481° | 0.0039° | 0.0457° |
| 2001 | 2920 | 0.0523° | 0.0041° | 0.0498° |
| 2002 | 2920 | 0.0583° | 0.0055° | 0.0558° |
| 2003 | 2920 | 0.0639° | 0.0087° | 0.0616° |
| 2004 | 2928 | 0.0681° | 0.0127° | 0.0665° |
| 2005 | 2920 | 0.0703° | 0.0176° | 0.0698° |
| 2006 | 2920 | 0.0702° | 0.0234° | 0.0715° |
| 2007 | 2920 | 0.0676° | 0.0302° | 0.0720° |
| 2008 | 2928 | 0.0628° | 0.0380° | 0.0718° |
| 2009 | 2920 | 0.0568° | 0.0464° | 0.0721° |
| 2010 | 2920 | 0.0503° | 0.0552° | 0.0738° |
| 2011 | 2920 | 0.0446° | 0.0638° | 0.0773° |
| 2012 | 2928 | 0.0408° | 0.0717° | 0.0821° |
| 2013 | 2920 | 0.0389° | 0.0788° | 0.0875° |
| 2014 | 2920 | 0.0386° | 0.0850° | 0.0931° |
| 2015 | 2920 | 0.0389° | 0.0907° | 0.0985° |
| 2016 | 2928 | 0.0387° | 0.0963° | 0.1037° |
| 2017 | 2920 | 0.0372° | 0.1023° | 0.1088° |
| 2018 | 2920 | 0.0337° | 0.1090° | 0.1140° |
| 2019 | 2920 | 0.0275° | 0.1169° | 0.1200° |
| 2020 | 2928 | 0.0193° | 0.1259° | 0.1273° |
| 2021 | 2920 | 0.0125° | 0.1361° | 0.1367° |
| 2022 | 2920 | 0.0175° | 0.1471° | 0.1481° |
| 2023 | 2920 | 0.0305° | 0.1584° | 0.1613° |
| 2024 | 2928 | 0.0446° | 0.1694° | 0.1751° |
| 2025 | 2920 | 0.0579° | 0.1795° | 0.1886° |
| 2026 | 1369 | 0.0627° | 0.1795° | 0.1902° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
