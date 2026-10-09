# First-year apparent-of-date frame check

Current TYCHOS export. First year: 21 June 2000 to 21 June 2001 (end exclusive), 2,920 samples per body.
The exports do not cover January–June 2000. Full interval: 21 June 2000 to 21 June 2026.

RMS and means below are in degrees. Rotation is a diagnostic, not an applied correction.

## tychos_vs_jpl

| Body | First-year mean RA | Mean Dec | RMS RA | RMS Dec | RMS separation | Full RMS separation | Last-year RMS separation |
|---|---:|---:|---:|---:|---:|---:|---:|
| moon | -0.191747 | -0.005531 | 1.054429 | 0.320674 | 1.061235 | 1.073484 | 1.103712 |
| sun | 0.019242 | 0.003585 | 0.051879 | 0.011613 | 0.050539 | 0.053584 | 0.057997 |
| mercury | -0.215324 | 0.215593 | 2.906443 | 0.921409 | 2.907069 | 2.648538 | 2.761348 |
| venus | 0.304097 | 0.002420 | 0.439675 | 0.303748 | 0.518864 | 0.457984 | 0.289474 |
| mars | -0.171575 | -0.241493 | 0.755417 | 0.271478 | 0.751129 | 0.621506 | 0.376517 |
| jupiter | -0.150281 | -0.295475 | 0.342898 | 0.306654 | 0.444007 | 0.430288 | 0.358477 |
| saturn | 0.549893 | 0.021670 | 0.919964 | 0.152000 | 0.887571 | 0.673577 | 0.648330 |
| uranus | -0.177094 | 0.060238 | 0.192827 | 0.065947 | 0.197709 | 0.157240 | 0.209762 |
| neptune | 0.084133 | 0.047496 | 0.085012 | 0.047592 | 0.093595 | 0.073787 | 0.028753 |
| pluto | 0.736405 | 1.868982 | 0.740442 | 1.870762 | 2.007169 | 5.298340 | 7.801843 |

## tychos_vs_stellarium

| Body | First-year mean RA | Mean Dec | RMS RA | RMS Dec | RMS separation | Full RMS separation | Last-year RMS separation |
|---|---:|---:|---:|---:|---:|---:|---:|
| moon | -0.191857 | -0.005467 | 1.054450 | 0.320663 | 1.061251 | 1.073504 | 1.103720 |
| sun | 0.029405 | 0.005135 | 0.056599 | 0.011185 | 0.054686 | 0.053739 | 0.057997 |
| mercury | -0.215341 | 0.215591 | 2.906445 | 0.921409 | 2.907070 | 2.648538 | 2.761350 |
| venus | 0.304084 | 0.002418 | 0.439666 | 0.303751 | 0.518858 | 0.457983 | 0.289472 |
| mars | -0.171600 | -0.241490 | 0.755416 | 0.271475 | 0.751127 | 0.621504 | 0.376530 |
| jupiter | -0.150344 | -0.295494 | 0.342925 | 0.306673 | 0.444038 | 0.430289 | 0.358495 |
| saturn | 0.549872 | 0.021673 | 0.919949 | 0.152000 | 0.887557 | 0.673596 | 0.648304 |
| uranus | -0.177174 | 0.060204 | 0.192900 | 0.065916 | 0.197765 | 0.157356 | 0.210037 |
| neptune | 0.083912 | 0.047441 | 0.084795 | 0.047536 | 0.093389 | 0.073566 | 0.028989 |
| pluto | 0.736432 | 1.868964 | 0.740468 | 1.870744 | 2.007161 | 5.298380 | 7.801926 |

## stellarium_vs_jpl

| Body | First-year mean RA | Mean Dec | RMS RA | RMS Dec | RMS separation | Full RMS separation | Last-year RMS separation |
|---|---:|---:|---:|---:|---:|---:|---:|
| moon | 0.000111 | -0.000064 | 0.000114 | 0.000070 | 0.000130 | 0.000138 | 0.000082 |
| sun | -0.010163 | -0.001551 | 0.035941 | 0.005794 | 0.033958 | 0.006658 | 0.000019 |
| mercury | 0.000016 | 0.000002 | 0.000021 | 0.000006 | 0.000021 | 0.000017 | 0.000020 |
| venus | 0.000014 | 0.000002 | 0.000025 | 0.000009 | 0.000026 | 0.000023 | 0.000020 |
| mars | 0.000025 | -0.000003 | 0.000029 | 0.000011 | 0.000029 | 0.000019 | 0.000021 |
| jupiter | 0.000063 | 0.000019 | 0.000066 | 0.000024 | 0.000066 | 0.000063 | 0.000052 |
| saturn | 0.000021 | -0.000003 | 0.000024 | 0.000008 | 0.000024 | 0.000062 | 0.000040 |
| uranus | 0.000080 | 0.000034 | 0.000081 | 0.000036 | 0.000086 | 0.000176 | 0.000340 |
| neptune | 0.000220 | 0.000055 | 0.000221 | 0.000056 | 0.000217 | 0.000304 | 0.000391 |
| pluto | -0.000027 | 0.000018 | 0.000031 | 0.000026 | 0.000040 | 0.000064 | 0.000087 |

## Shared rotation — temporal validation

Fit one three-axis rotation on the first half of the first year; evaluate on the second half.
All bodies receive the same rotation. Values are pooled angular RMS with equal sample counts.

| Comparison | Fit group | Rotation magnitude | Held-out RMS before | Held-out RMS after |
|---|---|---:|---:|---:|
| tychos_vs_jpl | all_ten | 0.380755° | 1.227265° | 1.194409° |
| tychos_vs_jpl | without_mercury_pluto | 0.199892° | 0.598592° | 0.639697° |
| tychos_vs_stellarium | all_ten | 0.380741° | 1.227299° | 1.194328° |
| tychos_vs_stellarium | without_mercury_pluto | 0.199841° | 0.598688° | 0.639212° |
| stellarium_vs_jpl | all_ten | 0.000053° | 0.015187° | 0.015193° |
| stellarium_vs_jpl | without_mercury_pluto | 0.000067° | 0.016979° | 0.016989° |

## Reference timestamp quality checks

For first-year Stellarium/JPL disagreements above 1 arcsecond, compare adjacent JPL timestamps (3-hour cadence).

- sun: 234 affected samples; 2001-04-28T15:00:00 through 2001-06-12T12:00:00.
  Best JPL offset counts (hours): {'-3': 234, '0': 0, '3': 0}.
  RMS disagreement (arcseconds) by JPL offset: {'-3': 0.04216396835365615, '0': 431.84579501398827, '3': 863.7125288140084}.
- jupiter: 5 affected samples; 2001-06-14T09:00:00 through 2001-06-14T21:00:00.
  Best JPL offset counts (hours): {'-3': 0, '0': 5, '3': 0}.
  RMS disagreement (arcseconds) by JPL offset: {'-3': 103.97624737499726, '0': 1.1620097811339722, '3': 103.29510809367821}.
- neptune: 13 affected samples; 2001-01-26T12:00:00 through 2001-01-28T00:00:00.
  Best JPL offset counts (hours): {'-3': 0, '0': 13, '3': 0}.
  RMS disagreement (arcseconds) by JPL offset: {'-3': 18.348219099548984, '0': 1.3087593649051723, '3': 15.893954836157167}.

These samples are flagged, not shifted or repaired. A match to an earlier timestamp is evidence of a timing/update issue, not proof of its software cause.

## Interpretation limits

- A short interval reduces some accumulated drift; it does not eliminate a fixed frame offset or orbital errors.
- A fitted rotation can absorb model errors; its success alone does not establish a reference-frame cause.
- Inspect results.json for per-body effects, rotation components and input hashes.
- Strong changes between bodies or degradation on held-out dates argue against a single constant rotation being the main explanation.
- No export or model configuration was changed.
