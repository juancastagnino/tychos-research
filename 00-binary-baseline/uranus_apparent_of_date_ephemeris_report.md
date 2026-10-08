# TYCHOS Uranus Ephemeris Audit

**Model:** TYCHOS uranus / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:52:18.255209+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.0258° | 0.1520° | 0.2598° | 0.2896° |
| Declination | 0.0303° | 0.0540° | 0.1018° | 0.1125° |
| Angular separation | 0.1435° | 0.1572° | 0.2539° | 0.2804° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.1568° | 0.0805° | 0.1710° |
| 2001 | 2920 | 0.1919° | 0.0652° | 0.1970° |
| 2002 | 2920 | 0.1830° | 0.0648° | 0.1897° |
| 2003 | 2920 | 0.1712° | 0.0652° | 0.1799° |
| 2004 | 2928 | 0.1573° | 0.0659° | 0.1683° |
| 2005 | 2920 | 0.1434° | 0.0663° | 0.1565° |
| 2006 | 2920 | 0.1296° | 0.0664° | 0.1447° |
| 2007 | 2920 | 0.1171° | 0.0658° | 0.1338° |
| 2008 | 2928 | 0.1061° | 0.0645° | 0.1239° |
| 2009 | 2920 | 0.0967° | 0.0622° | 0.1150° |
| 2010 | 2920 | 0.0886° | 0.0596° | 0.1068° |
| 2011 | 2920 | 0.0819° | 0.0567° | 0.0995° |
| 2012 | 2928 | 0.0766° | 0.0542° | 0.0938° |
| 2013 | 2920 | 0.0744° | 0.0518° | 0.0906° |
| 2014 | 2920 | 0.0779° | 0.0500° | 0.0924° |
| 2015 | 2920 | 0.0882° | 0.0482° | 0.1002° |
| 2016 | 2928 | 0.1050° | 0.0463° | 0.1140° |
| 2017 | 2920 | 0.1248° | 0.0432° | 0.1307° |
| 2018 | 2920 | 0.1461° | 0.0389° | 0.1490° |
| 2019 | 2920 | 0.1664° | 0.0331° | 0.1663° |
| 2020 | 2928 | 0.1846° | 0.0262° | 0.1817° |
| 2021 | 2920 | 0.1981° | 0.0201° | 0.1928° |
| 2022 | 2920 | 0.2072° | 0.0209° | 0.2004° |
| 2023 | 2920 | 0.2119° | 0.0308° | 0.2049° |
| 2024 | 2928 | 0.2133° | 0.0453° | 0.2076° |
| 2025 | 2920 | 0.2127° | 0.0615° | 0.2100° |
| 2026 | 1369 | 0.2276° | 0.0661° | 0.2242° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
