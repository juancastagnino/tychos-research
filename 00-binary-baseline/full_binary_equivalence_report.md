# Phase export-equivalence comparison

Status: **PASS**  
Coordinate/numeric tolerance: `1.000e-09`  
Constructed midpoint endpoint-angle tolerance: `2.000e-06 deg`

## Scientific summary fields

Provenance fields are intentionally excluded.

| Body | Maximum numeric delta | Other differences |
|---|---:|---|
| jupiter_apparent_of_date | 0 | none |
| mars_apparent_of_date | 0 | none |
| mercury_apparent_of_date | 0 | none |
| moon_apparent_of_date | 0 | none |
| neptune_apparent_of_date | 0 | none |
| pluto_apparent_of_date | 0 | none |
| saturn_apparent_of_date | 0 | none |
| sun_apparent_of_date | 0 | none |
| uranus_apparent_of_date | 0 | none |
| venus_apparent_of_date | 0 | none |

## Per-sample and spectral artifacts

Byte-identical files: `30` of `30`.

Non-identical files: none

## Sun-Mars binary CSV

Rows: `9497`; timestamp mismatches: `0`.

| Field | Maximum absolute delta | RMS delta |
|---|---:|---:|
| sun_world_x | 0 | 0 |
| sun_world_y | 0 | 0 |
| sun_world_z | 0 | 0 |
| mars_world_x | 0 | 0 |
| mars_world_y | 0 | 0 |
| mars_world_z | 0 | 0 |
| sun_mars_separation | 0 | 0 |
| earth_center_x | 0 | 0 |
| earth_center_y | 0 | 0 |
| earth_center_z | 0 | 0 |
| earth_sun_dx | 0 | 0 |
| earth_sun_dy | 0 | 0 |
| earth_sun_dz | 0 | 0 |
| earth_mars_dx | 0 | 0 |
| earth_mars_dy | 0 | 0 |

## Interpretation

- This gate compares TYCHOS outputs before and after a structural refactor; it does not measure agreement with JPL.
- Different export hashes or decimal strings are acceptable only when timestamp-aligned numeric values remain within tolerance.
- The midpoint is defined from the two endpoints, so its opposition is exactly 180 degrees by construction. Its relaxed angle tolerance covers only floating-point sensitivity of `acos` at that endpoint; it does not relax any position field.
- A pass supports coordinate equivalence at the declared tolerance; it does not prove physical correctness.
