# TYCHOS Pluto Ephemeris Audit

**Model:** TYCHOS pluto / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:52:40.736627+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -4.0548° | 4.8628° | 7.8474° | 8.3133° |
| Declination | 2.6887° | 2.7093° | 3.0959° | 3.1443° |
| Angular separation | 4.9462° | 5.2983° | 7.6537° | 8.0432° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.7867° | 1.8143° | 1.9723° |
| 2001 | 2920 | 0.5438° | 1.9599° | 2.0312° |
| 2002 | 2920 | 0.1893° | 2.1195° | 2.1275° |
| 2003 | 2920 | 0.3459° | 2.2680° | 2.2930° |
| 2004 | 2928 | 0.7415° | 2.4046° | 2.5104° |
| 2005 | 2920 | 1.1521° | 2.5290° | 2.7649° |
| 2006 | 2920 | 1.5644° | 2.6397° | 3.0427° |
| 2007 | 2920 | 1.9757° | 2.7367° | 3.3348° |
| 2008 | 2928 | 2.3839° | 2.8196° | 3.6342° |
| 2009 | 2920 | 2.7871° | 2.8890° | 3.9359° |
| 2010 | 2920 | 3.1819° | 2.9443° | 4.2343° |
| 2011 | 2920 | 3.5676° | 2.9862° | 4.5272° |
| 2012 | 2928 | 3.9437° | 3.0150° | 4.8126° |
| 2013 | 2920 | 4.3106° | 3.0319° | 5.0907° |
| 2014 | 2920 | 4.6674° | 3.0363° | 5.3596° |
| 2015 | 2920 | 5.0156° | 3.0288° | 5.6204° |
| 2016 | 2928 | 5.3554° | 3.0095° | 5.8729° |
| 2017 | 2920 | 5.6875° | 2.9792° | 6.1184° |
| 2018 | 2920 | 6.0101° | 2.9377° | 6.3550° |
| 2019 | 2920 | 6.3232° | 2.8855° | 6.5831° |
| 2020 | 2928 | 6.6256° | 2.8228° | 6.8019° |
| 2021 | 2920 | 6.9169° | 2.7511° | 7.0118° |
| 2022 | 2920 | 7.1936° | 2.6705° | 7.2098° |
| 2023 | 2920 | 7.4554° | 2.5819° | 7.3961° |
| 2024 | 2928 | 7.7012° | 2.4858° | 7.5698° |
| 2025 | 2920 | 7.9322° | 2.3833° | 7.7326° |
| 2026 | 1369 | 7.9961° | 2.2387° | 7.7530° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
