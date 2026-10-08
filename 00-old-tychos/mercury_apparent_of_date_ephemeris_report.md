# TYCHOS Mercury Ephemeris Audit

**Model:** TYCHOS mercury / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:39:59.640269+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0792° | 2.2740° | 4.4550° | 8.1219° |
| Declination | 0.3639° | 1.4313° | 2.5494° | 4.6915° |
| Angular separation | 2.1619° | 2.5973° | 4.8288° | 8.3176° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 2.7182° | 1.4105° | 2.9322° |
| 2001 | 2920 | 2.4663° | 1.3669° | 2.7013° |
| 2002 | 2920 | 2.3014° | 1.3375° | 2.5623° |
| 2003 | 2920 | 2.2015° | 1.4114° | 2.5324° |
| 2004 | 2928 | 2.1739° | 1.4970° | 2.5666° |
| 2005 | 2920 | 2.1441° | 1.5042° | 2.5525° |
| 2006 | 2920 | 2.2835° | 1.4690° | 2.6291° |
| 2007 | 2920 | 2.4431° | 1.3983° | 2.7014° |
| 2008 | 2928 | 2.4148° | 1.3496° | 2.6531° |
| 2009 | 2920 | 2.2274° | 1.3531° | 2.5166° |
| 2010 | 2920 | 2.2228° | 1.4636° | 2.5802° |
| 2011 | 2920 | 2.1153° | 1.5038° | 2.5304° |
| 2012 | 2928 | 2.1921° | 1.4959° | 2.5814° |
| 2013 | 2920 | 2.3513° | 1.4402° | 2.6592° |
| 2014 | 2920 | 2.4640° | 1.3753° | 2.7036° |
| 2015 | 2920 | 2.3272° | 1.3401° | 2.5825° |
| 2016 | 2928 | 2.1911° | 1.3942° | 2.5139° |
| 2017 | 2920 | 2.1887° | 1.4936° | 2.5746° |
| 2018 | 2920 | 2.1242° | 1.5062° | 2.5392° |
| 2019 | 2920 | 2.2518° | 1.4793° | 2.6128° |
| 2020 | 2928 | 2.4167° | 1.4101° | 2.6882° |
| 2021 | 2920 | 2.4284° | 1.3575° | 2.6671° |
| 2022 | 2920 | 2.2463° | 1.3469° | 2.5265° |
| 2023 | 2920 | 2.2078° | 1.4480° | 2.5591° |
| 2024 | 2928 | 2.1217° | 1.5027° | 2.5334° |
| 2025 | 2920 | 2.1698° | 1.5028° | 2.5698° |
| 2026 | 1369 | 1.9173° | 1.4578° | 2.3472° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
