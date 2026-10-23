# TYCHOS Mercury Ephemeris Audit

**Model:** TYCHOS mercury / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-23T14:32:52.197561+00:00
- Export configuration: mercury tests vs JPL
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0113° | 2.8112° | 5.6897° | 9.4601° |
| Declination | 0.2450° | 1.0016° | 1.8559° | 4.1496° |
| Angular separation | 2.2828° | 2.8623° | 5.7430° | 9.4815° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 3.2320° | 0.9090° | 3.1911° |
| 2001 | 2920 | 2.9808° | 0.8646° | 2.9524° |
| 2002 | 2920 | 2.7348° | 0.9221° | 2.7636° |
| 2003 | 2920 | 2.6778° | 1.0327° | 2.7595° |
| 2004 | 2928 | 2.7342° | 1.1354° | 2.8555° |
| 2005 | 2920 | 2.7399° | 1.1027° | 2.8535° |
| 2006 | 2920 | 2.9110° | 0.9841° | 2.9455° |
| 2007 | 2920 | 3.0117° | 0.8707° | 2.9826° |
| 2008 | 2928 | 2.8919° | 0.8838° | 2.8825° |
| 2009 | 2920 | 2.6474° | 0.9618° | 2.7051° |
| 2010 | 2920 | 2.7565° | 1.0928° | 2.8520° |
| 2011 | 2920 | 2.6840° | 1.1364° | 2.8188° |
| 2012 | 2928 | 2.8094° | 1.0604° | 2.8934° |
| 2013 | 2920 | 2.9643° | 0.9262° | 2.9655° |
| 2014 | 2920 | 2.9934° | 0.8616° | 2.9621° |
| 2015 | 2920 | 2.7712° | 0.9119° | 2.7905° |
| 2016 | 2928 | 2.6475° | 1.0125° | 2.7255° |
| 2017 | 2920 | 2.7433° | 1.1312° | 2.8601° |
| 2018 | 2920 | 2.7118° | 1.1160° | 2.8355° |
| 2019 | 2920 | 2.8791° | 1.0066° | 2.9282° |
| 2020 | 2928 | 2.9998° | 0.8812° | 2.9764° |
| 2021 | 2920 | 2.9184° | 0.8766° | 2.9026° |
| 2022 | 2920 | 2.6673° | 0.9484° | 2.7165° |
| 2023 | 2920 | 2.7228° | 1.0736° | 2.8151° |
| 2024 | 2928 | 2.6868° | 1.1392° | 2.8207° |
| 2025 | 2920 | 2.7815° | 1.0793° | 2.8784° |
| 2026 | 1369 | 2.6070° | 0.8964° | 2.6437° |

## Interpretation notes

- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
- Compare RA, declination and angular separation using the same epochs and declared export settings.
- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.

