# TYCHOS Moon model

> Current implementation: `paired-radial-3d` replaces the lunar equant with paired radial geometry in the lunar plane. The older detailed sections below describe the superseded equant configuration, including its distance and historical validation; do not attribute those results to the current branch.

## Current paired-radial 3D configuration

Earth → lunar nodal / plane frame → apsidal geometry → paired-radial and solar-coupled geometry → Moon. The editor groups the paired and solar settings separately; the current implementation evaluates both in `MoonSolarCoupledEccentric.jsx`. The equant is absent. The apsidal radius is `0.028147459454447972`; paired radius is `-0.007055` per vector; solar coupling uses `-0.0055` and `0.002168`. The Moon's base rotation rate remains constant; this does not imply that its resulting geocentric trajectory or speed is uniform.

The pair is calculated in the moving lunar plane, using the uncorrected Earth–Moon direction and apsidal frame before the displacement is applied. It alters the modeled position, not only the export. It is a geometric construction, not proof of a physical breathing orbit or an explanation for its cause. The earlier `paired-radial` branch uses world XZ; the `lunarPlaneBlend` experiment has been removed from the 3D branch.

For 2000-06-21–2026-06-21, 3-hour samples, JPL apparent true-of-date comparison gives the following RMS in degrees:

| Metric | 2D | 3D |
|---|---:|---:|
| RA | 0.325625 | 0.322465 |
| Declination | 0.249383 | 0.207025 |
| Angular separation | 0.399335 | 0.371747 |

These are angular results from `00-paired-radial` and `00-paired-radial-3d`, not a distance audit. Check distances separately; earlier equant distance results are not evidence for this configuration. Native Tychosium versus JPL apparent-of-date conventions remain a comparison limitation.

## Historical equant configuration — superseded

This document describes the current experimental Moon implementation. It is the
accepted baseline after successful dense modern and 226-year historical
validation of the final pure-`2D` addition.

The objective has never been to append a correction to the exported longitude.
Every accepted change is part of the visible model geometry and is evaluated by
the normal coordinate and ephemeris pipeline.

## Current functional hierarchy

```text
Earth
└─ Lunar Nodal / Plane Frame
   └─ Lunar Apsidal Frame / Geometry
      ├─ Apsidal radial geometry
      ├─ Lunar Apsidal Equant
      └─ Solar-Coupled Lunar Frame
         ├─ 2D-M eccentric contribution
         ├─ 2D solar-variation contribution
         └─ Moon Orbit
```

The renderer may nest the equant and orbit objects in the exact order needed by
Three.js transformations. The diagram above describes their astronomical roles,
not merely their JSX nesting.

## 1. Nodal and plane geometry

The original declination problem was addressed by making two different ideas
explicit:

- the **plane inclination** sets how much the lunar orbital plane is tilted;
- the **node** sets the direction of the line about which that plane is tilted
  and lets that direction regress over time.

This is a genuine geometrical construction. The Moon remains Earth-hosted and
travels in an explicitly oriented plane instead of receiving a final declination
offset.

Current principal values:

| Component | Parameter | Value |
|---|---|---:|
| Lunar node | `startPos` | `-296°` |
| Lunar node | `speed` | `-0.33780566` |
| Lunar plane | `orbitTilta` | `0.1°` |
| Lunar plane | `orbitTiltb` | `-5.2°` |

## 2. Apsidal geometry and the equant

The remaining large angular residual was dominated by the anomalistic lunar
cycle, about `27.552` days. Static centre offsets could not solve it: they
degraded right ascension, declination and angular separation together.

The successful replacement is a classical **equant-like construction**. A ray
advances uniformly as viewed from a small offset point and intersects the lunar
orbit. The Moon still lies on a circular geometrical path, but its angular
progress around the circle is non-uniform when viewed from Earth.

This matters because the former experimental solution used a separate
`moon-anomalistic-tangent` stage. That stage could improve angular position, but
it split radial and tangential behaviour into separate pseudo-objects and made
distance tuning difficult to interpret. The equant expresses both effects as
one coherent circle-and-ray geometry.

Current apsidal values:

| Component | Parameter | Value |
|---|---|---:|
| Lunar apsidal deferent | `startPos` | `167.51°` |
| Lunar apsidal deferent | `speed` | `0.71015440177343` |
| Lunar apsidal deferent | `orbitRadius` | `0.01407` |
| Lunar apsidal equant | `orbitRadius` | `0.01407` |

The equant reduced the principal `27.552`-day residual amplitude from about
`3.006°` to about `0.027°`, a reduction of roughly `99.1%`.

## 3. One solar-coupled lunar frame

After the anomalistic residual was removed, a stable signal associated with the
Sun-Moon angular relationship became visible. Instead of restoring several
independent hierarchy objects, the current model uses one solar-coupled frame
with two small vector contributions:

### `2D-M` eccentric contribution

`D` is the Moon's elongation from the Sun and `M` is the Moon's anomalistic
phase. The `2D-M` contribution moves the lunar orbital centre according to those
already existing geometrical directions. It is not driven by a separately
fitted calendar period.

Current value:

```json
"orbitRadius": "-0.0055"
```

### Pure `2D` variation contribution

Once the equant and `2D-M` geometry were active, the remaining longitude error
contained an exceptionally stable pure-`2D` term:

- the internal synodic period of `D` was `29.530623` days;
- therefore the internal `2D` period was `14.765312` days;
- the observed residual FFT peak was `14.768468` days;
- its amplitude was about `0.483°` and its phase was stable across the modern
  interval;
- it explained about `74%` of the remaining ecliptic-longitude residual
  variance before implementation.

The same phase was recovered from TYCHOS's own Sun and Moon directions. The
runtime model therefore derives the vector from its internal geometry; it does
not consult JPL and it does not store the FFT period.

Current value:

```json
"solarVariationRadius": "0.002168"
```

After implementation, the exact pure-`2D` residual amplitude fell to about
`0.0033°`, roughly a `99.3%` removal. A nearby `14.791`-day FFT peak remains at
only about `0.034°`; it is a sideband or modulation, not evidence that the main
`2D` vector should be retuned.

## Relation to established lunar terminology

The arguments themselves are not invented names. A NASA lunar-properties table
lists the classical **variation** as a term proportional to `sin(2D)` and
**evection** as a term proportional to `sin(2D-g)`, where `g` is the Moon's mean
anomaly. In the notation used here, `g` plays the role of the anomalistic phase
`M`.

This is useful independent confirmation that `2D` and `2D-M` are meaningful
solar-lunar geometrical relationships. It does **not** mean that NASA validates
the TYCHOS physical interpretation: conventional lunar theory treats them as
solar gravitational inequalities, whereas this experimental TYCHOS model
expresses their observable geometry through moving frames and centre vectors.

Reference: NASA Technical Reports Server, *Lunar Sourcebook precursor material*,
document 19830003839:
https://ntrs.nasa.gov/api/citations/19830003839/downloads/19830003839.pdf

## 4. Moon orbit

| Parameter | Value |
|---|---:|
| `startPos` | `318°` |
| `speed` | `83.28521004` |
| `orbitRadius` | `0.25695552897999907` |

The small speed refinement was supplied by the TYCHOS author and retained
because it improves long-cycle return behaviour.

## Modern validation result

The current model was compared with JPL apparent true-of-date ephemerides from
`2000-06-21` to `2026-06-21`, at three-hour cadence (`75,969` samples).

| Metric | Previous equant + `2D-M` baseline | Current model | RMS improvement |
|---|---:|---:|---:|
| Right ascension, mean (RMS) | `-0.230206° (0.461128°)` | `-0.230071° (0.309603°)` | `32.9%` |
| Declination, mean (RMS) | `-0.001440° (0.240061°)` | `-0.001538° (0.205922°)` | `14.2%` |
| Angular separation, mean (RMS) | `0.449581° (0.501149°)` | `0.326085° (0.361032°)` | `28.0%` |

The mean angular separation improved by about `27.5%`. Full-year angular RMS
values remain stable across the modern interval, approximately `0.321°` to
`0.413°`.

## Historical validation

An independent daily comparison from `1800-06-21` to `2026-06-21` used `82,546`
timestamps and the same JPL apparent true-of-date reference:

| Coordinate | Mean difference | RMS |
|---|---:|---:|
| Right ascension | `-0.208460°` | `0.295290°` |
| Declination | `-0.001161°` | `0.203339°` |
| Angular separation | `0.312773°` | `0.348833°` |

The historical RMS values are slightly lower than the dense modern results:
approximately `4.6%` lower for RA, `1.3%` lower for declination and `3.4%` lower
for angular separation. The improvement therefore transfers across more than two
centuries rather than being confined to the development window.

The largest remaining historical RA signals are annual (`365.248` days, about
`0.186°`), approximately `205.850` days (`0.158°`), and `31.810` days
(`0.099°`). The former dominant anomalistic and pure-`2D` errors are no longer
the leading residuals.

## Distance audit

For the same modern interval, compared point by point with JPL:

| Distance statistic | Current result |
|---|---:|
| Mean error | `+313 km` |
| RMS error | `3,049 km` |
| Mean absolute error | `2,722 km` |
| 95th percentile absolute error | `4,722 km` |
| Maximum absolute error | `5,447 km` |

At the `2015-03-20` eclipse sample, TYCHOS gives approximately `353,059 km`
versus JPL's `357,886 km`, an error of about `-4,827 km`.

The current interval extrema are approximately:

- TYCHOS minimum: `351,884 km`; JPL at that timestamp: `356,812 km`;
- TYCHOS maximum: `410,432 km`; JPL at that timestamp: `406,515 km`.

The accepted configuration therefore favours a strong simultaneous reduction of
angular and point-by-point distance errors, rather than forcing the isolated
minimum and maximum distances to match at the expense of sky position.

The historical distance audit is effectively identical to the modern one:

| Historical distance statistic | Result |
|---|---:|
| Mean error | `+315.0 km` |
| RMS error | `3,048.7 km` |
| Mean absolute error | `2,721.2 km` |
| 95th percentile absolute error | `4,719.2 km` |
| Maximum absolute error | `5,435.3 km` |

The difference between modern and historical distance RMS is only `0.4 km`.
This close agreement is strong evidence that the distance improvement is a
property of the geometry rather than a local fit to 2000-2026.

## Why this is better than the previous experimental hierarchy

The earlier version contained three visibly separate devices:

```text
moon-solar-eccentric
moon-solar-variation
moon-anomalistic-tangent
```

The current version is both simpler and more interpretable:

- the anomalistic tangential device is replaced by one equant geometry;
- `2D-M` and pure `2D` are two contributions inside one solar-coupled frame,
  not two apparent celestial objects;
- all driving angles come from the current Sun-Moon-Earth and apsidal geometry;
- no empirical period or final-coordinate correction is stored;
- radial and angular behaviour can be audited at the level where it is created;
- the editor hierarchy now describes astronomical roles rather than the history
  of individual experiments.

This does not prove a unique physical cause. It does show that the dominant
residuals can be represented compactly by geometrical relations that are already
meaningful in lunar astronomy and are generated internally by TYCHOS.

## Rejected or superseded approaches

- fixed eccentric offsets at the Moon-orbit and apsidal-deferent levels;
- a lunar-only eccentric mechanism with no solar relationship;
- an independently rotating centre whose period was inferred directly from an
  FFT peak;
- the separate `moon-anomalistic-tangent` pseudo-stage;
- a separate hierarchy object for pure solar variation;
- forcing distance extrema while allowing angular accuracy to degrade.

These failures are scientifically useful: they constrain the successful
mechanism to one that distinguishes apsidal timing from solar-lunar geometry.

## Validation status

The final pure-`2D` state has passed the dense modern comparison, the independent
`1800-2026` comparison and the software tests. The new historical report
supersedes older long-interval figures from the equant-plus-`2D-M` configuration.

Future acceptance gates should preserve:

- the modern angular improvement;
- the point-by-point distance improvement;
- the node and plane declination solution;
- geometrical derivation from internal model directions;
- no fitted calendar period and no post-export correction.
