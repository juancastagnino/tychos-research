# TYCHOS Moon geometry

## Status

The current Moon is a validated experimental TYCHOS geometry. It remains an
Earth-hosted body and is generated entirely by the model hierarchy before right
ascension, declination, distance or elongation are calculated. No fitted
longitude term, lookup table, date-specific offset or post-export correction is
used.

The final configuration was developed on a dense `2000-2026` comparison and
then independently validated from `1800-06-21` through `2026-06-21`. Its angular
and distance performance remained stable across the full 226-year interval.

## Hierarchy

```text
Earth
└─ Moon Node
   └─ Moon Plane
      └─ Moon Deferent A
         └─ Solar-Coupled Lunar Geometry
            ├─ 2D-M eccentric action
            ├─ solar-variation action
            ├─ anomalistic tangential action
            └─ Moon Orbit
```

These intermediate stages are geometric motions, not additional celestial
bodies. The same hierarchy drives the rendered Moon, physical-scale coordinate
Moon, plot/export model and Edit Settings data.

## Plane and node

The investigation began by correcting the original Moon declination problem.
The Moon's inclination is no longer treated only as a static tilt on the final
orbit. `Moon Plane` defines the inclined orbital plane, while `Moon Node`
controls its changing orientation. This made the intended lunar geometry
explicit and substantially improved declination without altering exported
coordinates afterward.

## How residual analysis was used

Residual spectra exposed recurring structures near the anomalistic month,
approximately `31.8` days, approximately `14.8` days and one year. These were
used only as diagnostic fingerprints. Their measured periods were never inserted
into the astronomical model.

An implementation such as the following is explicitly rejected:

```text
moon longitude += fittedAmplitude * sin(fittedPeriod * time + fittedPhase)
```

Instead, every retained cycle emerges from rotations and directions already
present in the Sun-Earth-Moon geometry.

## Coordinated anomalistic geometry

`Moon Deferent A` and the final Moon orbit form a coordinated phase pair. The
retained phases are:

```text
Moon Deferent A startPos: 167.51°
Moon orbit startPos:      318°
```

Changing one without the other produced a large global orientation error. Their
successful paired behavior confirmed that the deferent performs a necessary
geometric role.

A large deferent radius supplied useful angular action but nearly doubled the
physical distance excursion. Reducing that radius corrected distance but
removed the angular action. The final model therefore separates those two jobs.

## Solar-coupled `2D-M` geometry

The solar-coupled stage derives its direction from:

- the actual Earth-to-Moon direction;
- the actual Earth-to-Sun direction; and
- the Moon's existing anomalistic phase.

If `D` denotes lunar elongation and `M` anomalistic phase, the relationship has
the form `2D-M`. It is not evaluated as a correction to longitude. Its geometric
centre is oriented relative to the Moon direction:

```text
Moon direction + (2D-M)
```

Treating `2D-M` as an absolute direction was rejected because it introduced
artificial cycles near `202-206` days. Using the Moon-relative orientation
removed that reference-frame error.

The retained amplitude is:

```json
"Moon Solar-Coupled Eccentric": {
  "orbitRadius": "-0.0055"
}
```

### Final radial reflection

Point-by-point distance auditing revealed that this vector's tangential action
was beneficial but its Earth-Moon radial action had the wrong orientation. The
vector is now decomposed relative to the instantaneous Earth-Moon direction:

- its tangential component is preserved;
- its radial component is reflected across the instantaneous lunar tangent.

This is performed on the model-space displacement before the Moon coordinates
are derived. It is an explicit geometric reflection, not a distance correction.

Three controlled states were tested:

1. Original radial action.
2. Radial-neutral projection.
3. Reflected radial action.

Radial suppression reduced distance RMS by about `43%` and improved every
angular RMS metric. Full reflection retained those gains, further improved the
angular metrics, and reduced the 2015 eclipse distance discrepancy from about
`21,000 km` to about `5,400 km`. It was therefore retained.

## Solar variation

A second vector is derived from twice the actual lunar elongation:

```text
Moon direction + 2D
```

No half-synodic period is stored. The cycle emerges from the changing Sun and
Moon directions. Its retained amplitude is:

```json
"Moon Solar Variation": {
  "orbitRadius": "0.002"
}
```

Reversing this complete vector improved some distance values but severely
damaged angular accuracy. Suppressing only its radial component produced only a
modest compromise. The accepted model therefore preserves this vector's
original action and applies the radial reflection only to the `2D-M` stage.

## Anomalistic tangential frame

The physical `Moon Deferent A` radius was reduced to avoid excessive perigee and
apogee excursion. A separate anomalistic tangential stage restores the required
angular action:

1. Read the apsidal direction generated by `Moon Deferent A`.
2. Determine the instantaneous Earth-Moon radial direction.
3. Remove the component parallel to that radius.
4. Retain only the perpendicular displacement.

The retained values are:

```json
"Moon Deferent A": {
  "orbitRadius": "0.01131"
},
"Moon Anomalistic Tangential Frame": {
  "orbitRadius": "0.01655"
}
```

The tangential stage is equivalent to compound circular geometry whose radial
components cancel while transverse components combine. It acts before export
and does not modify RA or longitude directly.

## Retained principal parameters

| Component | Parameter | Value |
|---|---|---:|
| Moon Deferent A | `startPos` | `167.51°` |
| Moon Deferent A | `speed` | `0.71015440177343` |
| Moon Deferent A | `orbitRadius` | `0.01131` |
| Moon orbit | `startPos` | `318°` |
| Moon orbit | `speed` | `83.28521004` |
| Solar-Coupled Eccentric | `orbitRadius` | `-0.0055` |
| Solar Variation | `orbitRadius` | `0.002` |
| Anomalistic Tangential Frame | `orbitRadius` | `0.01655` |

The Moon speed was refined from `83.2851946` to `83.28521004` at the author's
request. Over the dense modern interval this improved RA RMS by about `2.7%` and
angular-separation RMS by about `1.5%`, with a small declination-RMS tradeoff.

## Final long-interval validation

```text
Interval:  1800-06-21 through 2026-06-21
Cadence:   1 day
Samples:   82,546
Reference: JPL apparent true-of-date
```

| Coordinate | Mean difference | RMS |
|---|---:|---:|
| Right ascension | `-0.208457°` | `0.290102°` |
| Declination | `-0.001203°` | `0.203615°` |
| Angular separation | `0.309363°` | `0.345048°` |

The dominant remaining RA structure is annual at approximately `0.186°`. The
formerly dominant solar-coupled and half-synodic structures were substantially
reduced by separate geometric elements.

## Distance validation

Across the same 82,546 timestamps:

| Statistic | Result |
|---|---:|
| Mean TYCHOS minus JPL | `+37.3 km` |
| RMS distance error | `5,711.1 km` |
| Mean absolute error | `4,787.6 km` |
| 95th-percentile absolute error | `11,572.7 km` |
| Maximum absolute error | `14,276.3 km` |

Long-interval extremes were:

| Extreme | TYCHOS | JPL reference in the interval | Difference |
|---|---:|---:|---:|
| Minimum / perigee-like | `362,246 km` | about `356,396 km` | about `+5,850 km` |
| Maximum / apogee-like | `412,537 km` | about `406,708 km` | about `+5,829 km` |

Those accumulated extremes alone do not describe point-by-point performance.
The mean bias is only `+37 km`; the remaining error comes from phase and
interference among radial cycles rather than a simple fixed radius offset.

For the 2015-03-20 solar eclipse, the dense three-hour comparison gave:

| Source | Distance near greatest eclipse |
|---|---:|
| TYCHOS | `363,275 km` |
| JPL | `357,886 km` |
| Difference | `+5,389 km` |

Before radial reflection, that event differed by approximately `21,094 km`.
The reflected geometry therefore reduced this particular discrepancy by about
`74.5%`.

The modern `2000-2026` distance RMS was `5,706.5 km`; the independent
`1800-2026` value was `5,711.1 km`. This near-identical performance across more
than two centuries is strong evidence that the result is transferable rather
than fitted to the modern interval.

## Why this is TYCHOS-framework compatible

- The Moon remains a child of Earth.
- The Sun is used as a directional reference, not as the Moon's parent.
- Every motion is evaluated inside the astronomical hierarchy.
- No correction is applied to exported RA, declination, longitude or distance.
- No observed residual period is stored as a forcing frequency.
- The cycles change automatically if the underlying Sun or Moon geometry changes.
- Parameters are ordinary geometric quantities: phase, speed and displacement
  radius.
- JPL is used to assess candidate geometry, not by the running simulator.

The precise solar-coupled construction is not claimed as a verbatim mechanism
from the TYCHOS book. It is an explicit geometrical extension consistent with
the project's method and remains open to physical interpretation by the authors.

## Important rejected experiments

- Static Moon-orbit and deferent centre offsets worsened all angular RMS values.
- A Moon-only eccentric stage gave negligible or negative improvement.
- Treating `2D-M` as an absolute direction created artificial long cycles.
- Changing only one member of the coordinated deferent/orbit phase pair caused
  a large global orientation error.
- A large deferent radius improved angles but nearly doubled radial excursion.
- Reducing that radius without a tangential replacement restored a large
  anomalistic angular residual.
- Reversing the complete solar-variation vector improved distance but more than
  doubled angular-separation RMS.

## Recommended status

Treat this configuration as the accepted experimental Moon baseline. Preserve
its settings, raw export, JPL product, analysis configuration, angular reports
and distance audit together before any further refinement.

The radial-reflection multiplier should be exposed as a named declarative model
parameter rather than left only as an implementation constant. That will make
the accepted geometry visible, editable and serializable in the same manner as
the other Moon components.
