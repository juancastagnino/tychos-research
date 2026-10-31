# TYCHOS Moon model

## Current baseline: `paired-radial-3d`

The accepted working Moon model no longer uses a lunar equant. Its purpose is to keep the Moon's base orbital rotation uniform while representing observed position and distance behaviour through explicit, pre-export geometry.

```text
Earth
└─ Lunar Nodal / Plane Frame
   └─ Lunar Apsidal Geometry
      └─ Geometry-dependent Lunar Centre Displacement
         ├─ Solar-coupled contribution
         ├─ Paired-radial contribution in the lunar plane
         └─ Moon Orbit
```

The implementation evaluates both centre-displacement contributions in `MoonSolarCoupledEccentric.jsx`. They are part of the rendered hierarchy, coordinate calculation and ephemeris export; no longitude, RA, declination or distance correction is added after export.

## Roles of the stages

### Nodal and plane frame

The lunar plane establishes the approximately 5.1-degree inclination. The node sets the direction of that inclination and lets it regress. Keeping them separate is the geometrical solution to the original declination problem: inclination and nodal orientation are different quantities.

| Component | Parameter | Value |
|---|---|---:|
| Lunar node | `startPos` | `-296°` |
| Lunar node | `speed` | `-0.33780566` |
| Lunar plane | `orbitTilta / orbitTiltb` | `0.1° / -5.2°` |

### Apsidal geometry

The apsidal stage slowly carries the lunar orbital centre around its theoretical Earth-centred location. It is the evolved form of the former Moon Deferent A, not an exported correction.

| Parameter | Value |
|---|---:|
| `startPos` | `167.51°` |
| `speed` | `0.71015440177343` |
| `orbitRadius` | `0.028147459454447972` |

### Solar-coupled contribution

Two small vectors are derived from existing Earth-Sun-Moon and apsidal directions. They use the familiar lunar argument relationships often called `2D-M` and `2D`; their periods are consequences of the model's relative motions, not independently fitted calendar periods.

| Parameter | Value |
|---|---:|
| `orbitRadius` | `-0.0055` |
| `solarVariationRadius` | `0.002168` |

Using `2D` and `2D-M` identifies a geometrical relationship; it is not a claim that conventional gravitational terminology validates the TYCHOS interpretation.

### Paired-radial contribution in the lunar plane

The paired-radial stage replaces the removed equant. It applies two coordinated centre-displacement vectors in the **moving lunar plane**, using the uncorrected Earth-Moon direction and apsidal frame before the displacement. Its retained radius is `-0.007055` per vector.

The resulting Earth-Moon distance varies because the final Moon position is displaced inward and outward relative to the theoretical centre. This does **not** mean that the local Moon orbit circle expands, contracts, or is traversed with an imposed variable angular speed. The local orbit retains its fixed radius and base rotation; it is the centre, and therefore the resultant Earth-centred path, that moves.

This is an explicit geometrical hypothesis, not proof of its physical cause. Its advantage over an equant is that it expresses the distance action as visible centre geometry rather than as a virtual point controlling angular progression.

### Moon orbit

| Parameter | Value |
|---|---:|
| `startPos` | `317.83°` |
| `speed` | `83.28521004` |
| `orbitRadius` | `0.25695552897999907` |

## Validation status

On the dense `2000-06-21` to `2026-06-21` apparent true-of-date comparison, the saved 2D and 3D paired-radial runs produced the following angular RMS values in degrees:

| Metric | 2D paired radial | 3D paired radial |
|---|---:|---:|
| RA | `0.325625` | `0.322465` |
| Declination | `0.249383` | `0.207025` |
| Angular separation | `0.399335` | `0.371747` |

The 3D form was retained because placing the vectors in the lunar plane greatly improved declination while slightly improving RA and angular separation. Each candidate remains subject to independent angular and distance audits; these figures do not establish the physical mechanism.

## Superseded equant configuration

Earlier branches used an apsidal equant-like circle-and-ray construction and reported strong angular and distance statistics. Those results belong to that historical configuration only. The equant was removed from the current baseline because it imposed non-uniform angular progression around the local lunar circle and was less straightforward to interpret within the intended geometrical framework.

Likewise, earlier separate `moon-anomalistic-tangent` and standalone solar-variation stages are superseded. The retained model groups the solar-coupled and paired-radial actions as contributions to one geometry-dependent lunar-centre displacement.

## Migration note

The `tychos-migration` / TSOG flat-model branch evaluates the solar-coupled and paired-radial 3D vectors together in its lunar centre-offset operation. Its Moon still requires an ephemeris comparison on the same interval after every parameter synchronization, but the paired-radial action itself is no longer absent from that architecture.