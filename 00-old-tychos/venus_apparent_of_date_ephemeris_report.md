# TYCHOS Venus Ephemeris Audit

**Model:** TYCHOS venus / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:06.684927+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.4291° | 0.8029° | 1.4872° | 2.3532° |
| Declination | -0.1004° | 0.2432° | 0.4363° | 1.1124° |
| Angular separation | 0.6807° | 0.8106° | 1.5129° | 2.3077° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.2472° | 0.2087° | 0.3147° |
| 2001 | 2920 | 0.9216° | 0.4011° | 0.9920° |
| 2002 | 2920 | 0.9665° | 0.1416° | 0.9227° |
| 2003 | 2920 | 0.6766° | 0.1687° | 0.6726° |
| 2004 | 2928 | 0.6995° | 0.2162° | 0.6862° |
| 2005 | 2920 | 0.6251° | 0.2082° | 0.6318° |
| 2006 | 2920 | 0.8357° | 0.2445° | 0.8465° |
| 2007 | 2920 | 0.9637° | 0.2369° | 0.9664° |
| 2008 | 2928 | 0.6395° | 0.1634° | 0.6350° |
| 2009 | 2920 | 0.9367° | 0.4086° | 1.0103° |
| 2010 | 2920 | 0.9812° | 0.1472° | 0.9396° |
| 2011 | 2920 | 0.6825° | 0.1676° | 0.6777° |
| 2012 | 2928 | 0.7080° | 0.2188° | 0.6941° |
| 2013 | 2920 | 0.6311° | 0.2109° | 0.6378° |
| 2014 | 2920 | 0.8231° | 0.2408° | 0.8331° |
| 2015 | 2920 | 0.9547° | 0.2291° | 0.9545° |
| 2016 | 2928 | 0.6357° | 0.1655° | 0.6320° |
| 2017 | 2920 | 0.9353° | 0.4118° | 1.0118° |
| 2018 | 2920 | 0.9956° | 0.1592° | 0.9573° |
| 2019 | 2920 | 0.6758° | 0.1692° | 0.6719° |
| 2020 | 2928 | 0.7133° | 0.2235° | 0.6999° |
| 2021 | 2920 | 0.6310° | 0.2170° | 0.6394° |
| 2022 | 2920 | 0.8075° | 0.2344° | 0.8163° |
| 2023 | 2920 | 0.9419° | 0.2232° | 0.9392° |
| 2024 | 2928 | 0.6361° | 0.1666° | 0.6327° |
| 2025 | 2920 | 0.9382° | 0.4146° | 1.0168° |
| 2026 | 1369 | 0.8310° | 0.0442° | 0.7915° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
