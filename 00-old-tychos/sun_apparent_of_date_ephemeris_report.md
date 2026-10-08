# TYCHOS Sun Ephemeris Audit

**Model:** TYCHOS sun / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:39:52.449021+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0063° | 0.2544° | 0.3575° | 0.3695° |
| Declination | -0.0774° | 0.1026° | 0.2043° | 0.2142° |
| Angular separation | 0.2423° | 0.2691° | 0.3824° | 0.4030° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.2475° | 0.1342° | 0.2766° |
| 2001 | 2920 | 0.2533° | 0.1034° | 0.2684° |
| 2002 | 2920 | 0.2529° | 0.1032° | 0.2680° |
| 2003 | 2920 | 0.2557° | 0.1038° | 0.2707° |
| 2004 | 2928 | 0.2542° | 0.1033° | 0.2692° |
| 2005 | 2920 | 0.2550° | 0.1034° | 0.2699° |
| 2006 | 2920 | 0.2544° | 0.1028° | 0.2691° |
| 2007 | 2920 | 0.2551° | 0.1029° | 0.2699° |
| 2008 | 2928 | 0.2569° | 0.1031° | 0.2716° |
| 2009 | 2920 | 0.2542° | 0.1020° | 0.2687° |
| 2010 | 2920 | 0.2533° | 0.1017° | 0.2678° |
| 2011 | 2920 | 0.2553° | 0.1023° | 0.2698° |
| 2012 | 2928 | 0.2536° | 0.1019° | 0.2682° |
| 2013 | 2920 | 0.2540° | 0.1022° | 0.2686° |
| 2014 | 2920 | 0.2533° | 0.1019° | 0.2678° |
| 2015 | 2920 | 0.2537° | 0.1024° | 0.2684° |
| 2016 | 2928 | 0.2556° | 0.1031° | 0.2704° |
| 2017 | 2920 | 0.2536° | 0.1025° | 0.2683° |
| 2018 | 2920 | 0.2542° | 0.1028° | 0.2690° |
| 2019 | 2920 | 0.2570° | 0.1034° | 0.2717° |
| 2020 | 2928 | 0.2556° | 0.1029° | 0.2702° |
| 2021 | 2920 | 0.2549° | 0.1027° | 0.2696° |
| 2022 | 2920 | 0.2531° | 0.1018° | 0.2675° |
| 2023 | 2920 | 0.2522° | 0.1017° | 0.2667° |
| 2024 | 2928 | 0.2529° | 0.1017° | 0.2674° |
| 2025 | 2920 | 0.2505° | 0.1006° | 0.2647° |
| 2026 | 1369 | 0.2729° | 0.0548° | 0.2724° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
