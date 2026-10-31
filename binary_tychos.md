# Binary TYCHOS: current model overview

## Purpose

This document describes the current application of the Binary TYCHOS model in
Tychosium. It is an implementation guide to the **present hierarchy and its
geometrical roles**, not a record of every migration, experiment or numerical
comparison that led here.

The core rule is simple: positions must arise from declared geometry before
coordinate calculation and ephemeris export. The model does not apply fitted RA,
declination, longitude or distance corrections after an ephemeris is produced.

## Declared hierarchy

```text
System Center / PVP reference
└─ Earth
   ├─ Earth-Moon System
   │  └─ Moon
   └─ Sun-Mars Binary Frame
      └─ Sun Primary
         ├─ Mars Binary Companion
         │  ├─ Phobos
         │  └─ Deimos
         ├─ Venus Senior Solar Moon
         ├─ Mercury Junior Solar Moon
         ├─ Jupiter
         ├─ Saturn
         ├─ Uranus
         ├─ Neptune
         ├─ Pluto
         ├─ Halley
         └─ Eros
```

`SystemCenter` is a coordinate reference associated with the Earth/PVP
construction. It is not a physical body, a conventional barycentre or an
additional source of motion.

The hierarchy is intentionally asymmetric. The Sun is Earth-referenced, while
Mars is treated as the Sun's binary companion and the remaining solar bodies
inherit the Sun's translation through the declared parent chain. This expresses
the intended Binary TYCHOS relationship in software without forcing a
conventional equal-mass binary interpretation.

## Parent inheritance

A child receives the world translation of its parent. Its own deferent, plane
or local orbit supplies only what belongs to that branch: local orientation,
centre displacement, phase, radius, tilt or counterrotation.

This distinction is important. A local counterrotation may cancel an inherited
**orientation** where necessary without cancelling the inherited world
**position** of the Sun.

### Venus and Mercury

```text
Sun
├─ Venus Deferent
│  └─ Venus Plane
│     └─ Venus Orbit
└─ Mercury Deferent
   └─ Mercury Plane
      └─ Mercury Orbit
```

Both are ordinary Sun-hosted branches. Their deferent and plane stages are
retained because each has its own local orientation and centre requirements;
they are not duplicate copies of the Sun's path.

### Mars

```text
Sun
└─ Mars Binary Annual Frame
   └─ Mars Long-Period Deferent
      └─ Mars Orbit
```

Mars remains distinct from the ordinary solar branches because its role is that
of the Sun's binary companion. The named stages replace the less informative
legacy names “primary carrier” and “secondary carrier”.

### Pluto

```text
Sun
└─ Pluto Deferent Frame
   └─ Pluto Eccentric Frame
      └─ Pluto Orbit
```

Pluto's eccentric frame translates the centre of its local orbit while preserving
that orbit's local orientation. In plain geometrical terms, it is equivalent to
moving an orbit from one location to another without rotating the orbit itself.
The specialised operation prevents a parent rotation from unintentionally
turning Pluto's local orbital axes.

### Eros

```text
Sun
└─ Eros Sun-Relative Annual Frame
   └─ Eros Annual Centre Oscillation
      └─ Eros Local Deferent
         └─ Eros Orbit
```

The annual centre oscillation is a visible, declared translation of Eros's local
centre. It preserves the established Eros path without relying on an opaque
post-export residual.

## Current Moon model

```text
Earth
└─ Lunar Nodal / Plane Frame
   └─ Lunar Apsidal Geometry
      └─ Geometry-Dependent Lunar Centre Displacement
         ├─ Solar-coupled contribution
         ├─ Paired-radial contribution in the lunar plane
         └─ Moon Orbit
```

The lunar node and plane have separate roles:

- The **plane** establishes the lunar inclination.
- The **node** establishes the direction of that inclination and its regression.

The apsidal geometry carries the local lunar-orbit centre around its theoretical
Earth-centred location. It is the current semantic successor to the former Moon
Deferent A.

The geometry-dependent lunar-centre displacement combines two actions before
the Moon's local orbit is evaluated:

- **Solar-coupled contribution:** derived from the instantaneous Earth–Moon,
  Earth–Sun and lunar apsidal relationships. Its `2D-M` and `2D` components
  are generated from model geometry, not from a fitted calendar correction.
- **Paired-radial contribution:** two coordinated vectors derived from the
  Earth–Moon direction in the moving lunar/apsidal plane. It adds an additional
  displacement of the same local lunar-orbit centre.

The paired-radial contribution does not resize the Moon's local circular orbit
or impose a variable orbital speed. The local circle and its base rotation remain
as declared; the centre displacement changes the final Earth-centred position.

The historical lunar equant and the earlier separate anomalistic-tangential
stage are not part of the retained `paired-radial-3d` baseline.

For parameter values, validation results and historical context, see
[moon_model.md](moon_model.md).

## Software model

The primary implementation uses `src/settings/celestial-model.json` as the
single astronomical model definition. It contains:

- celestial bodies and their `parentId` relationships;
- named local motion stages and numerical parameters;
- the ordered render/evaluation hierarchy; and
- the data used by the hierarchy-aware Edit Settings interface.

The live Three.js scene, plot/export scene and coordinate calculation must use
the same declared stages. A new geometrical action is acceptable only if it is
visible in the model, participates before ephemeris calculation, and can be
examined independently.

## TSOG migration status

The separate `tychos-migration` repository uses Patrik's flat
`objects[]` / `parentId` model rather than the nested source representation. It
contains the current directly compatible planetary parameters and preserves its
own architecture.

Its lunar special-motion layer evaluates the solar-coupled and paired-radial
terms together as a geometry-dependent lunar-centre displacement. The
parameters remain editable in the Settings panel under the lunar geometry
operation. Final equivalence should always be confirmed with an ephemeris run
on the same interval and reference convention.

## Working principles

- Geometry before output correction.
- A clear declared role for every added stage.
- Parent inheritance should replace duplicated absolute motion where possible.
- Preserve a successful configuration before experimenting.
- Compare like with like: same interval, cadence and reference-product
  convention.
- Treat JPL agreement as a measurement of coordinate agreement, not proof of a
  cosmological interpretation.

## Related documents

- [moon_model.md](moon_model.md) — current lunar model, parameters and
  validation context.
- [tychos_project_summary.md](tychos_project_summary.md) — project-level
  history, methodology and research status.
- `code-guide.md` — software and implementation notes for developers.