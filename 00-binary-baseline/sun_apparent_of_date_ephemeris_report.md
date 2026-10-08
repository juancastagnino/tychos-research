# TYCHOS Sun Ephemeris Audit

**Model:** TYCHOS sun / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:49:49.990213+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.0095° | 0.0547° | 0.0911° | 0.1062° |
| Declination | 0.0039° | 0.0141° | 0.0257° | 0.0305° |
| Angular separation | 0.0485° | 0.0536° | 0.0867° | 0.1001° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.0419° | 0.0121° | 0.0408° |
| 2001 | 2920 | 0.0516° | 0.0120° | 0.0504° |
| 2002 | 2920 | 0.0521° | 0.0122° | 0.0509° |
| 2003 | 2920 | 0.0520° | 0.0126° | 0.0508° |
| 2004 | 2928 | 0.0511° | 0.0128° | 0.0500° |
| 2005 | 2920 | 0.0498° | 0.0128° | 0.0489° |
| 2006 | 2920 | 0.0521° | 0.0139° | 0.0512° |
| 2007 | 2920 | 0.0523° | 0.0141° | 0.0513° |
| 2008 | 2928 | 0.0512° | 0.0141° | 0.0503° |
| 2009 | 2920 | 0.0524° | 0.0149° | 0.0517° |
| 2010 | 2920 | 0.0539° | 0.0150° | 0.0531° |
| 2011 | 2920 | 0.0547° | 0.0151° | 0.0538° |
| 2012 | 2928 | 0.0535° | 0.0147° | 0.0526° |
| 2013 | 2920 | 0.0525° | 0.0143° | 0.0516° |
| 2014 | 2920 | 0.0552° | 0.0148° | 0.0542° |
| 2015 | 2920 | 0.0552° | 0.0144° | 0.0541° |
| 2016 | 2928 | 0.0539° | 0.0136° | 0.0527° |
| 2017 | 2920 | 0.0545° | 0.0140° | 0.0534° |
| 2018 | 2920 | 0.0558° | 0.0139° | 0.0545° |
| 2019 | 2920 | 0.0571° | 0.0141° | 0.0557° |
| 2020 | 2928 | 0.0571° | 0.0143° | 0.0557° |
| 2021 | 2920 | 0.0575° | 0.0143° | 0.0561° |
| 2022 | 2920 | 0.0611° | 0.0155° | 0.0597° |
| 2023 | 2920 | 0.0610° | 0.0155° | 0.0597° |
| 2024 | 2928 | 0.0591° | 0.0153° | 0.0578° |
| 2025 | 2920 | 0.0589° | 0.0161° | 0.0580° |
| 2026 | 1369 | 0.0659° | 0.0133° | 0.0641° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
