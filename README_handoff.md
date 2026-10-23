# Developer / AI handoff

> Latest branch: `paired-radial-3d`. The lunar equant and blend control are absent; paired radial vectors are constructed in the moving lunar plane in `MoonSolarCoupledEccentric.jsx`, together with the solar-coupled geometry. See `moon_model.md` for results. Older lunar descriptions and distance figures below are historical, not validation of the present version.

Mercury transit-focused candidate: plane `orbitCenterb = 0.6` instead of 4, with no new hierarchy element. Four transit-date samples improve relative to the preceding compact baseline and show smaller centre separations than `mercury-test`; the global RMS worsens. Three-hour sampling cannot validate contact times or complete paths. Preserve `00-mercury-test`, `00-paired-radial-3d` and the latest `00-mercury-iteration` for comparison.

Shared-motion hypotheses are exploratory: similar FFT peaks are not evidence of a shared physical force. Compare matched epochs and frames, phase and direction, and held-out intervals before adding geometry. A common translation of observer and target cancels from their relative vector.

This handoff describes the experimental **`full-send-binary-tychos`** branch. See
[README.md](README.md) for analysis commands and [binary_tychos.md](binary_tychos.md)
for the design rationale.

## Current state

The exact-equivalence predecessor reports and raw exports are preserved under
`00-backup/full-binary-baseline`.

This branch completes the parent-relative settings migration without deliberately
changing any accepted orbit:

- Earth supplies the PVP motion.
- The Sun inherits Earth and supplies the solar-system position.
- Mars, Mercury, Venus and Eros inherit the Sun's world position.
- Mars and Eros retain the direct parent-relative carrier mechanism established
  during the equivalence migration.
- Mercury and Venus no longer use special parent-relative A carriers or separate
  B/secondary records. Each now has one local deferent, one plane and its orbit.
- Jupiter, Saturn, Uranus, Neptune, Pluto and Halley were already Sun-hosted.
- The Moon remains Earth-hosted; Phobos and Deimos remain Mars-hosted.

After equivalence was proven, the common annual cosine/sine residual of Mars,
Mercury and Venus was intentionally set to zero. Schema v3 now removes those
parameters entirely rather than storing eight inactive zero fields.
The exact equivalence version and reports remain in
`00-backup/full-binary-baseline`, and its original residual values are preserved
in [binary_tychos.md](binary_tychos.md).

```text
SystemCenter
└─ Earth
   ├─ Moon Node / Plane -> Moon
   └─ Sun-Mars Binary Frame
      └─ Sun Primary -> Sun
         ├─ Mars Junior Companion -> Phobos / Deimos
         ├─ Venus Senior Solar Moon
         ├─ Mercury Junior Solar Moon
         ├─ Jupiter / Saturn / Uranus / Neptune / Pluto
         ├─ Halley
         └─ Eros
```

`SystemCenter` is the fixed geometric reference of Earth's PVP path, not a body or
barycentre. The model remains Tychonic: Earth follows the PVP path, the Sun is
positioned relative to Earth, and the solar subsystem is organized beneath the
Sun.

### Current Mercury/Venus simplification

The accepted active branches are now:

```text
Sun Primary
├─ Venus deferent
│  └─ Venus Plane
│     └─ Venus
└─ Mercury deferent
   └─ Mercury Plane
      └─ Mercury
```

The single deferent in each branch counterrotates the annual orientation inherited
from the Sun while retaining necessary local geometry. It is not a duplicated Sun
orbit. Venus retains a small local radius and tilt; Mercury retains a non-zero
centre and tilt. Consequently these stages cannot be deleted merely because both
bodies are children of the Sun.

The former Venus A-carrier centre was algebraically transformed into the Venus
plane centre. Mercury's former A vertical offset was moved into the Mercury plane.
These translations were derived from the prior geometry, not fitted to JPL. Old
Mercury/Venus A/B component IDs are now treated as retired import data so an old
settings file cannot silently reconstruct the removed hierarchy.

The latest source verification passes `72` tests across `14` suites, and the
production build passes with only the pre-existing third-party MediaPipe
source-map warnings.

## What is genuinely different

The complete astronomical source of truth is now the schema-v3
`src/settings/celestial-model.json`. It contains the reference frame, one record
per real body, parent relationships, every numerical motion component, editor
groups and the internal render tree. The separate `celestial-settings.json` has
been removed.

Node, plane and deferent terms remain available for geometric adjustment inside
their owning body's `motion` object, but they are no longer declared as celestial
bodies. Stable component IDs are retained for runtime and legacy import
compatibility.

The first full-binary migration evaluated each affected body from its old absolute
chain and expressed the result relative to the Sun. Mars and Eros still use the
resulting parent-relative carrier quantities:

```text
body world position
  = inherited Sun world position
  + direct relative centre
  + declared local geometric stages
  + body orbit
```

The active parent-relative carrier IDs are:

- `mars-deferent-e`
- `eros-deferent-a`

Both have `orbitRadius: 0`. Mars has no active annual residual. Eros's former
six-coefficient annual residual was replaced by the declared
`eros-annual-centre-oscillation` stage: a single annual centre displacement
with an explicit amplitude, axis and phase. Mercury and Venus now use ordinary
declarative `motion-stage` nodes and no longer pass through
`nativeRelativeCarrier.js` or body-specific Sun-relative JSX adapters.

Old absolute-carrier files are rejected for Mars and Eros rather than being
silently mixed with the new model. Retired Mercury/Venus A/B entries are ignored
safely. Other stable-ID and legacy-name imports remain supported.

## Original schema-v3 verification completed

The schema-v3 single-file migration was re-exported over the complete baseline
grid on 2026-10-06. It is numerically identical to the immediately preceding
zero-residual full-binary baseline; therefore reorganizing the data into body
records introduced no ephemeris change.

| Gate | Result |
|---|---|
| Dense direct-settings audit, -100 to +100 model years | PASS for all four carriers |
| Maximum centre reconstruction error | `2.3e-16` |
| Maximum annual reconstruction error | `2.9e-14` |
| Source tests | 67 passed across 12 suites |
| Production build | PASS; only third-party MediaPipe source-map warnings |
| Complete ten-body TYCHOS export | PASS; 759,756 non-metadata lines identical |
| Direct Eros export | PASS; 75,969 displayed rows identical |
| Sun–Mars binary CSV | PASS; all recorded numeric deltas exactly zero |
| Ten-body apparent true-of-date summaries | PASS; zero numerical delta |
| Residual, annual and FFT artifacts | PASS; 30 of 30 byte-identical |

Run the software gates with:

```powershell
npm test -- --watchAll=false --runInBand
npm run build
```

The phase-specific derivation scripts used during this migration have been
retired from the active script directory. Their results remain preserved in this
document, `binary_tychos.md`, the archived baselines and Git history.

## End-to-end result

The fresh exports use the baseline bodies, interval, cadence and native frame.
The archived exact-equivalence run confirms the parent-relative derivation against
`00-backup/full-binary-baseline`. The later common-residual removal is an
intentional scientific change and should not pass that particular raw-output gate.

The combined files differ only in their `Generated on` timestamp. Eros is
identical in RA, declination, distance and elongation. The high-precision binary
CSV differs only around `1e-14`, plus `acos` endpoint sensitivity below
`1.21e-6°`; both are numerical roundoff.

Both saved and candidate report sets now use JPL apparent true-of-date, so the
scientific comparison is valid. Keep this reference product identical in future
before/after comparisons; do not compare these values directly with an ICRF
report set. Use `compare_summary_metrics.py` for current report baselines.

The structural migration is complete. The later Mercury/Venus simplification is
also a scientific improvement on the matched long comparison:

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

These results cover `1800-06-21` through `2026-06-21`, one-day cadence,
`82,546` matched samples, using JPL apparent true-of-date. Mercury's signed mean
declination bias increased from `+0.188732°` to `+0.347652°`, although its
declination RMS improved slightly. This tradeoff must remain visible in future
evaluation.

## Retained Pluto, Jupiter, Saturn and Mars refinements

These are empirical adjustments of existing TYCHOS parameters. They do not alter
the hierarchy, restore an absolute carrier, introduce a fitted correction term or
change the Sun. All quoted comparisons use JPL apparent true-of-date coordinates.

### Retained parameters

| Body / component | Parameter | Previous | Retained |
|---|---|---:|---:|
| Pluto orbit | `startPos` | `200` | `204` |
| Pluto orbit | `orbitCentera` | `877` | `1387.5` |
| Pluto orbit | `orbitCenterb` | `667` | `1110` |
| Pluto orbit | `orbitCenterc` | `-333` | `-525.5` |
| Pluto deferent | `orbitTilta` | `0` | `-1.5` |
| Pluto deferent | `orbitTiltb` | `0` | `1.2` |
| Jupiter orbit | `startPos` | `-34` | `-34.09` |
| Jupiter orbit | `speed` | `0.52994136` | `0.52989` |
| Jupiter orbit | `orbitCentera` | `-49` | `-49.95` |
| Jupiter orbit | `orbitCenterc` | `-1` | `1.1` |
| Jupiter orbit | `orbitTiltb` | `-1.2` | `-1.24` |
| Saturn orbit | `startPos` | `-123.8` | `-123.7` |
| Saturn orbit | `speed` | `0.21351984` | `0.21357` |
| Saturn deferent | `orbitRadius` | `89` | `98` |
| Saturn deferent | `orbitCenterc` | `0` | `1.6` |
| Saturn orbit | `orbitCenterb` | `40` | `35.87` |
| Mars orbit | `startPos` | `119.2` | `119.358` |
| Mars deferent E | `orbitCentera` | `7` | `7.62` |
| Mars deferent E | `orbitCenterc` | `0` | `0.232` |
| Mars orbit | `orbitTiltb` | `-2.16` | `-2.109` |

The active Pluto configuration follows the author's preferred revision. The
research-optimized alternative remains documented for later comparison:
`startPos = 204.5`, with deferent `orbitTilta = 0` and `orbitTiltb = 0`; its
centres were the same active `1387.5 / 1110 / -525.5`. The author-selected
Pluto values are being retained despite the long-baseline JPL comparison
favouring that alternative. Jupiter's other geometry was retained. The active
Saturn phase, speed and deferent C value are the later author refinement shown
above. Mars's speeds, secondary deferent and

Pluto speed was updated from ​​0.0253303 to --> 0.02545039

`Mars deferent E orbitCenterb = -20` were retained. Fractional adjustment of
that `orbitCenterb` was deliberately rejected in favour of the directly measured
and conceptually established value.

### Long-baseline results

The Pluto, Jupiter, Saturn and Mars long comparisons cover `1800-06-21` through
`2026-06-21` at one-day cadence.

| Body | Metric | Previous | Retained | Improvement |
|---|---|---:|---:|---:|
| Pluto | RA RMS | `10.051°` | `1.977°` | `80.3%` |
| Pluto | Dec RMS | `1.791°` | `1.324°` | `26.1%` |
| Pluto | Angular mean | `8.246°` | `2.188°` | `73.5%` |
| Pluto | Angular RMS | `9.687°` | `2.321°` | `76.0%` |
| Jupiter | RA RMS | `0.5380°` | `0.3893°` | `27.6%` |
| Jupiter | Dec RMS | `0.3234°` | `0.1575°` | `51.3%` |
| Jupiter | Angular mean | `0.5270°` | `0.3370°` | `36.0%` |
| Jupiter | Angular RMS | `0.6120°` | `0.4107°` | `32.9%` |
| Saturn | RA RMS | `0.9225°` | `0.6053°` | `34.4%` |
| Saturn | Dec RMS | `0.2277°` | `0.1763°` | `22.6%` |
| Saturn | Angular mean | `0.7209°` | `0.4997°` | `30.7%` |
| Saturn | Angular RMS | `0.9150°` | `0.6066°` | `33.7%` |
| Mars | RA RMS | `0.6287°` | `0.5708°` | `9.2%` |
| Mars | Dec RMS | `0.3614°` | `0.3041°` | `15.8%` |
| Mars | Angular mean | `0.5820°` | `0.5166°` | `11.2%` |
| Mars | Angular RMS | `0.6950°` | `0.6202°` | `10.8%` |

The fitted Jupiter and Saturn center values were confirmed by fresh exports:
Jupiter's predicted angular RMS was `0.41068°` and the measured value was
`0.41065°`; Saturn's predicted value was `0.60660°` and the measured value was
`0.60661°`. Mars's fitted phase, vertical center, plane tilt and `orbitCentera`
were also confirmed by fresh exports; the retained combined result is the
directly measured `0.62019°` angular RMS with `orbitCenterb = -20`.

### Independent validation status

Pluto was also tested over `2000-06-21` through `2026-06-21` at three-hour
cadence. Its angular mean improved from `5.509°` to `2.649°`, angular RMS from
`6.049°` to `2.690°`, RA RMS from `5.876°` to `1.862°`, and Dec RMS from
`2.554°` to `2.007°`. The modern Dec mean became worse, so the retained Pluto
setting is a global-fit choice rather than a claim that every metric improved.

Jupiter, Saturn and Mars still require the equivalent dense `2000-2026`,
three-hour validation before their refinements should be considered final. Their
remaining largest RA residuals are near `365.25` and `439.07` days for Jupiter,
`378.65` days for Saturn, and `365.25` and `248.63` days for Mars. Those peaks
are diagnostic fingerprints, not evidence that another arbitrary parameter
should be added.

## Moon refinement research

The accepted experimental Moon now uses explicit node/plane geometry, a
solar-coupled `2D-M` stage, solar variation, an anomalistic tangential stage and
a reflected radial `2D-M` action. See [moon_model.md](moon_model.md) for the full
derivation, rejected experiments and validation record.

The earlier author-selected configuration below is retained only as historical
research context. It was superseded by the solar-coupled solution:

| Component / parameter | Previous baseline | Author-selected |
|---|---:|---:|
| Moon Plane `orbitCentera` | `0` | `0.001` |
| Moon Plane `orbitCenterb` | `0` | `0.01` |
| Moon Deferent A `startPos` | `167.51°` | `157.3°` |
| Moon Deferent A `orbitRadius` | `0.02786` | `0.0215` |
| Moon orbit `startPos` | `318°` | `328°` |

A direct validation covering `2000-06-21` through `2026-06-21` at three-hour
cadence, compared with the same JPL apparent true-of-date product, found:

| Metric | Previous baseline | Author-selected | Result |
|---|---:|---:|---:|
| RA mean | `-0.240912°` | `-0.030819°` | smaller bias |
| RA RMS | `1.061210°` | `2.220218°` | `109.2%` worse |
| Declination mean | `-0.000858°` | `-0.071639°` | larger bias |
| Declination RMS | `0.364896°` | `0.712547°` | `95.3%` worse |
| Angular mean | `0.921211°` | `1.831483°` | `98.8%` worse |
| Angular RMS | `1.073484°` | `2.229533°` | `107.7%` worse |

Those values were an explicit author-directed model choice, not a JPL-error
optimization. Their reports remain useful historical evidence but they are no
longer the active Moon baseline.

The dominant RA residual periods were approximately `31.760 d` (`1.0900°`),
`14.769 d` (`0.6563°`), one year (`0.1846°`) and `13.783 d` (`0.1219°`). These
are diagnostic periods only; they must not be implemented as fitted corrections.

Two geometric investigations were rejected:

- Static centre offsets on the Moon orbit and Moon Deferent A, tested separately
  along their available axes, consistently worsened the global metrics. Further
  centre-offset iteration is therefore not recommended.
- An explicit Moon-only lunar eccentric stage was tested between Moon Deferent A
  and the Moon orbit. It used a conjugated rotating displacement driven at twice
  the Moon phase. A first `0.0005`-radius trial worsened all RMS metrics by about
  `0.3–0.4%` and reintroduced a strong `27.53 d` residual. Optimizing its sign,
  phase and radius (`startPos = 180°`, `phaseMultiplier = 2`, radius `0.00015`)
  produced only negligible improvements: RA RMS `0.026%`, declination RMS
  `0.016%` and angular RMS `0.025%`. The extra hierarchy and parameters were not
  justified, so the component was abandoned and is not present on this branch.

The eccentric-stage negative result indicates that the remaining Moon error in
the previous baseline is not well described by another Moon-only static
eccentricity. Any future experiment should begin from
a clear geometric hypothesis, most plausibly one involving the relative
Sun–Earth–Moon configuration, and must remain a visible declarative motion rather
than an empirical perturbation or output correction.

### Predecessor solar-coupled and radial-neutral solution

Subsequent research established a substantially better explicit geometry. No
periodic correction, Fourier term or ephemeris-output adjustment was introduced.
Every added motion is evaluated inside the Moon hierarchy from directions already
generated by the astronomical model:

```text
Earth
└─ Moon Node
   └─ Moon Plane
      └─ Moon Deferent A
         └─ Solar-Coupled / Variation / Anomalistic Tangential Frame
            └─ Moon Orbit
```

The retained experimental parameters are:

| Component | Parameter | Value |
|---|---|---:|
| Moon Deferent A | `startPos` | `167.51°` |
| Moon Deferent A | `speed` | `0.71015440177343` |
| Moon Deferent A | `orbitRadius` | `0.01131` |
| Moon orbit | `startPos` | `318°` |
| Moon Solar-Coupled Eccentric | `orbitRadius` | `-0.0055` |
| Moon Solar Variation | `orbitRadius` | `0.002` |
| Moon Anomalistic Tangential Frame | `orbitRadius` | `0.01655` |

The solar-coupled eccentric direction is constructed from the actual lunar
elongation and anomalistic phase. The solar-variation vector is constructed from
twice the actual elongation. Neither component stores a fitted period: their
cycles emerge from the changing Earth–Sun–Moon geometry.

Reducing the physical Deferent-A radius corrected the previously exaggerated
perigee/apogee excursion but initially restored a large anomalistic angular
error. The anomalistic tangential frame recovers the missing angular action from
the existing apsidal direction while rejecting its component parallel to the
Earth–Moon radius. It is a radial-neutral geometric construction, equivalent to
paired rotating vectors, and is not a post-calculation correction.

The final dense comparison covers `2000-06-21` through `2026-06-21` at three-hour
cadence (`75,969` samples), against JPL apparent true-of-date coordinates:

| Metric | Mean | RMS |
|---|---:|---:|
| Right ascension | `-0.241481°` | `0.319696°` |
| Declination | `-0.001618°` | `0.208520°` |
| Angular separation | `0.335800°` | `0.370483°` |

The final TYCHOS distance range over the same export is
`356,268–406,554 km`, with midpoint `381,411 km`. NASA's broad reference range is
approximately `356,400–406,700 km`; the differences are only `132 km` at the
near end and `146 km` at the far end. The modeled span is `50,286 km`, versus
approximately `50,300 km` for the reference range.

The previously dominant `27.5 d`, `31.8 d` and `14.8 d` RA structures were
strongly suppressed by distinct geometric stages. The largest remaining modern
RA peak was annual, approximately `0.185°`, and the Sun remained unchanged.

That radial-neutral solution was the predecessor of the final retained geometry.

### Current reflected-radial Moon baseline

The author-requested Moon speed is now `83.28521004`. Point-by-point distance
analysis showed that the solar-coupled `2D-M` vector had beneficial tangential
action but incorrectly oriented radial action. The current implementation keeps
the tangential component and reflects only its projection along the instantaneous
Earth-Moon radius. This happens inside the Moon hierarchy before coordinates are
derived; it is not a distance or ephemeris correction.

Final independent validation used JPL apparent true-of-date over
`1800-06-21` through `2026-06-21`, one-day cadence (`82,546` samples):

| Metric | Mean | RMS |
|---|---:|---:|
| Right ascension | `-0.208457°` | `0.290102°` |
| Declination | `-0.001203°` | `0.203615°` |
| Angular separation | `0.309363°` | `0.345048°` |

Distance results over the same interval were mean bias `+37.3 km`, RMS
`5,711.1 km`, mean absolute error `4,787.6 km` and maximum absolute error
`14,276.3 km`. TYCHOS extrema were `362,246-412,537 km`, versus JPL interval
extrema near `356,396-406,708 km`.

At the 2015-03-20 eclipse, the dense three-hour run gave `363,275 km` for
TYCHOS and `357,886 km` for JPL: a `+5,389 km` difference, reduced from roughly
`+21,094 km` before radial reflection. Relative to the saved `00-coupled`
baseline, angular RMS improved by about `2.1%` and distance RMS by about `42%`.

The distance RMS was `5,706.5 km` over dense `2000-2026` data and `5,711.1 km`
over the independent 226-year validation. Preserve the current settings and both
report sets as the accepted Moon research baseline.

## Key files

| File | Responsibility |
|---|---|
| `src/settings/celestial-model.json` | Single source: bodies, hierarchy, editor groups and all numerical motion parameters |
| `src/utils/nativeRelativeCarrier.js` | Direct centre/orientation evaluator for the remaining Mars/Eros carrier branches |
| `src/utils/celestialSettingsSchema.js` | Serialization and safe import rules |
| `src/components/SunMarsRelativeOrbit.jsx`, `ErosSunRelativeOrbit.jsx` | Remaining specialized parent-relative branches beneath the Sun |
| `scripts/` | Maintained ephemeris workflow; see its local `README.md` |
| `moon_model.md` | Complete Moon geometry, results and rejected experiments |

## Constraints

- TYCHOS ephemerides must be generated by the astronomical geometry declared in
  `src/settings/celestial-model.json`.
- Never add fitted perturbations or empirical corrections to model output.
- Do not add Fourier residual terms, lookup tables, splines, date-dependent
  offsets, body-specific output patches or post-export corrections merely to
  improve agreement with JPL.
- Residual, annual and FFT analyses are diagnostic tools only. They may identify
  the period or geometric layer worth investigating, but their fitted values must
  not be injected into the ephemeris output.
- Refine existing geometric quantities—phase, speed, radius, centre, tilt, plane,
  node or an already-declared motion stage—through `celestial-model.json`.
- A genuinely new motion component is acceptable only when it expresses an
  explicit TYCHOS geometric hypothesis, is visible in the declarative model and
  editor, and is validated as geometry. It must not be a hidden error-cancellation
  layer.
- The analysis and export code must remain observers of the astronomical core;
  they must not silently modify body coordinates to improve comparison metrics.
- Eros's annual centre oscillation is an explicit, visible geometric stage that
  compresses the former compatibility harmonic. It is not precedent for adding
  fitted harmonics or hidden output corrections to other bodies.
- Do not tune parameters until the fresh-export equivalence gate passes.
- Do not restore radius-100 carriers beneath the Sun.
- Do not restore the retired Mercury/Venus A/B hierarchy. Their accepted active
  form is `deferent -> plane -> orbit` beneath the Sun.
- Do not split Sun translation and orientation merely to hide all planetary
  deferents. Several deferents retain body-specific radius, centre or tilt; moving
  those values into a body record would rename the geometry rather than remove it.
- Do not treat a zero-radius stage as redundant if it retains centre/orientation.
- Keep reference-frame comparison separate from orbital tuning.
- Preserve the baseline settings, exports, configuration and reports together.
