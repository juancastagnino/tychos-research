# TYCHOS Jupiter Ephemeris Audit

**Model:** TYCHOS jupiter / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:20.155293+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0864° | 0.3464° | 0.6404° | 0.8565° |
| Declination | -0.2820° | 0.3149° | 0.5243° | 0.6373° |
| Angular separation | 0.4164° | 0.4599° | 0.7710° | 0.9828° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.2806° | 0.2595° | 0.3696° |
| 2001 | 2920 | 0.3258° | 0.3115° | 0.4355° |
| 2002 | 2920 | 0.3061° | 0.3106° | 0.4241° |
| 2003 | 2920 | 0.2630° | 0.3501° | 0.4355° |
| 2004 | 2928 | 0.2492° | 0.4241° | 0.4911° |
| 2005 | 2920 | 0.3360° | 0.4670° | 0.5744° |
| 2006 | 2920 | 0.4258° | 0.4031° | 0.5753° |
| 2007 | 2920 | 0.3559° | 0.2391° | 0.4072° |
| 2008 | 2928 | 0.1225° | 0.1096° | 0.1578° |
| 2009 | 2920 | 0.3333° | 0.1522° | 0.3546° |
| 2010 | 2920 | 0.4579° | 0.2533° | 0.5217° |
| 2011 | 2920 | 0.4517° | 0.2739° | 0.5240° |
| 2012 | 2928 | 0.4175° | 0.2987° | 0.5019° |
| 2013 | 2920 | 0.3729° | 0.3092° | 0.4646° |
| 2014 | 2920 | 0.3277° | 0.3025° | 0.4336° |
| 2015 | 2920 | 0.2595° | 0.3520° | 0.4353° |
| 2016 | 2928 | 0.2556° | 0.4334° | 0.5026° |
| 2017 | 2920 | 0.3553° | 0.4700° | 0.5877° |
| 2018 | 2920 | 0.4299° | 0.3897° | 0.5670° |
| 2019 | 2920 | 0.3177° | 0.2202° | 0.3666° |
| 2020 | 2928 | 0.1205° | 0.1113° | 0.1578° |
| 2021 | 2920 | 0.3798° | 0.1787° | 0.4087° |
| 2022 | 2920 | 0.4675° | 0.2641° | 0.5359° |
| 2023 | 2920 | 0.4396° | 0.2694° | 0.5104° |
| 2024 | 2928 | 0.3844° | 0.2941° | 0.4724° |
| 2025 | 2920 | 0.2971° | 0.3091° | 0.4140° |
| 2026 | 1369 | 0.1743° | 0.3487° | 0.3843° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
