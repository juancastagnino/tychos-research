# TYCHOS research and model-development summary

## Purpose of this document

This document summarizes the principal work completed during the TYCHOS and
Tychosium research project. It covers the evolution from a focused Moon
declination repair into a broader investigation of the model hierarchy,
ephemeris accuracy, reference frames, planetary refinement and research tools.

It is not a claim that agreement with JPL proves the TYCHOS cosmology. The work
has a narrower and more practical purpose:

- express the intended TYCHOS relationships coherently in software;
- preserve the model's geometric method;
- identify and correct implementation problems;
- measure ephemerides consistently;
- refine geometric parameters where the evidence transfers across time; and
- distinguish genuine model geometry from empirical output correction.

For implementation detail, see [binary_tychos.md](binary_tychos.md). For the
complete Moon derivation, see [moon_model.md](moon_model.md). For the current
working state and constraints, see [README_handoff.md](README_handoff.md).

## How the project began

The original goal was comparatively small: investigate why the Tychosium Moon
showed excessive declination error.

The solution was to make the Moon's orbital plane and node explicit. That first
change was important for two reasons. It improved the declination geometrically,
and it demonstrated that the software hierarchy could be made more faithful to
the conceptual TYCHOS structure without applying corrections to the final
ephemeris.

From that point, the work expanded into a general research program. The same
questions were applied to the rest of the model:

- Does the code hierarchy express the relationships proposed by TYCHOS?
- Are bodies inheriting motion from their intended parent, or repeating it in
  independent absolute definitions?
- Are discrepancies caused by orbital geometry, reference-frame conventions,
  coordinate export or analysis mistakes?
- Can recurring residual patterns be explained by visible geometric stages?
- Do improvements transfer to independent intervals?

## Methodological rule: geometry before correction

The project adopted a strict rule: TYCHOS ephemerides must emerge from the core
astronomical geometry.

Residual, annual and Fourier analyses are diagnostic instruments. They can
identify a frequency, phase relationship or geometric layer worth studying, but
their fitted values must not be inserted into the final coordinates.

The following techniques are therefore excluded:

- fitted perturbation terms added directly to longitude;
- body-specific RA or declination patches;
- lookup tables and splines derived from JPL differences;
- date-dependent offsets;
- post-export corrections; and
- hidden analysis code that modifies the simulator.

A new mechanism is acceptable only when it represents an explicit geometric
hypothesis, participates in the model before coordinate calculation, can be
tested independently and remains understandable within the hierarchy.

Numerical calibration is still legitimate. Every astronomical model requires
choices of phase, speed, radius, tilt, centre and orientation. The distinction
is that a calibrated geometric parameter defines a model element; it does not
overwrite the result after the model has run.

## Rebuilding the hierarchy

### Earlier organization

The preceding Tychosium contained correct and useful accumulated mathematics,
but several major paths were expressed as largely independent chains beneath
Earth. A simplified description was:

```text
Earth
├─ Moon
├─ Sun
├─ Mars independent deferent chain
├─ Mercury independent deferent chain
├─ Venus independent deferent chain
└─ other planetary chains
```

Some descendants repeated motion already represented by the Sun. This made the
software harder to interpret as the TYCHOS system described conceptually.

### Current native binary organization

The model is now organized approximately as:

```text
SystemCenter                         PVP geometric reference
└─ Earth                             Earth/PVP path
   ├─ Moon Node
   │  └─ Moon Plane
   │     └─ Moon geometry
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

`SystemCenter` is a coordinate reference associated with the PVP geometry. It is
not treated as a physical body, barycentre or cause of motion. The model remains
Tychonic: the Sun is positioned relative to Earth, while the solar subsystem is
organized beneath the Sun.

The Sun-Mars description is deliberately asymmetric. No conventional
mass-defined barycentre, equal orbital radius or forced opposition was imposed.
The hierarchy expresses the primary/companion relationship while preserving the
accepted TYCHOS motion.

## From visual hierarchy to native parent-relative settings

The first hierarchy migration preserved positions by reconstructing the old
absolute chains and subtracting the Sun chain at runtime. This proved that the
new organization could be equivalent, but some settings still spoke the language
of the former absolute model.

The full migration converted Mars, Mercury, Venus and Eros into genuinely
Sun-relative definitions. Their descendants inherit the Sun's world position
and contribute only their local centre, orientation and motion.

A later simplification completed this idea for Mercury and Venus. Their temporary
parent-relative A carriers, separate B/secondary records and body-specific JSX
adapters were removed. The active branches are now ordinary declarative chains:

```text
Sun
├─ Venus deferent -> Venus Plane -> Venus
└─ Mercury deferent -> Mercury Plane -> Mercury
```

The Sun supplies world position through parent inheritance. Each remaining local
deferent counterrotates the inherited annual orientation and retains only the
radius, centre or tilt required by that body. Mars and Eros continue to use the
specialized parent-relative carrier mechanism because their established geometry
has not undergone the same reduction.

The change was performed in stages:

1. Build the declarative hierarchy while preserving the old numerical paths.
2. Verify exact equivalence with raw exports and diagnostic CSV files.
3. Algebraically derive parent-relative carrier values.
4. Remove duplicated radius-100 absolute carriers.
5. Unify hierarchy and numerical settings into one source of truth.

The resulting astronomical core is `src/settings/celestial-model.json`. It
contains real bodies, parent relationships, owned motion stages, numerical
parameters, editor grouping and the render tree. Nodes, planes and deferents are
motion components owned by bodies rather than false celestial bodies.

The migration passed exact-equivalence tests before scientific refinements were
allowed. Complete exports, Eros exports, Sun-Mars diagnostics, summary metrics
and residual artifacts were compared against preserved baselines.

## What “legacy mathematics” means

The new hierarchy did not attempt to rediscover every orbit from zero. Accepted
phases, radii, tilts, speeds and deferent relationships from the preceding model
were treated as established starting values.

This does not mean a hidden second model remains active. It means the hierarchy
was changed first while preserving proven numerical behavior. Once equivalence
was established, individual geometric assumptions could be tested without
confusing a structural migration with an astronomical refinement.

## Single-file astronomical core and settings workflow

Hierarchy and astronomical parameters were consolidated into
`celestial-model.json`. The Edit Settings interface follows the same body and
motion-component organization.

The Save Settings and Load Settings paths were repaired so researchers can:

- edit a parameter in the interface;
- save the complete unified model;
- reload that model later; and
- recover the same hierarchy and numerical state.

Stable component IDs and selected legacy names remain for import compatibility.
Obsolete Mars/Eros absolute carriers are rejected where mixing them with the
parent-relative model would be unsafe. Retired Mercury/Venus A/B records are
filtered so old settings cannot silently reconstruct the removed hierarchy.

## Reference-frame investigation

Long comparisons initially showed a common angular rotation between TYCHOS and
JPL. Code inspection found that the native Tychosium frame moves with the model's
PVP orientation, while standard JPL comparisons commonly use a fixed J2000/ICRF
orientation.

This is a coordinate-frame issue, separate from orbital accuracy. Comparing a
moving native frame directly with fixed J2000 can create a large apparent drift
over centuries even when relative body geometry is unchanged.

Development branches therefore added two TYCHOS export modes:

- native TYCHOS/PVP frame;
- J2000/ICRF comparison frame.

The research workflow also supports appropriate JPL products:

- fixed J2000/ICRF;
- apparent true-of-date, including the relevant date-dependent orientation and
  apparent-observation conventions.

The intended comparisons are:

```text
TYCHOS J2000 export  vs JPL J2000/ICRF
TYCHOS native export vs JPL apparent true-of-date
```

These products are not claimed to be physically identical. They are the most
useful controlled comparisons for separating frame rotation from orbital
geometry. A report set produced against one reference product must never be
numerically compared as though it used the other.

The optional J2000 TYCHOS exporter remains a development and research facility,
not a required change to the public native presentation of TYCHOS.

## Research and analysis infrastructure

The project developed a reproducible workflow around the simulator:

- automated JPL Horizons downloads;
- explicit reference-product selection;
- parsing of TYCHOS, JPL and Stellarium exports;
- RA, declination and angular-separation statistics;
- annual summaries;
- residual CSV generation;
- Fourier diagnostics;
- baseline-to-candidate summary comparison;
- Mercury transit checks;
- Sun-Mars relative-system diagnostics;
- Eros before/after equivalence gates; and
- Moon point-by-point geocentric distance auditing.

Generated data and reports are deliberately separated from the astronomical
core. Analysis scripts observe the model; they do not alter it.

Baselines preserve settings, raw exports, analysis configuration and reports
together. This is essential because changing cadence, time interval, reference
frame or apparent-coordinate convention can change the resulting statistics.

## Planetary refinements

After the hierarchy migration, existing TYCHOS parameters were refined through
repeated long-baseline tests. These changes adjust explicit centres, phases,
tilts, radii and speeds; they do not introduce external perturbations.

### Pluto

Pluto was historically the least refined major body. Large improvements were
found by adjusting its phase, three-dimensional centre and deferent orientation.
Over the long `1800-2026` daily comparison, the retained configuration reduced:

- RA RMS by about `80%`;
- angular mean by about `74%`; and
- angular RMS by about `76%`.

The active Pluto values ultimately follow the author's preferred revision,
including the later speed `0.02545039`. A research-optimized alternative remains
documented because it performed better on some JPL aggregate metrics. This is an
intentional distinction between author-selected model interpretation and pure
error minimization.

### Jupiter

Small adjustments to phase, speed, centre and orbital tilt produced substantial
long-baseline gains:

- RA RMS improved by about `28%`;
- declination RMS by about `51%`; and
- angular RMS by about `33%`.

### Saturn

Refinement of phase, speed, deferent radius, centre and local orbit centre gave:

- RA RMS improvement of about `34%`;
- declination RMS improvement of about `23%`; and
- angular RMS improvement of about `34%`.

### Mars

Mars received smaller direct refinements to phase, centre and tilt while
preserving its established binary-companion geometry. The long comparison gave:

- RA RMS improvement of about `9%`;
- declination RMS improvement of about `16%`; and
- angular RMS improvement of about `11%`.

The established `Mars deferent E orbitCenterb = -20` was retained rather than
fractionally optimized because it is a directly meaningful TYCHOS value.

### Mercury and Venus

Early work tested Mercury and Venus as solar satellites using the existing
counter-rotating deferent structure. This showed that the solar-moon concept is
geometrically viable and that Mercury and Venus should not be forced onto one
identical numerical plane.

Separate explicit plane objects were later introduced as an equivalence-preserving
architectural expression. An intermediate migration still used special A/B
carrier stages and custom Sun-relative components. Those layers have now been
reduced to one deferent, one plane and one orbit for each body.

Venus's former A-carrier centre was algebraically expressed in the new local
basis and absorbed into the Venus plane. Mercury's former A vertical offset was
transferred into its plane. These transformations were derived from the prior
model rather than fitted against JPL.

In the final native hierarchy they are direct solar moons under the Sun branch:
they inherit the Sun's translation normally, while their local deferents cancel
only the unwanted inherited annual orientation. The deferents remain necessary
because Venus still has its own small radius and tilt, and Mercury retains a
non-zero centre and tilt.

Long validation from `1800-06-21` through `2026-06-21` at one-day cadence found:

| Body / metric | Previous hierarchy | Current hierarchy | Change |
|---|---:|---:|---:|
| Mercury RA RMS | `2.620184°` | `2.241029°` | `14.5%` better |
| Mercury Dec RMS | `0.998030°` | `0.987340°` | `1.1%` better |
| Mercury angular mean | `2.148367°` | `1.926522°` | `10.3%` better |
| Mercury angular RMS | `2.690188°` | `2.375774°` | `11.7%` better |
| Venus RA RMS | `0.422059°` | `0.415547°` | `1.5%` better |
| Venus Dec RMS | `0.209577°` | `0.113124°` | `46.0%` better |
| Venus angular mean | `0.355078°` | `0.308311°` | `13.2%` better |
| Venus angular RMS | `0.447191°` | `0.404515°` | `9.5%` better |

Mercury's signed mean declination bias worsened from `+0.188732°` to
`+0.347652°`, despite the slight declination-RMS improvement. This is the main
known tradeoff in an otherwise clearly better overall comparison.

Mercury's longitude remains more difficult than its latitude. Transit-focused
validation is more informative than assuming every moment of its geocentric JPL
curve should receive equal interpretive weight.

## The Moon: from declination repair to solar-coupled geometry

The Moon became the clearest example of the project's method: use residuals to
identify missing geometry, but never paste a fitted correction onto the exported
coordinates.

### Node and plane

The first major improvement separated the amount of orbital inclination from
the changing direction of its node. This corrected the original declination
problem and made the geometry visible to rendering, calculation, export and
editing.

### Current compact hierarchy

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

The former separate `moon-anomalistic-tangent` stage has been superseded by a
classical equant-like circle-and-ray geometry. This preserves a circular lunar
path while producing the required non-uniform angular progression. The former
separate solar-variation object is now simply a second vector inside the same
solar-coupled frame as the `2D-M` contribution.

This is simpler than the previous three-object experiment and makes the division
of responsibilities clearer:

- node and plane control orbital orientation;
- the apsidal deferent and equant control anomalistic timing;
- one solar frame supplies the two demonstrated Sun-Moon relationships;
- the Moon orbit remains the final local path.

The equant reduced the dominant `27.552`-day residual amplitude from about
`3.006°` to `0.027°`. A later diagnostic isolated a stable pure-`2D` signal with
about `0.483°` amplitude. Its phase and period were independently reproduced
from TYCHOS's internal Moon-Sun elongation. After adding that vector, the exact
pure-`2D` residual fell to about `0.0033°`.

The argument forms also have established lunar meaning. NASA lunar material
lists variation as `sin(2D)` and evection as `sin(2D-g)`, with `g` representing
lunar mean anomaly. This independently supports the relationships being used;
it does not imply NASA endorsement of the TYCHOS physical mechanism. TYCHOS
expresses them as moving geometry rather than final analytical longitude terms.

### Principal Moon parameters

| Component | Parameter | Value |
|---|---|---:|
| Lunar node | `startPos` | `-296°` |
| Lunar node | `speed` | `-0.33780566` |
| Lunar plane | `orbitTilta / orbitTiltb` | `0.1° / -5.2°` |
| Lunar apsidal deferent | `startPos` | `167.51°` |
| Lunar apsidal deferent | `speed` | `0.71015440177343` |
| Lunar apsidal deferent | `orbitRadius` | `0.01407` |
| Lunar apsidal equant | `orbitRadius` | `0.01407` |
| Solar-coupled `2D-M` | `orbitRadius` | `-0.0055` |
| Solar-coupled pure `2D` | `solarVariationRadius` | `0.002168` |
| Moon orbit | `startPos` | `318°` |
| Moon orbit | `speed` | `83.28521004` |
| Moon orbit | `orbitRadius` | `0.25695552897999907` |

### Current modern validation

The final state was compared with JPL apparent true-of-date from `2000-06-21`
to `2026-06-21`, using `75,969` samples at three-hour cadence:

| Coordinate | Mean difference | RMS |
|---|---:|---:|
| Right ascension | `-0.230071°` | `0.309603°` |
| Declination | `-0.001538°` | `0.205922°` |
| Angular separation | `0.326085°` | `0.361032°` |

Against the immediately preceding equant-plus-`2D-M` baseline, RMS improved by
`32.9%` in RA, `14.2%` in declination and `28.0%` in angular separation. Mean
angular separation improved by `27.5%`.

### Current modern distance audit

| Statistic | Result |
|---|---:|
| Mean TYCHOS minus JPL | `+313 km` |
| RMS distance error | `3,049 km` |
| Mean absolute distance error | `2,722 km` |
| 95th-percentile absolute error | `4,722 km` |
| Maximum absolute error | `5,447 km` |

At the `2015-03-20` eclipse sample, TYCHOS gives approximately `353,059 km`
versus JPL's `357,886 km`, an error of about `-4,827 km`.

### Important Moon limits and negative results

Static centre offsets, a lunar-only eccentric frame, and independently rotating
centres either failed or degraded the solution. Separating a large tangential
device from the radial geometry also made the distance behaviour difficult to
interpret. The successful model instead distinguishes apsidal timing from
solar-lunar geometry using one equant and one solar-coupled frame.

### Historical transfer validation

The final pure-`2D` state was independently compared from `1800-06-21` to
`2026-06-21` at daily cadence (`82,546` timestamps):

| Coordinate | Mean difference | RMS |
|---|---:|---:|
| Right ascension | `-0.208460°` | `0.295290°` |
| Declination | `-0.001161°` | `0.203339°` |
| Angular separation | `0.312773°` | `0.348833°` |

Historical distance RMS is `3,048.7 km`, compared with `3,049.1 km` in the
dense modern run. Mean historical distance error is `+315 km` and maximum
absolute error is `5,435 km`. The near-identical modern and 226-year distance
results, together with slightly lower historical angular RMS, show that the
geometry transfers rather than merely fitting the development interval.

## Additional software improvements

### Observer trace

An observer-trace tool was developed for visualizing the path of an observer or
selected bodies through discrete model steps. Its sampling was revised so Play
mode can trace at model-step intervals rather than connecting arbitrary animation
timestamps. Controls include trace length, line width, dotted rendering,
observer latitude/longitude and Earth opacity. Dotted trace rendering is the
preferred default presentation.

The trace remains a separate visualization feature and does not influence the
astronomical model or exported coordinates.

### Edit Settings reliability

Settings save/load behavior was corrected so UI changes are actually serialized
and restored. Stable internal IDs prevent display-name changes from altering the
hierarchy or ephemerides.

### Visual and coordinate consistency

Where new planes, nodes or parent-relative stages were introduced, both the live
visual model and the hidden plot/export model were updated. This prevents a
visually correct hierarchy from silently producing coordinates from an obsolete
one.

## What the project demonstrates

The work demonstrates that:

- the TYCHOS hierarchy can be represented declaratively and coherently in code;
- major structural changes can be made with exact equivalence before refinement;
- the Moon's original declination problem has a natural plane-and-node solution;
- solar-relative lunar geometry can improve both direction and distance;
- an equant can represent anomalistic angular timing without a separate
  tangential pseudo-object;
- the established `2D` and `2D-M` argument patterns can be generated from
  internal TYCHOS directions rather than stored fitted periods;
- meaningful planetary gains can be achieved by refining existing TYCHOS
  parameters;
- reference-frame conventions can dominate long-interval comparisons; and
- independent-interval validation is essential for distinguishing structural
  improvement from local fitting.

## What the project does not demonstrate

The work does not establish that:

- JPL is the physical truth in every interpretive question;
- agreement with JPL proves TYCHOS cosmology;
- the current geometry is unique;
- every software stage has the definitive interpretation intended by the book;
- every major body is fully refined; or
- remaining discrepancies should be hidden with additional parameters.

The comparison products are measurement tools. The astronomical and conceptual
interpretation remains a separate discussion with the TYCHOS authors.

## Current status and recommended next work

The native binary hierarchy and single-file astronomical core are established.
Mercury and Venus now use the accepted compact `deferent -> plane -> orbit`
structure and the implementation passes `72` tests across `14` suites plus the
production build.
The current compact Moon should be preserved as the accepted modern experimental
baseline. Both solar-coupled radii and the equant geometry are declared in the
single model file and pass through the normal settings workflow.

Recommended future work includes:

1. Preserve the current Moon settings, raw exports, modern reference products
   and completed `1800-2026` validation together.
2. Complete dense independent validation for the retained Jupiter, Saturn and
   Mars refinements.
3. Validate the compact Mercury/Venus hierarchy on the dense modern interval and
   continue transit-focused Mercury validation.
4. Investigate remaining annual and approximately `202-206` day Moon residuals
   only after identifying an explicit internal geometric relationship.
5. Continue separating reference-frame questions from orbital tuning.
6. Keep the observer trace and other visualization tools isolated from the
   astronomical coordinate pipeline.

The central achievement is not merely a collection of lower error statistics.
The software now expresses the intended TYCHOS relationships much more directly,
while its improvements remain testable, reversible and constrained by an
explicit geometric methodology.
