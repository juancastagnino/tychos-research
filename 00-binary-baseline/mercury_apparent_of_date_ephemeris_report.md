# TYCHOS Mercury Ephemeris Audit

**Model:** TYCHOS mercury / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:50:00.180139+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0142° | 2.5675° | 5.1890° | 8.7583° |
| Declination | 0.2049° | 1.0059° | 1.8691° | 4.1101° |
| Angular separation | 2.1110° | 2.6485° | 5.2873° | 8.8306° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 2.9751° | 0.9412° | 2.9704° |
| 2001 | 2920 | 2.7337° | 0.8834° | 2.7360° |
| 2002 | 2920 | 2.4999° | 0.9364° | 2.5596° |
| 2003 | 2920 | 2.4371° | 1.0380° | 2.5511° |
| 2004 | 2928 | 2.4896° | 1.1307° | 2.6415° |
| 2005 | 2920 | 2.4999° | 1.0931° | 2.6397° |
| 2006 | 2920 | 2.6578° | 0.9843° | 2.7208° |
| 2007 | 2920 | 2.7591° | 0.8858° | 2.7603° |
| 2008 | 2928 | 2.6490° | 0.9023° | 2.6708° |
| 2009 | 2920 | 2.4176° | 0.9724° | 2.5062° |
| 2010 | 2920 | 2.5072° | 1.0940° | 2.6355° |
| 2011 | 2920 | 2.4450° | 1.1280° | 2.6080° |
| 2012 | 2928 | 2.5643° | 1.0536° | 2.6749° |
| 2013 | 2920 | 2.7092° | 0.9333° | 2.7401° |
| 2014 | 2920 | 2.7450° | 0.8804° | 2.7445° |
| 2015 | 2920 | 2.5341° | 0.9280° | 2.5846° |
| 2016 | 2928 | 2.4108° | 1.0196° | 2.5210° |
| 2017 | 2920 | 2.4978° | 1.1281° | 2.6459° |
| 2018 | 2920 | 2.4735° | 1.1063° | 2.6237° |
| 2019 | 2920 | 2.6281° | 1.0049° | 2.7053° |
| 2020 | 2928 | 2.7463° | 0.8950° | 2.7533° |
| 2021 | 2920 | 2.6745° | 0.8961° | 2.6900° |
| 2022 | 2920 | 2.4370° | 0.9607° | 2.5171° |
| 2023 | 2920 | 2.4762° | 1.0766° | 2.6015° |
| 2024 | 2928 | 2.4468° | 1.1323° | 2.6100° |
| 2025 | 2920 | 2.5387° | 1.0714° | 2.6622° |
| 2026 | 1369 | 2.3709° | 0.8828° | 2.4301° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
