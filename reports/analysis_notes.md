# Analysis notes

Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.

Read the [research README](../README.md) for the retained baselines and comparison conventions.

## Moon — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: moon tests vs JPL

- RA: mean -0.208459 deg; RMS 0.295250 deg.
- Declination: mean -0.001159 deg; RMS 0.203255 deg.
- Angular separation: mean 0.312795 deg; RMS 0.348751 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.248 days, approximately 0.1860 deg.
  - 205.850 days, approximately 0.1575 deg.
  - 31.810 days, approximately 0.1000 deg.
  - 29.800 days, approximately 0.0392 deg.

## Sun — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: moon tests vs JPL

- RA: mean 0.038748 deg; RMS 0.053270 deg.
- Declination: mean 0.000304 deg; RMS 0.014186 deg.
- Angular separation: mean 0.047562 deg; RMS 0.052883 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 363.639 days, approximately 0.0209 deg.
  - 182.624 days, approximately 0.0098 deg.
  - 368.509 days, approximately 0.0036 deg.
  - 398.773 days, approximately 0.0020 deg.

## Questions to investigate

- Test whether biases and fitted coefficients transfer to a separate time interval.
- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.
- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.
