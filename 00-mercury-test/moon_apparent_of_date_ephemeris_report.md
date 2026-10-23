# TYCHOS Moon Ephemeris Audit

**Model:** TYCHOS moon / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-23T10:26:33.096748+00:00
- Export configuration: mercury old hierarchy  vs JPL
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0309° | 1.6344° | 3.0724° | 4.1750° |
| Declination | -0.0060° | 0.5468° | 1.1207° | 1.7827° |
| Angular separation | 1.3766° | 1.6468° | 3.0269° | 3.8313° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 1.5415° | 0.5007° | 1.5778° |
| 2001 | 2920 | 1.5445° | 0.5474° | 1.5911° |
| 2002 | 2920 | 1.7263° | 0.5412° | 1.7191° |
| 2003 | 2920 | 1.7429° | 0.5417° | 1.7105° |
| 2004 | 2928 | 1.5542° | 0.5988° | 1.5798° |
| 2005 | 2920 | 1.5040° | 0.6918° | 1.5919° |
| 2006 | 2920 | 1.6690° | 0.6440° | 1.6830° |
| 2007 | 2920 | 1.7709° | 0.5992° | 1.7387° |
| 2008 | 2928 | 1.6271° | 0.6122° | 1.6461° |
| 2009 | 2920 | 1.4726° | 0.6359° | 1.5495° |
| 2010 | 2920 | 1.6052° | 0.5680° | 1.6278° |
| 2011 | 2920 | 1.7504° | 0.4851° | 1.7266° |
| 2012 | 2928 | 1.6819° | 0.4604° | 1.6794° |
| 2013 | 2920 | 1.5407° | 0.4718° | 1.5762° |
| 2014 | 2920 | 1.5763° | 0.4360° | 1.6025° |
| 2015 | 2920 | 1.6677° | 0.3729° | 1.6619° |
| 2016 | 2928 | 1.7324° | 0.3437° | 1.7101° |
| 2017 | 2920 | 1.6229° | 0.3970° | 1.6210° |
| 2018 | 2920 | 1.5242° | 0.4528° | 1.5532° |
| 2019 | 2920 | 1.5720° | 0.4956° | 1.5976° |
| 2020 | 2928 | 1.7557° | 0.5081° | 1.7369° |
| 2021 | 2920 | 1.6932° | 0.5313° | 1.6722° |
| 2022 | 2920 | 1.5459° | 0.6115° | 1.5917° |
| 2023 | 2920 | 1.5164° | 0.6585° | 1.5846° |
| 2024 | 2928 | 1.7162° | 0.6423° | 1.7158° |
| 2025 | 2920 | 1.7484° | 0.6067° | 1.7218° |
| 2026 | 1369 | 1.5934° | 0.6353° | 1.6199° |

## Interpretation notes

- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
- Compare RA, declination and angular separation using the same epochs and declared export settings.
- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.

