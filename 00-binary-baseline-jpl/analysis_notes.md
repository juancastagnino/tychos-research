# Analysis notes

Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.

Read the [research README](../README.md) for the retained baselines and comparison conventions.

## Moon — true-of-date apparent

Interval: 2000-06-21 00:00:00 to 2026-06-21 00:00:00; 75969 samples.

Export configuration: moon baseline  vs JPL

- RA: mean -0.240912 deg; RMS 1.061210 deg.
- Declination: mean -0.000858 deg; RMS 0.364896 deg.
- Angular separation: mean 0.921211 deg; RMS 1.073484 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 31.760 days, approximately 1.0872 deg.
  - 14.768 days, approximately 0.6572 deg.
  - 365.236 days, approximately 0.1846 deg.
  - 13.782 days, approximately 0.1223 deg.

## Sun — true-of-date apparent

Interval: 2000-06-21 00:00:00 to 2026-06-21 00:00:00; 75969 samples.

Export configuration: moon baseline  vs JPL

- RA: mean 0.009528 deg; RMS 0.054706 deg.
- Declination: mean 0.003903 deg; RMS 0.014145 deg.
- Angular separation: mean 0.048500 deg; RMS 0.053584 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.236 days, approximately 0.0743 deg.
  - 351.708 days, approximately 0.0374 deg.
  - 379.845 days, approximately 0.0369 deg.
  - 182.618 days, approximately 0.0136 deg.

## Questions to investigate

- Test whether biases and fitted coefficients transfer to a separate time interval.
- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.
- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.
