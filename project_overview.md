# TYCHOSIUM: model refinement and current state

## Scope

This document is a concise account of what the TYCHOSIUM refinement project has
achieved. It describes the retained model, its guiding method, and the broad
before/after evidence. It is **not** a chronology of every experiment, and it
does not claim that agreement with JPL establishes a cosmological conclusion.

The project began with a focused practical problem: the original Tychosium Moon
had substantial declination error. It grew into two connected pieces of work:

1. improve the geometry and validation of the Moon and selected planetary
   branches; and
2. make the software state the intended TYCHOS parent–child relationships
   directly, rather than leaving important relationships implicit in separate
   absolute motion chains.

The resulting system is still a geometrical model. A position is obtained from
the hierarchy of rotations, planes, centres and local orbits before coordinates
are exported. No fitted right-ascension, declination, longitude or distance term
is added afterwards.

The original Tychosium was already a capable working simulator, but much of its
astronomical arrangement was expressed in specialised JSX components and
separate settings records. The refinement made the hierarchy an explicit part
of the model definition.

In broad terms, the retained arrangement is:

```text
System centre / PVP reference              
└─ Earth                                   
   ├─ Moon                                 
   │  ├─ nodal / plane frame
   │  ├─ apsidal geometry
   │  ├─ lunar modulations
   │  └─ Moon orbit
   └─ Sun–Mars binary frame
      └─ Sun
         ├─ Mars
         │  ├─ Phobos
         │  └─ Deimos
         ├─ Venus
         ├─ Mercury
         ├─ Jupiter, Saturn, Uranus, Neptune and Pluto
         └─ smaller bodies including Halley and Eros
```

The main architectural result is parent-relative inheritance. Sun-hosted
bodies inherit the Sun's world translation and retain only their own local
orientation, centre displacement, plane and orbit. Where a local
counterrotation is required, it cancels an inherited orientation only; it does
not erase the parent body's translated position. This makes the intended
relationships inspectable rather than duplicated in independent chains.

## The new lunar model

The Moon was the largest refinement because it required both a geometrical
solution to the initial declination problem and a way to address the remaining
angular and distance behaviour without placing an analytical correction at the
end of an ephemeris calculation.

The Moon has long been one of the most difficult bodies to model accurately.
Its apparent motion contains several recurring inequalities and distance
variations, and modern lunar ephemerides likewise require high-fidelity
dynamical models and thousands periodic effects to predict position and distance
closely.

This difficulty was already recognised within the historical Tychonic
tradition. Tycho Brahe and Christian Longomontanus used moving centres,
epicyclic constructions and libration-like geometry in their lunar work. Their
models were not identical to the one implemented here, but they demonstrate an
important historical point: an unmodulated circular Moon orbit with a fixed
Earth-centred construction was not considered sufficient to reproduce the
observed lunar inequalities.

The present TYCHOS implementation explores the same broad geometrical
possibility without claiming to reproduce the historical theory. It retains a
uniform local circular motion for the Moon, while allowing the centre from
which that circle is evaluated to undergo small, explicit, geometry-dependent
displacements. The Earth–Sun–Moon stage intentionally derives its vector
directions from the live Earth–Sun, Earth–Moon and apsidal geometry, producing
the phase relationships conventionally written `2D−M` and `2D`. The Earth–Moon
stage derives a coordinated radial resultant from the live Moon–apsidal
relationship. These are operational phase relationships in the geometry, not
an accidental numerical resemblance; what the model avoids is adding them as
finished analytical longitude corrections.

The distinction is essential: none of these mechanisms is a numerical patch
applied to the Moon's final coordinates. They are visible pre-export vector
constructions. Their combined motion changes the resulting Earth-centred path,
and can therefore affect both apparent direction and distance.

The current retained Moon hierarchy is:

```text
Earth
└─ Moon
   ├─ Lunar Nodal / Plane Frame
   ├─ Lunar Apsidal Frame
   ├─ Lunar Modulation Frame
   │  └─ Earth–Sun–Moon Modulations
   │     ├─ 2D−M solar modulation
   │     ├─ 2D solar modulation
   │     └─ Earth–Moon modulation
   └─ Moon Orbit
```

The nodal/plane frame separates two things which should not be conflated: the
amount of lunar inclination and the changing direction of that inclined plane.
Making both explicit resolved the original declination issue geometrically.

In simple terms, begin with a hypothetical lunar circle aligned with the
Earth's equatorial plane. The **plane** stage tilts that circle by the required
amount. The **node** then tells the model which direction that tilt faces and
allows that direction to regress over time. A plane does not need a node merely
to be inclined; the node is needed because the *orientation of the inclined
plane* is itself part of the lunar motion. Treating those roles separately is
why the model can address declination without disguising the effect as a
coordinate correction.

The apsidal geometry then moves the centre from which the local lunar orbit is
constructed. The Moon retains a declared local circular orbit and base uniform
rotation. The additional stages move its *centre* before that orbit is
evaluated, so the resulting Earth-centred position can vary in both direction
and distance without a post-export coordinate patch.

### Earth–Sun–Moon modulations

The two solar terms use the familiar relative arguments commonly written
`2D−M` and `2D`: relationships associated in historical lunar work with
evection and variation. They are not entered as fitted longitude corrections.
Instead, the instantaneous Earth–Sun–Moon and apsidal directions orient small
centre-displacement vectors within the model. The associated settings provide
the **size** of those vectors; they do not supply a separately fitted period or
phase.

Here, `D` is the Sun–Moon elongation as seen from Earth and `M` is the lunar
apsidal/anomalistic phase. Thus these are not arbitrary calendar frequencies:
their values change as the already-declared Earth, Sun and Moon geometry
changes. At every evaluation, the model derives the relevant direction from
those current geometric phases, then applies the corresponding fixed-radius
vector. It does not append `sin(2D−M)` or `sin(2D)` to a finished lunar
longitude.

This is why the word **modulation** is useful. Constant-amplitude vectors can
add, reinforce or partly cancel as their relative phases change. The resulting
centre displacement changes even though no individual component is a lookup
table or a date-specific correction. The supplied conceptual notes give two
useful ways to understand this distinction:

- the same angular relationships can be implemented as a moving-centre
  geometry rather than as terms appended to a final longitude; and
- phase-dependent vector superposition is an appropriate mathematical analogy,
  without asserting an electromagnetic physical cause.

The model therefore remains deliberately neutral about the underlying physical
mechanism. It demonstrates a compact geometry that works well numerically; it
does not establish that this is the unique explanation of lunar motion.

### Earth–Moon modulation

The paired-radial mechanism was retained only after tests of simpler existing
geometry and several alternative additions. It is one geometrical mechanism
implemented through two coordinated centre-displacement vectors in the moving
lunar plane. Their symmetry cancels the tangential parts and leaves a radial
resultant governed by the Moon's direction relative to the apsidal direction.

More specifically, let the current uncorrected Earth–Moon direction be
`θ` and the apsidal direction be `ω`. The operation constructs two equal-scale
vectors: one at `ω`, and its mirror around the Moon direction at `2θ−ω`. Their
sum lies along `θ`; the sideways parts cancel. One radius setting controls the
scale of both vectors, while their changing directions are computed from the
current Earth–Moon and apsidal geometry. There is no separately fitted
paired-radial period or phase.

This gives the term *Earth–Moon modulation* a precise, limited meaning: it is
a phase-dependent displacement determined by the Earth–Moon and apsidal
relationship. It does not claim an identified physical force, and it is not an
analytical correction fitted to a residual series.

This is important to state precisely: the paired action does **not** expand or
contract the Moon's local circular orbit, and it does not impose a variable
angular speed around that local circle. It supplies an additional displacement
of the local orbit's centre. The final Earth-centred path consequently changes
in distance and apparent rate, while the base local orbit remains the declared
circle.

The resulting construction is comparatively simple, visible in the hierarchy,
and related to historically debated moving-centre and epicyclic lunar
geometries, including work associated with Tycho Brahe and Longomontanus. It is
not presented as a reconstruction of their exact theory, nor as a final lunar
solution. Other geometries may be possible and the remaining residual structure
deserves continued study.

## Venus and Mercury: solar branches with their own planes

Venus and Mercury are represented as Sun-hosted branches rather than as
independent Earth-hosted absolute chains. Each inherits the Sun's translated
world position through the hierarchy, then applies only its own local geometry:

```text
Sun
├─ Venus deferent → Venus plane → Venus orbit
└─ Mercury deferent → Mercury plane → Mercury orbit
```

The two plane stages are not decorative. Venus and Mercury require their own
local orbital orientation and small centre/tilt relationships. The deferent
stages also manage local orientation relative to the inherited annual Sun
motion; where needed, a counterrotation prevents a parent's orientation from
being unintentionally imposed on a child's local plane. This preserves parent
translation while keeping each inner body's geometry explicit and editable.

Mercury remains a special validation case. It is visible from Earth for only
limited windows around its greatest elongations, so an all-date geocentric
residual is not the sole criterion of interest. The practical priority is that
the geometry continue to represent the timing and placement of Mercury's solar
transits at least as well as the retained earlier configuration. The project
therefore treats broad Mercury residuals as a diagnostic, but gives
transit-focused checks greater decision weight than a small improvement in a
global average.

## What improved

Using 1800–2026 daily interval as a comparisson baseline, with
82,546 samples and the same JPL true-of-date reference. The following
is therefore a direct A/B summary for those saved configurations.

For the seven shared, relatively non-exceptional branches — Sun, Venus, Mars,
Jupiter, Saturn, Uranus and Neptune — the average absolute coordinate bias and
average residual magnitude changed approximately as follows:

| Aggregate metric | Original saved run | Current saved run | Direction |
|---|---:|---:|---:|
| Mean absolute RA bias | `0.243°` | `0.063°` | about 74% lower |
| Mean absolute declination bias | `0.134°` | `0.044°` | about 67% lower |
| Mean angular separation | `0.489°` | `0.290°` | about 41% lower |
| Average RA RMS | `0.543°` | `0.308°` | about 43% lower |
| Average declination RMS | `0.256°` | `0.173°` | about 33% lower |
| Average angular-separation RMS | `0.590°` | `0.342°` | about 42% lower |

In practical terms, the aggregate reduction in mean RA bias is about eleven
arcminutes, the declination-bias reduction is about five arcminutes, and the
mean angular-separation reduction is about twelve arcminutes. The reality is 
most of the gains came from adjusting the planets parameters and testing more
than related to a modification of the hierarchy of the code. 

The exceptional bodies should be read separately:

- **Moon:** mean angular separation changed from `3.834°` to `0.291°` and
  angular RMS from `4.114°` to `0.325°`: roughly 92% lower on this shared
  long-span comparison. This is the principal numerical result of the lunar
  geometry work.
- **Pluto:** it was historically the least refined branch. Its saved mean
  angular separation changed from `8.240°` to `2.135°`, and angular RMS from
  `9.686°` to `2.352°`: roughly 74% and 76% lower. RA improved especially
  strongly, but the remaining declination behaviour and the current positive
  declination mean bias shows Pluto is still a separate refinement problem, not
  a completed solution.
- **Mercury:** ordinary all-date aggregate error is not the only useful
  criterion; transit behaviour and visibility geometry require dedicated
  validation.

## How the work was validated

The project built a repeatable analysis workflow rather than relying on visual
impressions alone. It can compare TYCHOS outputs with selected JPL products,
record RA, declination and angular-separation means and RMS values, retain
residuals and annual summaries, inspect dominant periodic signals, audit
geocentric Moon distance, examine Mercury transits, and preserve baselines for
later comparison.

This work also clarified a methodological limit: a reference-frame mismatch can
look like a long-term orbital error. Consequently, J2000/ICRF products and
apparent true-of-date products must only be compared with compatible TYCHOS
exports. JPL agreement is used here as a reproducible coordinate-agreement
measure, not as a proof of either system's physical interpretation.

## Current status

The current state is a clearer, hierarchy-aware Binary TYCHOS implementation
with a materially stronger lunar model, better measured planetary baselines,
and a reproducible route for future research. It does not settle the physical
cause of the lunar modulations, prove the uniqueness of any geometry, or make
every planetary branch definitive.

Its strongest result is the combination of two things:

1. the intended TYCHOS relationships are now represented directly in software;
2. improvements are expressed as declared pre-export geometry rather than
   hidden coordinate corrections.
