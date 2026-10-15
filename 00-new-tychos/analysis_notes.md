# Analysis notes

Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.

Read the [research README](../README.md) for the retained baselines and comparison conventions.

## Sun — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: venus mercury baseline vs JPL

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

Export configuration: venus mercury baseline vs JPL

- RA: mean 0.014390 deg; RMS 2.620184 deg.
- Declination: mean 0.188732 deg; RMS 0.998030 deg.
- Angular separation: mean 2.148367 deg; RMS 2.690188 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.248 days, approximately 2.5620 deg.
  - 49.998 days, approximately 1.9910 deg.
  - 169.848 days, approximately 0.9133 deg.
  - 34.933 days, approximately 0.7509 deg.

## Venus — true-of-date apparent

Interval: 1800-06-21 00:00:00 to 2026-06-21 00:00:00; 82546 samples.

Export configuration: venus mercury baseline vs JPL

- RA: mean 0.043248 deg; RMS 0.422059 deg.
- Declination: mean 0.042494 deg; RMS 0.209577 deg.
- Angular separation: mean 0.355078 deg; RMS 0.447191 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 224.921 days, approximately 0.3283 deg.
  - 365.248 days, approximately 0.2352 deg.
  - 162.173 days, approximately 0.1370 deg.
  - 416.899 days, approximately 0.1225 deg.

## Questions to investigate

- Test whether biases and fitted coefficients transfer to a separate time interval.
- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.
- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.
