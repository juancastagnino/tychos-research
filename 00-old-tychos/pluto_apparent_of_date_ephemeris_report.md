# TYCHOS Pluto Ephemeris Audit

**Model:** TYCHOS pluto / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:46.912810+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -4.0676° | 4.8730° | 7.8607° | 8.3280° |
| Declination | 2.6945° | 2.7159° | 3.1042° | 3.1522° |
| Angular separation | 4.9537° | 5.3102° | 7.6760° | 8.0669° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.7708° | 1.7893° | 1.9431° |
| 2001 | 2920 | 0.5287° | 1.9380° | 2.0062° |
| 2002 | 2920 | 0.1810° | 2.1000° | 2.1074° |
| 2003 | 2920 | 0.3591° | 2.2509° | 2.2780° |
| 2004 | 2928 | 0.7555° | 2.3899° | 2.5003° |
| 2005 | 2920 | 1.1659° | 2.5167° | 2.7591° |
| 2006 | 2920 | 1.5778° | 2.6298° | 3.0406° |
| 2007 | 2920 | 1.9888° | 2.7292° | 3.3359° |
| 2008 | 2928 | 2.3967° | 2.8144° | 3.6380° |
| 2009 | 2920 | 2.7996° | 2.8862° | 3.9420° |
| 2010 | 2920 | 3.1942° | 2.9439° | 4.2425° |
| 2011 | 2920 | 3.5796° | 2.9881° | 4.5371° |
| 2012 | 2928 | 3.9556° | 3.0193° | 4.8241° |
| 2013 | 2920 | 4.3223° | 3.0384° | 5.1036° |
| 2014 | 2920 | 4.6790° | 3.0451° | 5.3737° |
| 2015 | 2920 | 5.0271° | 3.0399° | 5.6356° |
| 2016 | 2928 | 5.3669° | 3.0227° | 5.8892° |
| 2017 | 2920 | 5.6991° | 2.9946° | 6.1356° |
| 2018 | 2920 | 6.0217° | 2.9552° | 6.3730° |
| 2019 | 2920 | 6.3348° | 2.9051° | 6.6018° |
| 2020 | 2928 | 6.6374° | 2.8445° | 6.8214° |
| 2021 | 2920 | 6.9289° | 2.7748° | 7.0318° |
| 2022 | 2920 | 7.2058° | 2.6962° | 7.2304° |
| 2023 | 2920 | 7.4679° | 2.6095° | 7.4172° |
| 2024 | 2928 | 7.7140° | 2.5153° | 7.5915° |
| 2025 | 2920 | 7.9453° | 2.4147° | 7.7546° |
| 2026 | 1369 | 8.0102° | 2.2725° | 7.7762° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
