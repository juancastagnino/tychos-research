# TYCHOS Mars Ephemeris Audit

**Model:** TYCHOS mars / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:13.459212+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.1036° | 0.5078° | 1.0553° | 1.9279° |
| Declination | -0.2854° | 0.4423° | 0.9229° | 1.4801° |
| Angular separation | 0.5529° | 0.6490° | 1.2395° | 2.1091° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.3163° | 0.4187° | 0.5191° |
| 2001 | 2920 | 0.9978° | 0.3548° | 0.9765° |
| 2002 | 2920 | 0.2021° | 0.3046° | 0.3625° |
| 2003 | 2920 | 0.6240° | 0.2224° | 0.6251° |
| 2004 | 2928 | 0.2180° | 0.3100° | 0.3752° |
| 2005 | 2920 | 0.5100° | 0.3557° | 0.6023° |
| 2006 | 2920 | 0.3564° | 0.3448° | 0.4816° |
| 2007 | 2920 | 0.4339° | 0.4681° | 0.6175° |
| 2008 | 2928 | 0.5284° | 0.4695° | 0.6694° |
| 2009 | 2920 | 0.3130° | 0.4371° | 0.5255° |
| 2010 | 2920 | 0.4525° | 0.6535° | 0.7782° |
| 2011 | 2920 | 0.2893° | 0.3849° | 0.4706° |
| 2012 | 2928 | 0.5154° | 0.7527° | 0.8981° |
| 2013 | 2920 | 0.2711° | 0.3512° | 0.4355° |
| 2014 | 2920 | 0.8107° | 0.8190° | 1.1338° |
| 2015 | 2920 | 0.2409° | 0.3228° | 0.3979° |
| 2016 | 2928 | 1.0701° | 0.5675° | 1.1476° |
| 2017 | 2920 | 0.2157° | 0.3035° | 0.3692° |
| 2018 | 2920 | 0.6670° | 0.2151° | 0.6553° |
| 2019 | 2920 | 0.2180° | 0.3005° | 0.3680° |
| 2020 | 2928 | 0.5271° | 0.3241° | 0.5982° |
| 2021 | 2920 | 0.3152° | 0.3206° | 0.4405° |
| 2022 | 2920 | 0.4736° | 0.4614° | 0.6385° |
| 2023 | 2920 | 0.4964° | 0.3995° | 0.6045° |
| 2024 | 2928 | 0.3120° | 0.4724° | 0.5551° |
| 2025 | 2920 | 0.4927° | 0.5900° | 0.7431° |
| 2026 | 1369 | 0.1424° | 0.1354° | 0.1933° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
