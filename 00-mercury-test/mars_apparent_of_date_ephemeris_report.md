# TYCHOS Mars Ephemeris Audit

**Model:** TYCHOS mars / True-of-date apparent

## Dataset

- Samples: **37985**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **6.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-23T02:08:11.810656+00:00
- Export configuration: mars sun moon - new mars  vs JPL
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0012° | 0.4714° | 1.0036° | 1.4939° |
| Declination | -0.0662° | 0.2557° | 0.4375° | 0.7943° |
| Angular separation | 0.4429° | 0.5146° | 1.0281° | 1.4244° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 776 | 0.3367° | 0.1833° | 0.3801° |
| 2001 | 1460 | 0.8922° | 0.1470° | 0.8391° |
| 2002 | 1460 | 0.2772° | 0.1953° | 0.3339° |
| 2003 | 1460 | 0.6798° | 0.3490° | 0.7295° |
| 2004 | 1464 | 0.2966° | 0.1570° | 0.3261° |
| 2005 | 1460 | 0.5378° | 0.2969° | 0.5961° |
| 2006 | 1460 | 0.3284° | 0.1914° | 0.3643° |
| 2007 | 1460 | 0.3845° | 0.2019° | 0.4152° |
| 2008 | 1464 | 0.3275° | 0.2568° | 0.3942° |
| 2009 | 1460 | 0.2873° | 0.2335° | 0.3579° |
| 2010 | 1460 | 0.2900° | 0.3188° | 0.4188° |
| 2011 | 1460 | 0.2394° | 0.2679° | 0.3527° |
| 2012 | 1464 | 0.4537° | 0.3726° | 0.5720° |
| 2013 | 1460 | 0.2304° | 0.2849° | 0.3635° |
| 2014 | 1460 | 0.7315° | 0.3528° | 0.7952° |
| 2015 | 1460 | 0.2477° | 0.2711° | 0.3657° |
| 2016 | 1464 | 0.9265° | 0.1689° | 0.8893° |
| 2017 | 1460 | 0.2808° | 0.2224° | 0.3545° |
| 2018 | 1460 | 0.7354° | 0.3265° | 0.7576° |
| 2019 | 1460 | 0.3030° | 0.1650° | 0.3372° |
| 2020 | 1464 | 0.5910° | 0.3375° | 0.6628° |
| 2021 | 1460 | 0.3325° | 0.1617° | 0.3565° |
| 2022 | 1460 | 0.4453° | 0.2060° | 0.4692° |
| 2023 | 1460 | 0.3570° | 0.2166° | 0.3934° |
| 2024 | 1464 | 0.3343° | 0.2082° | 0.3773° |
| 2025 | 1460 | 0.2876° | 0.2784° | 0.3858° |
| 2026 | 685 | 0.1679° | 0.2766° | 0.3197° |

## Interpretation notes

- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
- Compare RA, declination and angular separation using the same epochs and declared export settings.
- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.

