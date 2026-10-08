# TYCHOS Moon Ephemeris Audit

**Model:** TYCHOS moon / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:39:42.232066+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.8091° | 2.2237° | 4.2319° | 6.0466° |
| Declination | -0.0172° | 3.5385° | 5.4804° | 6.7145° |
| Angular separation | 3.8520° | 4.1328° | 6.0294° | 7.3710° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 2.5581° | 3.8357° | 4.5749° |
| 2001 | 2920 | 2.6148° | 3.9216° | 4.6648° |
| 2002 | 2920 | 2.7297° | 3.7451° | 4.5714° |
| 2003 | 2920 | 2.5537° | 3.3917° | 4.1910° |
| 2004 | 2928 | 2.1426° | 3.1372° | 3.7586° |
| 2005 | 2920 | 2.0703° | 3.0986° | 3.6686° |
| 2006 | 2920 | 2.1529° | 3.2731° | 3.8425° |
| 2007 | 2920 | 2.0714° | 3.4459° | 3.9612° |
| 2008 | 2928 | 1.7745° | 3.4245° | 3.8255° |
| 2009 | 2920 | 1.8468° | 3.1255° | 3.5923° |
| 2010 | 2920 | 1.9753° | 3.0058° | 3.5398° |
| 2011 | 2920 | 2.0206° | 3.2370° | 3.7652° |
| 2012 | 2928 | 1.8721° | 3.6640° | 4.0865° |
| 2013 | 2920 | 1.8783° | 3.9487° | 4.3499° |
| 2014 | 2920 | 1.9490° | 4.0314° | 4.4451° |
| 2015 | 2920 | 2.0459° | 3.8891° | 4.3542° |
| 2016 | 2928 | 2.1566° | 3.7000° | 4.2472° |
| 2017 | 2920 | 2.2049° | 3.7238° | 4.3008° |
| 2018 | 2920 | 2.4516° | 3.8676° | 4.5460° |
| 2019 | 2920 | 2.6234° | 3.9689° | 4.7066° |
| 2020 | 2928 | 2.7352° | 3.8025° | 4.6266° |
| 2021 | 2920 | 2.4912° | 3.4924° | 4.2451° |
| 2022 | 2920 | 2.3060° | 3.1587° | 3.8685° |
| 2023 | 2920 | 2.1954° | 3.1472° | 3.7722° |
| 2024 | 2928 | 2.2352° | 3.3055° | 3.9146° |
| 2025 | 2920 | 2.0454° | 3.4728° | 3.9773° |
| 2026 | 1369 | 1.7961° | 3.4554° | 3.8617° |

## Interpretation notes

- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- Lunar ecliptic periodic diagnostics are intentionally omitted in this mode.

