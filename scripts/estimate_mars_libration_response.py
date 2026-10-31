"""Estimate the linear response of Mars residuals to one libration test.

This is a diagnostic only.  It interpolates between a saved baseline and one
candidate run to estimate the sign/scale that would minimise tangent-plane RMS
within that *same* tested geometrical response.  It does not fit or export an
ephemeris correction.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def read(folder: Path):
    return np.genfromtxt(
        folder / "mars_apparent_of_date_residuals.csv",
        delimiter=",",
        names=True,
        dtype=None,
        encoding="utf-8",
    )


def rms(vectors: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.sum(vectors**2, axis=1))))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument(
        "--candidate-amplitude",
        type=float,
        required=True,
        help="Plane-libration amplitude used for candidate, in degrees.",
    )
    args = parser.parse_args()

    baseline, candidate = read(args.baseline), read(args.candidate)
    if not np.array_equal(baseline["date"], candidate["date"]):
        raise ValueError("Baseline and candidate timestamps do not match")

    # RA is scaled by cos(dec) so it shares the local tangent-plane units of
    # declination before estimating a single geometric response scale.
    cos_dec = np.cos(np.deg2rad(baseline["jpl_dec_deg"]))
    initial = np.column_stack(
        (baseline["dra_deg"] * cos_dec, baseline["ddec_deg"])
    )
    response = np.column_stack(
        (
            (candidate["dra_deg"] - baseline["dra_deg"]) * cos_dec,
            candidate["ddec_deg"] - baseline["ddec_deg"],
        )
    )
    scale = -float(np.sum(initial * response) / np.sum(response * response))
    proposed_amplitude = args.candidate_amplitude * scale

    print(f"best linear response scale: {scale:.6f}")
    print(
        "candidate amplitude: "
        f"{args.candidate_amplitude:.6f} deg; "
        f"projected amplitude: {proposed_amplitude:.6f} deg"
    )
    print(
        "tangent-plane RMS (deg): "
        f"baseline={rms(initial):.6f}; "
        f"candidate={rms(initial + response):.6f}; "
        f"linear projection={rms(initial + scale * response):.6f}"
    )
    print(
        "response correlation: "
        f"RA={np.corrcoef(baseline['dra_deg'], candidate['dra_deg'] - baseline['dra_deg'])[0, 1]:.6f}; "
        f"Dec={np.corrcoef(baseline['ddec_deg'], candidate['ddec_deg'] - baseline['ddec_deg'])[0, 1]:.6f}"
    )


if __name__ == "__main__":
    main()
