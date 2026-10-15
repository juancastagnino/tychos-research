# Full binary TYCHOS implementation

## Purpose and status

`full-send-binary-tychos` is an experimental completion of the accepted
`native-binary-system` hierarchy. It makes the numerical settings parent-relative,
not only the visible tree.

The initial migration was intentionally equivalence preserving. It established a
clean native baseline before later geometric refinements were tested. The active
model now goes beyond that first baseline: the common Mars/Mercury/Venus annual
residual is absent, and Mercury and Venus have since been simplified from special
A/B carrier chains into ordinary Sun-hosted declarative branches.

## Hierarchy

```text
SystemCenter                         (PVP geometric reference)
└─ Earth                             (PVP path)
   ├─ Moon Node / Plane -> Moon
   └─ Sun-Mars Binary Frame
      └─ Sun Primary Branch -> Sun
         ├─ Mars Junior Companion -> Phobos / Deimos
         ├─ Venus Senior Solar Moon
         ├─ Mercury Junior Solar Moon
         ├─ Jupiter / Saturn / Uranus / Neptune / Pluto
         ├─ Halley
         └─ Eros
```

This is an asymmetric primary/companion description. No conventional mass
barycentre, forced opposition or equal binary radius is introduced. `SystemCenter`
is an identity coordinate reference associated with Earth's PVP geometry, not a
physical body or cause of motion.

The current internal Mercury/Venus branches are:

```text
Sun
├─ Venus deferent
│  └─ Venus Plane
│     └─ Venus
└─ Mercury deferent
   └─ Mercury Plane
      └─ Mercury
```

Each body receives the Sun's translation through normal parent inheritance. Its
single deferent supplies the local counterrotation and body-specific centre,
radius or tilt that the descendant plane/orbit still needs.

## Why another migration was needed

The preceding native hierarchy placed Mars, Mercury, Venus and Eros beneath the
Sun, but preserved exact coordinates by calculating each old absolute chain and
subtracting the old Sun chain at runtime:

```text
relative vector = old absolute body chain - old absolute Sun chain
```

That was a valid and tested coordinate adapter, but the child carrier settings
still contained the former Earth-level radius-100 motion. The code hierarchy was
native while part of the parameter vocabulary remained absolute.

The full migration algebraically decomposes each affected carrier into:

1. a constant centre already expressed relative to the Sun;
2. a three-dimensional annual residual stored as cosine and sine basis vectors;
3. the unchanged local orientation basis required by later deferent, plane and
   main-orbit stages.

The resulting evaluation is:

```text
body world position
  = inherited Sun world position
  + direct relative centre
  + direct annual residual
  + local descendant geometry
```

The child no longer repeats the Sun's radius-100 movement. It receives the Sun's
world position from its parent and contributes only what is unique to its branch.

## Direct carrier settings: migration history and current scope

The equivalence migration originally created `mars-deferent-e`,
`mercury-deferent-a`, `venus-deferent-a` and `eros-deferent-a` as direct
parent-relative carriers. That is historical derivation information, not the
current Mercury/Venus structure. Today only Mars and Eros use the specialized
parent-relative carrier evaluator.

The direct annual residual uses:

```text
R(t) = C cos(wt - phase) + S sin(wt - phase)
```

where `C` is stored in `relativeAnnualCosX/Y/Z`, `S` in
`relativeAnnualSinX/Y/Z`, and the angle uses `relativeAnnualSpeed` and
`relativeAnnualStart`.

| Carrier | Direct centre in model XYZ | Annual residual character |
|---|---:|---|
| Mars E | `(6.8, 0, -20.055)` | small Sun-plane remainder |
| Mercury A | `(-1.3, -0.5, 2.645)` | same small remainder |
| Venus A | `(-3.3, 0, 0.645)` | same small remainder |
| Eros A | `(-43.3, -0.5, 32.145)` | larger 3-D remainder from differing planes |

The table uses model XYZ order. JSON centre fields map as
`X=orbitCentera`, `Y=orbitCenterc`, `Z=orbitCenterb`.

The original residual was not an empirical correction fitted to JPL. It was the exact
algebraic remainder of the accepted predecessor. A later physical experiment may
try to explain or simplify it, but it must not be silently discarded during the
migration.

### Current Mercury and Venus reduction

The former Mercury/Venus A carriers, B/secondary records and special
`MercurySunRelativeOrbit.jsx` / `VenusSunRelativeOrbit.jsx` components have been
removed. Their active model records now own only:

```text
motion.deferent
motion.plane
motion.orbit
```

For Venus, the former A-carrier centre was transformed into the local basis and
absorbed into the Venus plane centre. The resulting plane centre is
`(-1.322868312130857, 0.846478306956517, 0.0028256060705597465)` in the JSON
`a/b/c` fields. For Mercury, the former A vertical offset was transferred to the
plane as `orbitCenterc = -0.5`.

The retained deferents use an annual `-2π` speed to cancel the inherited annual
orientation of the Sun without cancelling its inherited world position. Venus
also retains its local radius `0.6` and tilt `0.03`; Mercury retains its local
centre and `-0.3` tilt. These stages therefore encode real local geometry and are
not redundant placeholder objects.

No JPL fit was used to derive the transferred centres. JPL was used only after
the refactor to measure its observational effect.

## Original common annual residual: historical restoration reference

The equivalence-preserving migration originally gave Mars, Mercury and Venus the
same annual definition. Schema v3 removes these parameters entirely; these
complete original blocks are retained here for deliberate restoration:

```json
{
"mercury-deferent-a": {
  "relativeAnnualStart": 0,
  "relativeAnnualSpeed": 6.283185307179586,
  "relativeAnnualCosX": 0,
  "relativeAnnualCosY": 0,
  "relativeAnnualCosZ": 0,
  "relativeAnnualSinX": 0,
  "relativeAnnualSinY": -0.4820580723705152,
  "relativeAnnualSinZ": -0.0011619066758328245
},
"venus-deferent-a": {
  "relativeAnnualStart": 0,
  "relativeAnnualSpeed": 6.283185307179586,
  "relativeAnnualCosX": 0,
  "relativeAnnualCosY": 0,
  "relativeAnnualCosZ": 0,
  "relativeAnnualSinX": 0,
  "relativeAnnualSinY": -0.4820580723705152,
  "relativeAnnualSinZ": -0.0011619066758328245
},
"mars-deferent-e": {
  "relativeAnnualStart": 0,
  "relativeAnnualSpeed": 6.283185307179586,
  "relativeAnnualCosX": 0,
  "relativeAnnualCosY": 0,
  "relativeAnnualCosZ": 0,
  "relativeAnnualSinX": 0,
  "relativeAnnualSinY": -0.4820580723705152,
  "relativeAnnualSinZ": -0.0011619066758328245
}
}
```

It is evaluated as:

```text
R(t) = C cos(wt - phase) + S sin(wt - phase)
```

`relativeAnnualSpeed = 2π` gives one cycle per model year. The maximum
displacement is approximately `0.482` internal model units and lies almost
entirely along model Y.

In the preceding implementation, Mars, Mercury and Venus each contained an
untilted annual carrier of radius `100`. The Sun also had a radius-100 annual
motion, but with a small inclination of approximately `0.2762°`. Their
body-minus-Sun calculation therefore cancelled almost all of the two carriers,
but not this small component:

```text
100 × sin(0.2762°) ≈ 0.48206
```

The explicit residual fields were introduced solely to retain that component
after removing the duplicated absolute carriers. They were not fitted to JPL and
do not represent a newly proposed perturbation. Keeping them is what allowed the
full hierarchy migration to preserve every accepted ephemeris value.

Relative to the current local orbital radii, their approximate maximum scale is:

| Body | Relative displacement | Simplified maximum angular scale |
|---|---:|---:|
| Mercury | `1.25%` | about `0.71°` |
| Venus | `0.67%` | about `0.38°` |
| Mars | `0.32%` | about `0.18°` |

These angles are geometric scale estimates, not predicted constant offsets or
RMS changes. The observed effect is annual and depends on date, viewing direction
and all later transforms. Removing the residual would therefore not shift every
body by the same `0.4°`.

The common term may represent an inherited frame convention rather than three
independent physical motions. It has therefore been removed from the active
settings while its original values remain above as a reversible reference.

The zero-residual experiment found:

- Mercury absolute RA mean improved by `80.8%`, while angular RMS worsened by
  `0.42%`.
- Venus absolute RA mean improved by `32.0%` and angular mean by `3.2%`, while
  angular RMS worsened by `3.0%`.
- Mars absolute declination mean improved by `2.5%`, while angular RMS worsened by
  `3.9%`.
- Sun, Moon and all outer planets remained unchanged.

The active choice prioritizes the cleaner parent-relative geometry and improved
mean biases, while retaining the option to restore the former values or refine
local planes, centres and phases. Full results are in
[`zero_common_annual_residual_report.md`](reports/zero_common_annual_residual_report.md).

Eros must be investigated separately. Its larger and differently oriented
residual comes from its own former carrier plane and is not the same common term.

## Inheritance semantics

The remaining specialized relative-frame adapters inherit the Sun's world
**position** while retaining the binary frame's axes for their accepted local
orientation. Mercury and Venus no longer use those adapters: they inherit through
the normal render tree, and their local deferents explicitly counterrotate the
orientation that should not propagate into their orbital planes.

The remaining local stages are still meaningful:

- Mars deferent S and the Mars leaf define the companion path.
- Mercury/Venus single deferent, fixed plane and leaf define their local paths.
- Eros deferent B and leaf define its local path.
- Mercury's current deferent has zero radius but a non-zero centre/orientation and is not
  an identity transform.

## Settings and import contract

[celestial-model.json](../src/settings/celestial-model.json) is the schema-v3
single source of truth under ID `tychos-unified-binary-system`. It contains:

- the PVP reference frame;
- one record for each real celestial body and its `parentId`;
- every body's named `motion` components and numerical parameters;
- hierarchy-aware Edit Settings groups; and
- an internal `renderTree` that compiles the ordered transforms.

There is no separate `celestial-settings.json`. Nodes, planes and deferents are
motion terms owned by a body rather than entries in the astronomical body list.
The Edit Settings panel follows this same body/component structure, and its Save
action writes a complete reusable unified model.

Mercury, Venus and Mars have no `relativeAnnual*` properties. Eros retains those
fields because its distinct non-zero harmonic remains active and is exposed in
Edit Settings. Imports that try to restore former radius-100 Mars/Eros carriers
are rejected. Retired Mercury/Venus A/B entries are filtered so they cannot
silently recreate the deleted hierarchy. Other stable-ID and legacy-name imports
remain supported.

## Verification

The final schema-v3 unification was exported and compared with the saved
zero-residual full-binary baseline. Moving hierarchy and settings into one file,
and nesting the 36 motion components inside 15 real body records, caused no
coordinate change.

The frozen source values in
`scripts/derive_full_binary_settings.js` reproduce the accepted predecessor
over a dense -100 to +100 model-year grid.

| Gate | Result |
|---|---|
| Four direct carrier derivations | PASS |
| Maximum centre error | `2.3e-16` |
| Maximum annual error | `2.9e-14` |
| Source tests | 67 / 67 passed |
| Production build | PASS |
| Complete ten-body export | 759,756 non-metadata lines exactly identical |
| Direct Eros export | 75,969 displayed rows exactly identical |
| Sun–Mars diagnostic | All recorded numeric deltas exactly zero |
| Apparent true-of-date summaries | Zero numerical delta for all ten bodies |
| Residual/annual/FFT artifacts | 30 of 30 byte-identical |

The equivalence-baseline simulator export passes against
`00-backup/full-binary-baseline`. The only difference in that combined
ephemeris file is its generation timestamp. This completes the structural
migration without a scientific coordinate change. The active zero-residual
settings are a subsequent, intentional ephemeris refinement and are not expected
to pass this exact-equivalence gate.

The later Mercury/Venus simplification passes `72` tests across `14` suites and
the production build. Its matched `1800-2026` daily apparent true-of-date
comparison produced the following changes against the immediately preceding
hierarchy:

| Body | RA RMS | Dec RMS | Angular mean | Angular RMS |
|---|---:|---:|---:|---:|
| Mercury | `14.5%` better | `1.1%` better | `10.3%` better | `11.7%` better |
| Venus | `1.5%` better | `46.0%` better | `13.2%` better | `9.5%` better |

Mercury's signed declination mean moved from `+0.188732°` to `+0.347652°` even
though declination RMS improved slightly. The refactor is therefore accepted as a
strong overall result with that explicit remaining tradeoff.

## Moon geometry refinement

The Moon refinement now uses a smaller and more coherent geometry. The node and
plane remain explicit. The former separate `moon-anomalistic-tangent` stage has
been replaced by a classical equant-like circle-and-ray construction, and the
former separate solar-variation object has been folded into the same
solar-coupled frame as the `2D-M` eccentric contribution:

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

The equant reduced the dominant `27.552`-day anomalistic residual from about
`3.006°` to `0.027°`. A subsequent diagnostic found a stable pure-`2D` residual:
its period and phase were reproduced from the model's own Sun-Moon elongation,
and no fitted calendar period is stored. Adding that vector to the existing
solar-coupled frame reduced its exact residual amplitude from about `0.483°` to
`0.0033°`.

On the dense `2000-2026` apparent true-of-date comparison, the current Moon has
RA mean/RMS `-0.230071° / 0.309603°`, declination mean/RMS
`-0.001538° / 0.205922°`, and angular-separation mean/RMS
`0.326085° / 0.361032°`. Relative to the immediately preceding equant-plus-
`2D-M` baseline, RMS improved by `32.9%`, `14.2%` and `28.0%`, respectively.

The modern point-by-point distance audit gives mean error `+313 km`, RMS
`3,049 km`, and maximum absolute error `5,447 km`. At the `2015-03-20` eclipse
sample the error is about `-4,827 km`.

The argument forms are independently meaningful in standard lunar astronomy:
NASA material lists lunar variation with `2D` and evection with `2D-g`, where
`g` is lunar mean anomaly. This supports the selected relationships, but not a
claim that NASA endorses the TYCHOS mechanism; here they are expressed through
internal moving geometry rather than conventional analytical perturbations.

The final pure-`2D` state was then independently validated from `1800-2026` at
daily cadence (`82,546` samples). It returned RA mean/RMS
`-0.208460° / 0.295290°`, declination mean/RMS
`-0.001161° / 0.203339°`, and angular-separation mean/RMS
`0.312773° / 0.348833°`. Historical distance RMS is `3,048.7 km`, only `0.4 km`
different from the dense modern result. The geometry therefore transfers across
more than two centuries without degradation.

See [moon_model.md](moon_model.md) for the complete hierarchy, parameters,
methodology, distance audit, interpretation limits and rejected experiments.

## After equivalence is confirmed

The clean hierarchy makes later questions easier to isolate:

- whether Mercury and Venus should share a physically defined solar-equatorial
  plane while preserving the now-simplified local branches;
- whether any direct annual residual has a simpler TYCHOS geometric explanation;
- whether a local deferent can be removed without losing accepted observables;
- how transit-relative Mercury/Venus observables behave; and
- which changes improve independent intervals rather than only fitted data.

Those are physical-model experiments and may legitimately change ephemerides.
They should begin only after this migration's end-to-end equivalence is recorded.
