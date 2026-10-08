# TYCHOS Venus Ephemeris Audit

**Model:** TYCHOS venus / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:50:29.537860+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.0230° | 0.4283° | 0.9659° | 1.4904° |
| Declination | 0.0424° | 0.2219° | 0.4952° | 0.7768° |
| Angular separation | 0.3589° | 0.4580° | 0.9436° | 1.4936° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.4516° | 0.1804° | 0.4565° |
| 2001 | 2920 | 0.3382° | 0.2937° | 0.4427° |
| 2002 | 2920 | 0.4814° | 0.1803° | 0.4886° |
| 2003 | 2920 | 0.2743° | 0.1214° | 0.2843° |
| 2004 | 2928 | 0.4965° | 0.2930° | 0.5411° |
| 2005 | 2920 | 0.6064° | 0.2068° | 0.5949° |
| 2006 | 2920 | 0.2201° | 0.1913° | 0.2834° |
| 2007 | 2920 | 0.5212° | 0.2602° | 0.5564° |
| 2008 | 2928 | 0.3642° | 0.1456° | 0.3691° |
| 2009 | 2920 | 0.3280° | 0.2920° | 0.4344° |
| 2010 | 2920 | 0.4808° | 0.1875° | 0.4919° |
| 2011 | 2920 | 0.2747° | 0.1210° | 0.2845° |
| 2012 | 2928 | 0.4877° | 0.3001° | 0.5383° |
| 2013 | 2920 | 0.6177° | 0.2058° | 0.6036° |
| 2014 | 2920 | 0.2108° | 0.1897° | 0.2755° |
| 2015 | 2920 | 0.5273° | 0.2594° | 0.5607° |
| 2016 | 2928 | 0.3697° | 0.1487° | 0.3750° |
| 2017 | 2920 | 0.3342° | 0.2891° | 0.4372° |
| 2018 | 2920 | 0.4762° | 0.1905° | 0.4898° |
| 2019 | 2920 | 0.2756° | 0.1228° | 0.2858° |
| 2020 | 2928 | 0.4797° | 0.3078° | 0.5371° |
| 2021 | 2920 | 0.6296° | 0.2075° | 0.6135° |
| 2022 | 2920 | 0.2028° | 0.1844° | 0.2660° |
| 2023 | 2920 | 0.5368° | 0.2585° | 0.5676° |
| 2024 | 2928 | 0.3753° | 0.1521° | 0.3812° |
| 2025 | 2920 | 0.3334° | 0.2857° | 0.4346° |
| 2026 | 1369 | 0.3516° | 0.0887° | 0.3354° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
