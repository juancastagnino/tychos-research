# TYCHOS Jupiter Ephemeris Audit

**Model:** TYCHOS jupiter / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:51:23.992549+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.0717° | 0.3301° | 0.5774° | 0.7363° |
| Declination | -0.2642° | 0.2890° | 0.4696° | 0.5391° |
| Angular separation | 0.3969° | 0.4303° | 0.6954° | 0.8968° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.2812° | 0.2805° | 0.3850° |
| 2001 | 2920 | 0.3115° | 0.3141° | 0.4280° |
| 2002 | 2920 | 0.3353° | 0.2760° | 0.4198° |
| 2003 | 2920 | 0.2933° | 0.2805° | 0.4023° |
| 2004 | 2928 | 0.2579° | 0.3332° | 0.4205° |
| 2005 | 2920 | 0.3230° | 0.3793° | 0.4973° |
| 2006 | 2920 | 0.4051° | 0.3416° | 0.5188° |
| 2007 | 2920 | 0.3465° | 0.2195° | 0.3888° |
| 2008 | 2928 | 0.1506° | 0.1276° | 0.1890° |
| 2009 | 2920 | 0.2960° | 0.1796° | 0.3368° |
| 2010 | 2920 | 0.3999° | 0.2784° | 0.4862° |
| 2011 | 2920 | 0.4002° | 0.3039° | 0.4984° |
| 2012 | 2928 | 0.3731° | 0.3250° | 0.4850° |
| 2013 | 2920 | 0.3671° | 0.3072° | 0.4591° |
| 2014 | 2920 | 0.3593° | 0.2627° | 0.4301° |
| 2015 | 2920 | 0.2886° | 0.2780° | 0.3977° |
| 2016 | 2928 | 0.2601° | 0.3414° | 0.4285° |
| 2017 | 2920 | 0.3399° | 0.3848° | 0.5118° |
| 2018 | 2920 | 0.4093° | 0.3335° | 0.5147° |
| 2019 | 2920 | 0.3125° | 0.2069° | 0.3548° |
| 2020 | 2928 | 0.1363° | 0.1329° | 0.1837° |
| 2021 | 2920 | 0.3319° | 0.2064° | 0.3820° |
| 2022 | 2920 | 0.4079° | 0.2898° | 0.4997° |
| 2023 | 2920 | 0.3930° | 0.2999° | 0.4893° |
| 2024 | 2928 | 0.3444° | 0.3177° | 0.4586° |
| 2025 | 2920 | 0.2968° | 0.3010° | 0.4079° |
| 2026 | 1369 | 0.2036° | 0.3209° | 0.3722° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
