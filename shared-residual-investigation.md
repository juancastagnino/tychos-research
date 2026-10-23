# Shared-body residual investigation

Exploratory analysis of `tychos-research/TSN/00-paired-radial-3d`, using all ten same-grid residual CSVs. All summary metadata declare 82,546 daily samples, 1800-06-21–2026-06-21, and the same TYCHOS and JPL input hashes. Model/export configuration is not embedded in the export; the label is user-declared. TYCHOS native coordinates are compared with JPL apparent true-of-date; these are not identical products.

`scripts/inspect_shared_residuals.py` fits a constant plus first and second annual harmonics to each signed RA or Dec residual. Coefficients are fitted on 1800–1912 and evaluated on 1913–2026 against the training-period mean. Held-out R² is 1 minus the squared error ratio to that fixed-mean control. Annual amplitudes and phases are also independently estimated in each half (phase convention cos(theta - phase), theta measured from 2000-01-01 with period 365.2425 d). Fits describe residuals; they are not proposed model corrections. Fits to Sun-relative phase use JPL equatorial RA difference, not actual ecliptic elongation; this is an exploratory reference-derived proxy and not an independent or predictive model input.

| RA residual | Annual amplitude first / second half | Annual phases first / second half | Held-out R² annual harmonics |
|---|---:|---:|---:|
| Moon | 0.1861° / 0.1858° | 90.6° / 92.2° | 0.331 |
| Mercury | 1.8358° / 1.8282° | 50.8° / 55.9° | 0.335 |
| Venus | 0.2239° / 0.2496° | -67.7° / -56.1° | 0.169 |
| Mars | 0.3938° / 0.2699° | -139.8° / -140.2° | 0.128 |
| Jupiter | 0.2568° / 0.2556° | -176.2° / -174.2° | 0.243 |
| Uranus | 0.0658° / 0.0713° | -16.9° / -17.4° | 0.095 |
| Sun | 0.0196° / 0.0490° | 162.9° / 13.6° | -0.349 |

These are different phases and amplitudes, not a single demonstrated common oscillation. A single annual fit transfers poorly for the Sun. Annual signatures are compatible with many explanations including coordinate/projection effects, geometric/apparent differences, annual model motion and sampling; no physical mechanism follows from these numbers.

Sun-relative RA-separation proxy harmonics transfer to the held-out half with R² 0.168 for Mars RA and 0.535 for Mars Dec; Saturn RA gives 0.637. Mercury and Venus RA scores are 0.023 and 0.007 respectively. These correlations can reflect body-specific orbital geometry, sky projection, sampling and other confounders; the intercept and training mean matter. Saturn's long cycle covers few independent orbital cycles, making a single split especially fragile. No cross-body phase-coherent vector or predictive relation is established. Scores use JPL directions as regressors, so they cannot validate TYCHOS as a self-contained model.

Practical next steps: compare frame-matched geometric ephemerides with identical corrections; use model-derived 3D relative angles and distances; analyze signed tangent-plane residual vectors, including phase and radial errors; separate annual and conjunction terms in joint regressions and perform blocked tests over multiple epochs. Check sampling and Moon 3-hour data before short-period conclusions. Test a constrained shared Earth-observer displacement, a shared Sun-host frame displacement and a Sun–Mars-relative mechanism separately; predict direction and distance scaling, evaluate all bodies and protect Sun/Moon performance. Common translation of all objects cancels. A whirlpool is a hypothesis only after specifying center, axis, velocity/displacement field, clocks and testable body-dependent predictions; this analysis does not establish one.
