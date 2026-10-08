# TYCHOS Uranus Ephemeris Audit

**Model:** TYCHOS uranus / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-08T00:40:33.429577+00:00
- Export configuration: old tychos vs jpl apparent-of-date
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | -0.3144° | 0.3327° | 0.4923° | 0.5184° |
| Declination | 0.0481° | 0.0630° | 0.1067° | 0.1194° |
| Angular separation | 0.3186° | 0.3337° | 0.4837° | 0.5059° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.3883° | 0.0432° | 0.3758° |
| 2001 | 2920 | 0.4286° | 0.0339° | 0.4162° |
| 2002 | 2920 | 0.4271° | 0.0347° | 0.4172° |
| 2003 | 2920 | 0.4222° | 0.0360° | 0.4148° |
| 2004 | 2928 | 0.4148° | 0.0375° | 0.4096° |
| 2005 | 2920 | 0.4071° | 0.0387° | 0.4039° |
| 2006 | 2920 | 0.3989° | 0.0399° | 0.3975° |
| 2007 | 2920 | 0.3917° | 0.0409° | 0.3917° |
| 2008 | 2928 | 0.3851° | 0.0418° | 0.3863° |
| 2009 | 2920 | 0.3801° | 0.0423° | 0.3819° |
| 2010 | 2920 | 0.3751° | 0.0429° | 0.3775° |
| 2011 | 2920 | 0.3695° | 0.0438° | 0.3721° |
| 2012 | 2928 | 0.3614° | 0.0457° | 0.3641° |
| 2013 | 2920 | 0.3509° | 0.0485° | 0.3536° |
| 2014 | 2920 | 0.3367° | 0.0528° | 0.3395° |
| 2015 | 2920 | 0.3198° | 0.0586° | 0.3230° |
| 2016 | 2928 | 0.3006° | 0.0654° | 0.3046° |
| 2017 | 2920 | 0.2806° | 0.0723° | 0.2859° |
| 2018 | 2920 | 0.2608° | 0.0788° | 0.2677° |
| 2019 | 2920 | 0.2425° | 0.0842° | 0.2512° |
| 2020 | 2928 | 0.2262° | 0.0883° | 0.2366° |
| 2021 | 2920 | 0.2140° | 0.0904° | 0.2254° |
| 2022 | 2920 | 0.2053° | 0.0909° | 0.2168° |
| 2023 | 2920 | 0.1997° | 0.0901° | 0.2106° |
| 2024 | 2928 | 0.1959° | 0.0888° | 0.2057° |
| 2025 | 2920 | 0.1924° | 0.0874° | 0.2011° |
| 2026 | 1369 | 0.1681° | 0.0885° | 0.1811° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
