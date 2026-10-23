# Tychosium code architecture guide

> Branch update: this guide's equant implementation and update-order descriptions are historical. In `paired-radial-3d` the equant is removed; `MoonSolarCoupledEccentric.jsx` computes the paired displacement in the apsidal parent's lunar plane as well as the solar-coupled displacement. Both influence the model, including coordinate/export evaluation. The previous 2D branch uses world XZ. Consult the current source before applying earlier file-by-file details below.

Mercury keeps its ordinary Sun-hosted deferent, plane and orbit; the current transit-focused parameter experiment changes plane `orbitCenterb` to `0.6`. This is an experimental parameter adjustment, not a new adapter or demonstrated physical mechanism. See `binary_tychos.md` for comparison limitations.

## A note to the original developer

The original Tychosium code is the foundation of all this work. The research
branches grew through many small, measured experiments while the model was being
understood. That process produced useful geometry and strong validation, but it
also produced more infrastructure than would normally be designed in one clean
pass.

The local `main` branch remains the comparison reference for the original
Tychosium. The current work is isolated on experimental branches such as
`hierarchy-refinement`. Nothing in this guide proposes rewriting `main` before
the original developer has reviewed the approach and decided what, if anything,
should be retained.

The intended outcome of this guide is simple:

- explain what changed outside `celestial-model.json`;
- explain why those changes were made;
- distinguish required model code from research and compatibility code;
- answer whether the old `EphController.jsx` could have been updated directly;
- identify honest weaknesses and cleanup opportunities; and
- make it possible for the original developer to replace any implementation
  while preserving the tested astronomical behaviour.

For the astronomical rationale, see `binary_tychos.md` and `moon_model.md`.
This document is deliberately about software architecture.

## Short answer

The original architecture has not been discarded. Its central mechanism is
still present:

1. `Cobj` constructs and animates the visible model.
2. `Pobj` constructs a hidden mathematical copy of the model.
3. `EphController` advances the hidden model through time.
4. Ephemerides are read from the resulting Three.js world positions.

The principal architectural change is that the two trees are no longer written
manually and independently inside `SolarSystem.jsx` and `PlotSolarSystem.jsx`.
They are now generated from the same declared tree in
`celestial-model.json`.

Special geometry that cannot be expressed by the original fixed
`rotation + radius + child` pattern is implemented by a small set of transform
components. Each component supplies the same update operation to both paths:

- `useFrame(...)` updates the visible model;
- `updateAfterMotion(...)` updates the hidden plot/ephemeris model.

This was done to prevent the screen, traces, plots, checker and exported
ephemerides from silently using different astronomy.

The current solution is valid, but it is not beyond criticism. A cleaner final
architecture could move all geometry into renderer-independent functions that
return body matrices or positions for a requested time. Both React/Three.js and
`EphController` could consume that evaluator. The present code moves in that
direction, but it does not complete that separation.

## The important correction about `EphController`

The suggestion that the old `EphController.jsx` was itself a direct analytical
solver is understandable, but it does not match the original source.

The original controller already did this:

```js
movePlotModel(plotObjects, currentPos);
const data = getPlotModelRaDecDistance(name, plotObjects, scene);
```

It did not independently calculate Earth and every body from configuration
values. It advanced the rotations of the hidden `Pobj` hierarchy and then read
the resulting Three.js world positions.

Therefore, there are two different answers to the question:

> Could we simply update the old `EphController`?

### If the only objective were a different exported Moon position

Yes. A private Moon calculation could be placed in `EphController`, and the
exported coordinates could be changed with a comparatively small patch.

### If the objective is one coherent Tychosium model

No, not by changing only `EphController`.

That would leave the following consumers on the old geometry:

- the visible Moon;
- orbit and deferent guides;
- observer and camera views;
- traces;
- plots;
- the ephemeris checker;
- star/reference calculations that advance the plot model; and
- any code reading object world positions from the scene.

The application would then contain two models: one visible and one hidden inside
the exporter. It might produce better exported numbers, but the Tychosium would
no longer be displaying the geometry responsible for them.

The compact example based on `cos(sunAngle) * radius` is also not equivalent to
the current lunar model. The current Moon needs:

- the regressing nodal orientation;
- the inclined lunar plane;
- the apsidal centre geometry;
- the equant-defined non-uniform angular progress;
- actual Earth-to-Sun and Earth-to-Moon directions;
- the `2D-M` and `2D` geometrical arguments;
- conversion from the fixed ecliptic frame into the moving parent frame; and
- separate display-scale and physical-coordinate Moon branches.

That mathematics can certainly be expressed more compactly than the current
JSX hierarchy, but it is not just one Sun-angle translation.

## Original architecture

The original model had two manually duplicated JSX trees:

```text
SolarSystem.jsx
└─ hard-coded Cobj hierarchy
   └─ visible animated model

PlotSolarSystem.jsx
└─ hard-coded Pobj hierarchy
   └─ hidden mathematical model
      ├─ ephemerides
      ├─ plots
      ├─ traces
      ├─ checker
      └─ several star/reference operations
```

`Cobj` and `Pobj` were elegant generic components for the original problem.
Each setting described a centre, tilt, rotating orbit and radius. Nesting those
objects produced the accumulated transform.

This design had two important strengths:

- the geometry was visible as a transform hierarchy; and
- the hidden plot model reused Three.js matrix composition instead of
  duplicating all coordinate mathematics in `EphController`.

It also had two limitations once the research scope expanded:

1. The live and plot hierarchies had to be edited separately and kept identical
   by hand.
2. Some new mechanisms are not ordinary nested circular rotations. A lunar
   equant, a centre vector derived from live Sun-Moon elongation, or a translated
   Pluto centre whose orbit orientation remains unchanged requires a more
   specific transform operation.

## Current architecture

The current architecture is:

```text
celestial-model.json
├─ bodies and owned motion components
├─ stable IDs
├─ editor groups
└─ renderTree
   │
   └─ DeclarativeCelestialModel.jsx
      ├─ live mode -> Cobj + special geometry components
      └─ plot mode -> Pobj + the same special geometry components
                         │
                         ├─ EphController
                         ├─ PlotController
                         ├─ Trace
                         ├─ EphemerisChecker
                         └─ star/reference consumers
```

`SolarSystem.jsx` and `PlotSolarSystem.jsx` are now only two small entry points:

```jsx
<DeclarativeCelestialModel ObjectComponent={Cobj} mode="live" />
<DeclarativeCelestialModel ObjectComponent={Pobj} mode="plot" />
```

This does not make JSON execute astronomy. The JSON selects an ordered transform
tree and supplies parameters. The corresponding JavaScript components still
perform the transforms.

### Current Mercury/Venus implementation

Mercury and Venus no longer require custom Sun-relative React components. The
former `MercurySunRelativeOrbit.jsx` and `VenusSunRelativeOrbit.jsx` files and
their special node kinds were removed. Both bodies are now built entirely from
ordinary declarative motion stages:

```text
Sun
├─ Venus deferent -> Venus Plane -> Venus
└─ Mercury deferent -> Mercury Plane -> Mercury
```

Normal tree inheritance supplies the Sun's world position. The local deferent in
each branch applies the required annual counterrotation and retains that body's
own centre/radius/tilt. This is a real reduction in special code, not merely a
display-name change.

## How a time sample is evaluated now

### Visible model

The visible tree is created with `Cobj`. Normal circular stages continue using
the original `Cobj` rotation behaviour. Special components use `useFrame` to
update their matrices from the current `posRef`.

### Hidden plot and ephemeris model

The hidden tree is created with `Pobj`. Each normal `Pobj` registers its orbit
reference, speed and starting phase in `usePlotStore`, as before.

Special components register an `updateAfterMotion` callback in the same store.
`movePlotModel` then performs a sample in this order:

```text
1. Apply every registered orbital rotation.
   - ordinary Pobj stages
   - the lunar nodal/plane rotations
   - the ordinary Mercury and Venus deferent/plane/orbit stages
2. Apply negative-priority special geometry.
   - currently the lunar equant
3. Apply the remaining special transforms.
   - lunar solar-coupled centre
   - Pluto eccentric centre
   - remaining specialized Sun-relative body frames for Mars and Eros
4. Read final Three.js world positions.
```

The equant runs first because the solar-coupled Moon calculation needs the
Moon's direction for the same instant after the equant angle has been applied.

The important principle is that each special component owns one `update`
function. The same function is called by the live renderer and by the hidden
model. The implementation is not two independently fitted formula sets.

## File-by-file explanation

### `src/settings/celestial-model.json`

This is the unified astronomical document. It replaced the flat
`celestial-settings.json` and also declares the render and editor hierarchy.

It contains:

- real bodies and their parent IDs;
- motion components owned by those bodies;
- numerical parameters;
- stable component IDs;
- edit-menu grouping; and
- the render tree used for live and plot modes.

The hierarchy and the values were combined so a saved settings file could be a
complete, reusable model rather than a detached flat list whose structural
meaning lived elsewhere in JSX.

This decision is optional from a software-design perspective. A future version
could split it into `model-structure.json` and `model-parameters.json` without
changing the geometry, provided both are versioned and validated together.

### `src/components/DeclarativeCelestialModel.jsx`

This file replaces the two hard-coded trees, not `Cobj` or `Pobj` themselves.

It:

- validates model IDs, node kinds and setting references;
- walks `renderTree` recursively;
- emits the supplied generic object component for ordinary stages; and
- dispatches special node kinds to their corresponding transform components.

This is why adding a body or moving a parent no longer requires editing both
`SolarSystem.jsx` and `PlotSolarSystem.jsx`.

### `src/components/Cobj.jsx` and `Pobj.jsx`

These remain recognizably the original components.

Their meaningful changes are small:

- they can locate settings by stable `settingId`, not only display name;
- Moon scaling uses stable IDs;
- `Cobj` can suppress an inappropriate ordinary orbit line for a special frame;
  and
- `Pobj` participates in the same declared hierarchy as `Cobj`.

They were not replaced by a separate orbital engine.

### `src/components/MoonOrbitalPlane.jsx`

The original generic object could tilt an orbit, but the accepted lunar plane
requires a regressing line of nodes without rotating the entire descendant
orientation in the wrong way.

This component builds:

```text
outer nodal rotation
└─ inclined lunar plane
   └─ inverse nodal rotation
      └─ remaining lunar geometry
```

It also handles the existing Tychosium distinction between the enlarged display
Moon and the hidden physical-coordinate Moon. The same nodal and plane settings
drive both.

### Historical `src/components/MoonApsidalEquant.jsx` (removed from current branch)

This component implements a classical geometrical equant. A uniformly rotating
ray is viewed from an offset equant point and intersected with the circular lunar
orbit. The result is an angular correction to the ordinary circular phase.

The base Moon speed remains constant. The equant changes where the Moon lies on
the circle at a given mean phase; it is not an RA/declination correction.

The pure function `apsidalEquantCorrection(...)` is exported and tested. It
could be moved into a renderer-independent model-math module without changing
behaviour.

### `src/components/MoonSolarCoupledEccentric.jsx`

This is the most complex special component.

For the requested instant it:

1. temporarily removes its own centre offset to avoid feeding the result back
   into its input geometry;
2. reads Earth, Sun and Moon world positions;
3. derives lunar elongation `D` and anomalistic phase `M`;
4. derives the `2D-M` and `2D` orientations;
5. constructs the two centre-vector contributions;
6. applies the tested radial reflection; and
7. converts the fixed-ecliptic vector into the local coordinates of its moving
   parent.

Both contributions are translations of one lunar centre. There is no code that
adds a fitted value to the final RA, declination or longitude.

Its pure helpers are exported and tested, but the scene sampling and coordinate
conversion remain inside the React component. That is a reasonable target for
future extraction.

### `src/components/PlutoEccentricFrame.jsx`

This moves Pluto's orbital centre around the Sun while leaving the orientation
of Pluto's local orbit unchanged. It is the collapsed form of an earlier
rotation/translation/counterrotation hierarchy.

The component is short because the combined geometry is simply a time-dependent
translation. Its pure `plutoEccentricOffset(...)` helper is tested separately.

### `src/utils/nativeRelativeCarrier.js`

Mars, Mercury, Venus and Eros were formerly represented by Earth-level chains
that included parent-sized motion. After moving them beneath the Sun, those
absolute carriers could not simply remain active or the Sun's motion would be
counted twice. The utility was originally used for all four bodies; in the
current implementation it remains active only for Mars and Eros.

This utility evaluates the parent-relative carrier data:

- direct local centre;
- local orientation basis.

Mars has no annual remainder. Eros formerly used a six-coefficient annual vector
remainder, but the active model replaces it with the separate declared
`Eros Annual Centre Oscillation` stage in `ErosSunRelativeOrbit.jsx`. That stage
uses an amplitude, phase, annual speed and normalized axis to translate the
centre without rotating the local Eros orbit. Mercury and Venus no longer pass
through this evaluator.

### `*SunRelativeOrbit.jsx`

The two active adapters are:

- `SunMarsRelativeOrbit.jsx`; and
- `ErosSunRelativeOrbit.jsx`.

They place those local branches at the Sun and reconstruct their retained stages
in the correct matrix order. Mars uses an annual binary frame followed by its
long-period deferent; Eros uses its annual frame, declared annual centre
oscillation and local deferent. Phobos and Deimos then inherit the final Mars
frame naturally. Mercury and Venus now use ordinary declared `motion-stage`
nodes.

These files are not conventional perturbation models. They are coordinate
adapters required because the hierarchy was changed from independent Earth-level
chains to Sun-hosted branches while preserving the accepted local mathematics.

The two remaining adapters still share some scaffolding, but their sequences are
less alike than the former set of four. Any consolidation should therefore be
judged against readability rather than pursued only to reduce file count.

### `src/utils/celestialSettingsSchema.js`

The single-file model required an explicit schema layer. This utility:

- flattens body-owned motion components for the existing Zustand/UI code;
- resolves settings by stable ID or accepted legacy name;
- validates complete and partial imports;
- rejects obsolete absolute carriers that would be unsafe under the new parent
  hierarchy;
- reconstructs a complete schema-v3 model when saving; and
- provides the editor's declared body/frame groups.

This file changes data ownership and persistence, not orbital coordinates.

### `src/store.js`

The settings store now initializes from the normalized unified model rather than
the former flat file. Updates prefer stable IDs so display-name changes do not
break the runtime model. Load and reset operations also use the schema layer.

Two mutable Sun-Mars diagnostic references were added during binary-system
research. They do not modify transforms and are not required for normal
ephemerides.

### `src/components/Menus/EditSettings.jsx`

The settings editor now follows the declared astronomical body/frame groups
instead of inferring ownership from strings such as `" deferent"`.

Other changes repair or extend the research workflow:

- updates are immutable and ID-based;
- Save reads the current store at click time;
- Load accepts the unified document and selected older formats;
- new model parameters are exposed;
- visibility toggles are limited to actual visible objects; and
- zero-valued parameters are hidden by default but can be revealed with
  `Show zero values`.

Hidden zero fields remain in the store and in saved documents. This menu does
not alter ephemeris mathematics.

### `src/utils/saveAndLoadSettings.js`

The original save function exported a selected flat property list from a value
passed by the menu. The current code reads the store at click time and writes a
complete schema-v3 model. Loading is applied atomically through the schema
merger.

This was necessary after an observed bug in which the downloaded file could
contain the menu's initial value instead of the latest edit.

### `src/utils/plotModelFunctions.js`

The original `movePlotModel` rotated every registered `Pobj`. It still does
that. It now also calls registered special-transform callbacks after the normal
rotations.

This is the bridge that lets `EphController`, Plot, Trace and Checker all see the
same new geometry without each feature acquiring its own Moon or Pluto formula.

The Sun-Mars state functions in this file are diagnostics. Their return values
do not drive the bodies.

### `src/components/Ephemerides/EphController.jsx`

The ordinary ephemeris path is fundamentally unchanged. The controller still:

- creates the requested time samples;
- calls `movePlotModel`;
- reads body world positions; and
- converts them to RA, declination, distance and elongation.

The current diff in this file mostly adds an optional Sun-Mars diagnostic CSV.
It does not contain the new Moon, Pluto or Sun-relative orbital calculations.

If the diagnostic export is not wanted in a release branch, it can be removed
without changing ordinary ephemerides.

### Sun-Mars diagnostic files

These files were created to prove structural equivalence and inspect candidate
binary centres:

- `SunMarsBinaryTracker.jsx`;
- `sunMarsBinaryState.js`;
- `sunMarsBinaryCsv.js`; and
- the binary-output portions of the ephemeris UI/store/result components.

They read existing world positions. They do not reposition the Sun or Mars.

They are research instrumentation and can be isolated behind a development
flag, moved to a research package or removed from a publication branch after
their evidence has been archived.

### Small unrelated UI changes

- `Trace/traceStore.js` now enables dotted traces by default at the author's
  request.
- `StarSearch.jsx` reads the normalized unified model instead of the removed
  flat settings file.
- `misc-settings.json` uses the current lunar component name.

These changes do not alter celestial coordinates.

### Test files

Many of the newly added files are tests rather than runtime architecture. They
check:

- model-tree validity;
- save/load round trips;
- editor synchronization;
- exact relative-carrier reconstruction;
- special geometric helper functions;
- Sun-relative transforms;
- diagnostic formatting; and
- equivalence-sensitive matrix behaviour.

The number of changed files therefore overstates the amount of production logic
added to the simulator.

After the Mercury/Venus reduction, the full source gate passes `72` tests across
`14` suites. The production build also passes; its remaining warnings are the
pre-existing third-party MediaPipe source-map warnings.

## What actually changes coordinates

| Area | Can change body positions? | Purpose |
|---|---|---|
| Numerical values in `celestial-model.json` | Yes | Astronomical parameters |
| Parent/order changes in `renderTree` | Yes | Transform inheritance |
| Moon nodal/plane component | Yes | Lunar plane orientation |
| Lunar equant | Yes | Geometrical angular progression |
| Solar-coupled lunar centre | Yes | `2D-M` and `2D` centre geometry |
| Pluto eccentric frame | Yes | Moving Pluto orbital centre |
| Sun-relative adapters | Yes | Remaining Mars/Eros parent-relative branch reconstruction |
| Mercury/Venus ordinary stages | Yes | Sun inheritance plus local counterrotation, plane and orbit |
| Schema, Save/Load and Edit Settings | No | Data integrity and UI |
| Sun-Mars trackers/CSV | No | Read-only diagnostics |
| Dotted trace default | No | Presentation only |
| Tests | No | Regression protection |

## What was deliberately not done

The runtime does not:

- read JPL data;
- use the research residual CSV files;
- add corrections to final RA or declination;
- apply a date-indexed lookup table;
- run an FFT during simulation;
- replace exported coordinates after the model is evaluated; or
- hide a second conventional ephemeris solver inside `EphController`.

The research tools use JPL to measure outcomes, but the simulator receives only
geometric settings and its own internally generated body directions.

## Honest architectural concerns

The following concerns are valid and deserve review.

### 1. Model mathematics still lives partly in JSX

Pure helpers exist, but several special components combine mathematical
evaluation with React refs, scene lookup and lifecycle registration. This makes
the code harder to understand than a pure model evaluator.

Recommended direction: move pure geometry into modules such as:

```text
src/model/evaluateMoon.js
src/model/evaluatePluto.js
src/model/evaluateParentRelativeBody.js
```

The JSX components would then only apply returned matrices/vectors.

### 2. Two specialized Sun-relative components remain

The Mercury and Venus special adapters were eliminated. Mars and Eros still use
different parent-relative sequences with some shared React plumbing. A common
component remains possible, but the benefit is now smaller and should be weighed
against making two distinct geometries harder to read.

### 3. Update ordering is implicit infrastructure

`updatePriority` currently guarantees that the equant settles before the
solar-coupled Moon samples its direction. This works and is tested, but an
explicit dependency graph or a single ordered model evaluator would be clearer.

### 4. World-object lookup uses names

Stable setting IDs protect configuration lookup, but some scene operations still
find `Earth`, `Sun`, `Moon` or `Actual Moon` by object name. Stable runtime IDs or
direct references would be safer.

### 5. The enlarged and physical Moon branches add complexity

This distinction existed because a visually enlarged Moon must not be used for
physical coordinates. The declarative tree makes both branches explicit, but a
future renderer-independent evaluator could remove the need for a second hidden
live Moon branch.

### 6. Some compatibility-era components are currently unused

At the time of this audit:

- `SunPrimaryFrameAdapter.jsx`; and
- `SunMarsBinarySystem.jsx`

are not reachable from the application's active production render path. They
remain from intermediate migration phases and have tests. They are candidates
for removal after confirming that no external extension imports them.

### 7. Binary diagnostics are broader than the final product requires

The live tracker, state objects and CSV export were useful during research but
are not needed to display the model or export ordinary ephemerides. The original
developer may reasonably prefer to move them out of the release code.

## Three reasonable paths forward

### Option A: conservative cleanup of the current branch

Keep the current geometry and declarative tree, but:

1. remove confirmed unused components;
2. move optional binary diagnostics into development tooling;
3. review whether the two remaining Sun-relative adapters benefit from a shared
   evaluator;
4. extract Moon and Pluto pure mathematics from JSX; and
5. retain the existing equivalence and ephemeris tests.

This has the lowest risk because it does not change accepted coordinates.

### Option B: preserve the original explicit JSX style

The developer could rewrite `SolarSystem.jsx` and `PlotSolarSystem.jsx` as
explicit trees again, inserting the accepted special geometry in both.

This is possible, but the two trees must remain synchronized. The special
mathematics should still be shared in pure functions; it should not be copied
independently into both trees.

### Option C: build a renderer-independent evaluator

The cleanest long-term architecture would be something like:

```js
const state = evaluateCelestialModel(model, settings, time);
const moonWorld = state.get("moon").worldPosition;
```

The evaluator would return matrices or vectors for every stage/body. Then:

- the live renderer would display those matrices;
- traces and plots would sample them;
- `EphController` would read them directly; and
- tests would validate the evaluator without mounting React or Three.js scenes.

This would answer the original developer's underlying concern most completely:
astronomical mathematics would belong to the model layer, not the UI layer.

It is also the largest refactor. It should only be done behind the preserved raw
ephemeris and distance baselines so that architectural simplification cannot
silently change the astronomy.

## Recommended review order

The original developer can review the branch efficiently in this order:

1. Compare `main` and the experimental branch's `SolarSystem.jsx` and
   `PlotSolarSystem.jsx`.
2. Read `DeclarativeCelestialModel.jsx` and the `renderTree` section of
   `celestial-model.json`.
3. Confirm that ordinary `Cobj`/`Pobj` behaviour remains familiar.
4. Review the three lunar components and `PlutoEccentricFrame.jsx` as isolated
   special transformations.
5. Review the Mars and Eros Sun-relative adapters and confirm that Mercury and
   Venus now follow only ordinary declarative stages.
6. Inspect `movePlotModel` to verify how live and plot updates correspond.
7. Inspect `EphController` last; it remains a scheduler/reader rather than the
   owner of orbital geometry.
8. Decide whether diagnostics and compatibility files belong in the release.
9. Run the full source tests and production build.
10. Re-export the preserved validation interval before accepting any refactor.

## Acceptance rule for any rewrite

The implementation is replaceable; the verified behaviour is the asset.

A cleaner rewrite should be preferred if it can demonstrate all of the
following:

- the live view, hidden plot model and ephemeris export use one mathematical
  definition;
- the settings editor still changes the values actually used by the model;
- saved settings reload without loss;
- no JPL-derived correction enters runtime coordinates;
- the current raw ephemeris baselines remain equal within defined numerical
  tolerance; and
- the special Moon/Pluto geometry remains inspectable rather than being hidden
  as an output patch.

## Final assessment

The extra files were not added because `EphController` was incapable of
producing another number. They were added because the research objective became
larger: the displayed Tychosium, its declared hierarchy, its editable settings,
its traces and its exported ephemerides were all expected to describe the same
geometrical model.

That goal is sound. The current implementation achieves it and has extensive
regression evidence. At the same time, the original developer is correct to ask
whether the final code can be made smaller and whether astronomical evaluation
should be more independent of React components.

The best conclusion is therefore not that either approach was wrong:

- updating only `EphController` would have been smaller but would have created a
  private export-only model;
- the current implementation preserved cross-feature consistency but accumulated
  specialized infrastructure during research; and
- a reviewed pure evaluator could retain the new geometry while recovering the
  compactness and clarity the original developer values.

The original developer should feel free to refactor or reject any of this
software structure. The archived baselines, tests and documented geometry exist
precisely so the code can be improved without losing the astronomical work.
