# Analysis notes

Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.

Read the [research README](../README.md) for the retained baselines and comparison conventions.

## Moon — true-of-date apparent

Interval: 2000-06-21 00:00:00 to 2026-06-21 00:00:00; 75969 samples.

Export configuration: mercury tests vs JPL

- RA: mean -0.229925 deg; RMS 0.322465 deg.
- Declination: mean -0.001535 deg; RMS 0.207025 deg.
- Angular separation: mean 0.335067 deg; RMS 0.371747 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.236 days, approximately 0.1852 deg.
  - 206.438 days, approximately 0.1592 deg.
  - 13.782 days, approximately 0.1242 deg.
  - 202.045 days, approximately 0.0954 deg.

## Sun — true-of-date apparent

Interval: 2000-06-21 00:00:00 to 2026-06-21 00:00:00; 75969 samples.

Export configuration: mercury tests vs JPL

- RA: mean 0.009528 deg; RMS 0.054706 deg.
- Declination: mean 0.003903 deg; RMS 0.014145 deg.
- Angular separation: mean 0.048500 deg; RMS 0.053584 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.236 days, approximately 0.0743 deg.
  - 351.708 days, approximately 0.0374 deg.
  - 379.845 days, approximately 0.0369 deg.
  - 182.618 days, approximately 0.0136 deg.

## Mercury — true-of-date apparent

Interval: 2000-06-21 00:00:00 to 2026-06-21 00:00:00; 75969 samples.

Export configuration: mercury tests vs JPL

- RA: mean -0.011342 deg; RMS 2.811157 deg.
- Declination: mean 0.244982 deg; RMS 1.001597 deg.
- Angular separation: mean 2.282778 deg; RMS 2.862271 deg.
- Largest right ascension residual FFT peaks (finite-window estimates, not fitted orbital periods):
  - 365.236 days, approximately 2.8793 deg.
  - 49.980 days, approximately 2.0933 deg.
  - 379.845 days, approximately 1.4436 deg.
  - 351.708 days, approximately 1.4350 deg.

## Questions to investigate

- Test whether biases and fitted coefficients transfer to a separate time interval.
- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.
- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.
