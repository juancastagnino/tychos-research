# TYCHOS Neptune Ephemeris Audit

**Model:** TYCHOS neptune / True-of-date apparent

## Dataset

- Samples: **75969**
- Interval: **2000-06-21 00:00:00 → 2026-06-21 00:00:00**
- Median cadence: **3.000 h**
- Reference: **JPL Earth true-equator/equinox-of-date apparent RA/Dec (airless)**
- Ecliptic residual analysis: Not computed: true-of-date RA/Dec must not be rotated with fixed J2000 obliquity
- Analysis generated (UTC): 2026-10-07T13:52:30.651125+00:00
- Export configuration: latest tweaks
- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.

## Current residuals

| Metric | Mean | RMS | P95 abs. | Max abs. |
|---|---:|---:|---:|---:|
| RA (coordinate) | 0.0490° | 0.0601° | 0.1001° | 0.1106° |
| Declination | 0.0434° | 0.0455° | 0.0601° | 0.0638° |
| Angular separation | 0.0684° | 0.0738° | 0.1121° | 0.1218° |

## Annual stability

| Year | N | RMS RA | RMS Dec | RMS separation |
|---:|---:|---:|---:|---:|
| 2000 | 1552 | 0.0856° | 0.0472° | 0.0937° |
| 2001 | 2920 | 0.0858° | 0.0490° | 0.0951° |
| 2002 | 2920 | 0.0879° | 0.0517° | 0.0984° |
| 2003 | 2920 | 0.0898° | 0.0543° | 0.1015° |
| 2004 | 2928 | 0.0907° | 0.0563° | 0.1035° |
| 2005 | 2920 | 0.0897° | 0.0576° | 0.1037° |
| 2006 | 2920 | 0.0868° | 0.0580° | 0.1018° |
| 2007 | 2920 | 0.0817° | 0.0574° | 0.0976° |
| 2008 | 2928 | 0.0748° | 0.0557° | 0.0915° |
| 2009 | 2920 | 0.0669° | 0.0534° | 0.0841° |
| 2010 | 2920 | 0.0590° | 0.0507° | 0.0767° |
| 2011 | 2920 | 0.0522° | 0.0482° | 0.0702° |
| 2012 | 2928 | 0.0478° | 0.0463° | 0.0659° |
| 2013 | 2920 | 0.0456° | 0.0452° | 0.0636° |
| 2014 | 2920 | 0.0454° | 0.0449° | 0.0634° |
| 2015 | 2920 | 0.0461° | 0.0451° | 0.0641° |
| 2016 | 2928 | 0.0469° | 0.0453° | 0.0649° |
| 2017 | 2920 | 0.0468° | 0.0452° | 0.0648° |
| 2018 | 2920 | 0.0449° | 0.0443° | 0.0628° |
| 2019 | 2920 | 0.0406° | 0.0422° | 0.0584° |
| 2020 | 2928 | 0.0340° | 0.0389° | 0.0515° |
| 2021 | 2920 | 0.0256° | 0.0343° | 0.0428° |
| 2022 | 2920 | 0.0172° | 0.0289° | 0.0336° |
| 2023 | 2920 | 0.0135° | 0.0231° | 0.0268° |
| 2024 | 2928 | 0.0175° | 0.0177° | 0.0249° |
| 2025 | 2920 | 0.0241° | 0.0130° | 0.0273° |
| 2026 | 1369 | 0.0236° | 0.0101° | 0.0257° |

## Interpretation notes

- No lunar periodic terms are fitted to this body.
- Compare shared-frame changes across bodies using the same epochs and declared export configuration.
- This is an exploratory moving-frame comparison. JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.
- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.
