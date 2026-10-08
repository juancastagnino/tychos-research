# TYCHOS Saturn Ephemeris Audit

**Model:** TYCHOS saturn / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:51:51.013030+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0812° | 0.6812° | 1.2757° | 1.7177° |
| Declination | -0.0264° | 0.1720° | 0.3128° | 0.4032° |
| Angular separation | 0.5723° | 0.6736° | 1.2116° | 1.6081° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 1.2073° | 0.1706° | 1.1605° |
| 2001 | 2920 | 0.9840° | 0.1101° | 0.9281° |
| 2002 | 2920 | 0.9930° | 0.0705° | 0.9234° |
| 2003 | 2920 | 0.9441° | 0.1038° | 0.8807° |
| 2004 | 2928 | 0.8440° | 0.1559° | 0.8031° |
| 2005 | 2920 | 0.7197° | 0.1859° | 0.7053° |
| 2006 | 2920 | 0.6047° | 0.1907° | 0.6094° |
| 2007 | 2920 | 0.5320° | 0.1852° | 0.5471° |
| 2008 | 2928 | 0.5177° | 0.1873° | 0.5405° |
| 2009 | 2920 | 0.5547° | 0.2029° | 0.5863° |
| 2010 | 2920 | 0.6185° | 0.2219° | 0.6565° |
| 2011 | 2920 | 0.6876° | 0.2300° | 0.7241° |
| 2012 | 2928 | 0.7473° | 0.2180° | 0.7723° |
| 2013 | 2920 | 0.7895° | 0.1837° | 0.7946° |
| 2014 | 2920 | 0.8030° | 0.1296° | 0.7849° |
| 2015 | 2920 | 0.7821° | 0.0690° | 0.7453° |
| 2016 | 2928 | 0.7230° | 0.0596° | 0.6791° |
| 2017 | 2920 | 0.6293° | 0.1155° | 0.5943° |
| 2018 | 2920 | 0.5096° | 0.1685° | 0.4993° |
| 2019 | 2920 | 0.3870° | 0.2015° | 0.4105° |
| 2020 | 2928 | 0.3025° | 0.2109° | 0.3523° |
| 2021 | 2920 | 0.3026° | 0.2013° | 0.3509° |
| 2022 | 2920 | 0.3704° | 0.1836° | 0.4025° |
| 2023 | 2920 | 0.4573° | 0.1717° | 0.4808° |
| 2024 | 2928 | 0.5412° | 0.1746° | 0.5653° |
| 2025 | 2920 | 0.6214° | 0.1898° | 0.6494° |
| 2026 | 1369 | 0.5836° | 0.1774° | 0.6094° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
