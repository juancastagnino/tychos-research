# TYCHOS Moon Ephemeris Audit

**Model:** TYCHOS moon / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:49:40.141428+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.2439° | 1.1188° | 2.1324° | 3.3577° |
| Declination | -0.0120° | 0.3703° | 0.7925° | 1.3184° |
| Angular separation | 0.9495° | 1.1271° | 2.1214° | 3.1803° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 1.1361° | 0.3278° | 1.1393° |
| 2001 | 2920 | 1.1064° | 0.3589° | 1.1184° |
| 2002 | 2920 | 1.1150° | 0.3877° | 1.1313° |
| 2003 | 2920 | 1.1127° | 0.3942° | 1.1247° |
| 2004 | 2928 | 1.1102° | 0.3970° | 1.1132° |
| 2005 | 2920 | 1.1047° | 0.4224° | 1.1129° |
| 2006 | 2920 | 1.1247° | 0.4350° | 1.1381° |
| 2007 | 2920 | 1.1011° | 0.4152° | 1.1114° |
| 2008 | 2928 | 1.1033° | 0.3922° | 1.1055° |
| 2009 | 2920 | 1.1046° | 0.3888° | 1.1069° |
| 2010 | 2920 | 1.1370° | 0.3872° | 1.1457° |
| 2011 | 2920 | 1.1244° | 0.3586° | 1.1347° |
| 2012 | 2928 | 1.1293° | 0.3315° | 1.1402° |
| 2013 | 2920 | 1.1197° | 0.3136° | 1.1296° |
| 2014 | 2920 | 1.1327° | 0.2950° | 1.1400° |
| 2015 | 2920 | 1.1306° | 0.2805° | 1.1359° |
| 2016 | 2928 | 1.1501° | 0.2638° | 1.1495° |
| 2017 | 2920 | 1.1404° | 0.2852° | 1.1410° |
| 2018 | 2920 | 1.1461° | 0.3010° | 1.1459° |
| 2019 | 2920 | 1.1011° | 0.3414° | 1.1122° |
| 2020 | 2928 | 1.1100° | 0.3582° | 1.1211° |
| 2021 | 2920 | 1.1134° | 0.3926° | 1.1278° |
| 2022 | 2920 | 1.1335° | 0.3949° | 1.1380° |
| 2023 | 2920 | 1.1012° | 0.4160° | 1.1104° |
| 2024 | 2928 | 1.1048° | 0.4304° | 1.1203° |
| 2025 | 2920 | 1.1190° | 0.4269° | 1.1318° |
| 2026 | 1369 | 1.0801° | 0.4152° | 1.0884° |

## Interpretation notes

- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- Lunar ecliptic periodic diagnostics are intentionally omitted in this mode.

