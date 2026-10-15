# Analysis notes

Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.

Read the [research README](../README.md) for the retained baselines and comparison conventions.

## Sun — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: venus mercury new hierarchy vs JPL

- RA: mean 0.038748 deg; RMS 0.053270 deg.
- Declination: mean 0.000304 deg; RMS 0.014186 deg.
- Angular separation: mean 0.047562 deg; RMS 0.052883 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 363.639 days, approximately 0.0209 deg.
  - 182.624 days, approximately 0.0098 deg.
  - 368.509 days, approximately 0.0036 deg.
  - 398.773 days, approximately 0.0020 deg.

## Mercury — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: venus mercury new hierarchy vs JPL

- RA: mean 0.014251 deg; RMS 2.241029 deg.
- Declination: mean 0.347652 deg; RMS 0.987340 deg.
- Angular separation: mean 1.926522 deg; RMS 2.375774 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 49.998 days, approximately 1.9910 deg.
  - 365.248 days, approximately 1.8293 deg.
  - 34.933 days, approximately 0.7509 deg.
  - 169.848 days, approximately 0.7440 deg.

## Venus — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: venus mercury new hierarchy vs JPL

- RA: mean 0.043297 deg; RMS 0.415547 deg.
- Declination: mean 0.042387 deg; RMS 0.113124 deg.
- Angular separation: mean 0.308311 deg; RMS 0.404515 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 224.921 days, approximately 0.3283 deg.
  - 365.248 days, approximately 0.2352 deg.
  - 162.173 days, approximately 0.1372 deg.
  - 416.899 days, approximately 0.1216 deg.

## Questions to investigate

- Test whether biases and fitted coefficients transfer to a separate time interval.
- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.
- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.
