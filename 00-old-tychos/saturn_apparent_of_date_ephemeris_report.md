# TYCHOS Saturn Ephemeris Audit

**Model:** TYCHOS saturn / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:26.757370+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0921° | 0.6748° | 1.2747° | 1.7198° |
| Declination | -0.0427° | 0.1618° | 0.3044° | 0.4052° |
| Angular separation | 0.5629° | 0.6646° | 1.2076° | 1.5978° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 1.1800° | 0.1920° | 1.1381° |
| 2001 | 2920 | 0.9767° | 0.1055° | 0.9209° |
| 2002 | 2920 | 0.9953° | 0.0594° | 0.9248° |
| 2003 | 2920 | 0.9526° | 0.1139° | 0.8898° |
| 2004 | 2928 | 0.8542° | 0.1818° | 0.8180° |
| 2005 | 2920 | 0.7275° | 0.2214° | 0.7227° |
| 2006 | 2920 | 0.6073° | 0.2281° | 0.6248° |
| 2007 | 2920 | 0.5291° | 0.2124° | 0.5546° |
| 2008 | 2928 | 0.5113° | 0.1912° | 0.5362° |
| 2009 | 2920 | 0.5477° | 0.1776° | 0.5715° |
| 2010 | 2920 | 0.6122° | 0.1750° | 0.6361° |
| 2011 | 2920 | 0.6819° | 0.1731° | 0.7026° |
| 2012 | 2928 | 0.7416° | 0.1607° | 0.7526° |
| 2013 | 2920 | 0.7834° | 0.1331° | 0.7784° |
| 2014 | 2920 | 0.7964° | 0.0924° | 0.7733° |
| 2015 | 2920 | 0.7761° | 0.0587° | 0.7387° |
| 2016 | 2928 | 0.7192° | 0.0769° | 0.6772° |
| 2017 | 2920 | 0.6297° | 0.1231° | 0.5961° |
| 2018 | 2920 | 0.5161° | 0.1620° | 0.5028° |
| 2019 | 2920 | 0.3991° | 0.1821° | 0.4113° |
| 2020 | 2928 | 0.3130° | 0.1816° | 0.3438° |
| 2021 | 2920 | 0.2978° | 0.1663° | 0.3279° |
| 2022 | 2920 | 0.3473° | 0.1501° | 0.3678° |
| 2023 | 2920 | 0.4212° | 0.1489° | 0.4397° |
| 2024 | 2928 | 0.4975° | 0.1673° | 0.5218° |
| 2025 | 2920 | 0.5743° | 0.1956° | 0.6063° |
| 2026 | 1369 | 0.5386° | 0.1939° | 0.5719° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
