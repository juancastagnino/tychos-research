"""Compare TYCHOS Eros exports while changing annual-centre geometry.

This is a direct TYCHOS-to-TYCHOS comparison: it does not use JPL. Its purpose
is to measure how closely a candidate Eros geometry reproduces an accepted
TYCHOS export at the same timestamps.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np


REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_DIRECTORY = REPOSITORY / "00-new-tychos"
DEFAULT_REFERENCE = DEFAULT_DIRECTORY / "eros_ephemerides_with_residuals.txt"
DEFAULT_CANDIDATE = DEFAULT_DIRECTORY / "eros_new_hierarchy.txt"
DEFAULT_ZERO_RESIDUAL = DEFAULT_DIRECTORY / "eros_ephemerides_without_residuals.txt"

ROW = re.compile(
    r"^(\d{4}-\d{2}-\d{2})\s*\|\s*"
    r"(\d{2}:\d{2}:\d{2})\s*\|\s*"
    r"(\d{2})h(\d{2})m([\d.]+)s\s*\|\s*"
    r"([+-]?\d+)°(\d+)'([\d.]+)\"\s*\|\s*"
    r"([\d.]+)\s*AU\s*\|"
)


def parse(path: Path):
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        date, time, hh, mm, ss, dd, dm, ds, dist = m.groups()
        ra = 15.0 * (float(hh) + float(mm) / 60.0 + float(ss) / 3600.0)
        sign = -1.0 if dd.startswith("-") else 1.0
        dec = sign * (abs(float(dd)) + float(dm) / 60.0 + float(ds) / 3600.0)
        rows.append((date + " " + time, ra, dec, float(dist)))
    return rows


def wrap_degrees(values: np.ndarray) -> np.ndarray:
    return (values + 180.0) % 360.0 - 180.0


def angular_separation(ra_a, dec_a, ra_b, dec_b):
    ra_a, dec_a, ra_b, dec_b = map(np.radians, (ra_a, dec_a, ra_b, dec_b))
    dot = (
        np.sin(dec_a) * np.sin(dec_b)
        + np.cos(dec_a) * np.cos(dec_b) * np.cos(ra_a - ra_b)
    )
    return np.degrees(np.arccos(np.clip(dot, -1.0, 1.0)))


def report(reference_path: Path, candidate_path: Path, label: str) -> None:
    reference = parse(reference_path)
    candidate = parse(candidate_path)
    if len(reference) != len(candidate) or any(
        left[0] != right[0] for left, right in zip(reference, candidate)
    ):
        raise ValueError("Exports must contain the same timestamps in the same order")

    reference_ra = np.array([row[1] for row in reference])
    reference_dec = np.array([row[2] for row in reference])
    reference_distance = np.array([row[3] for row in reference])
    candidate_ra = np.array([row[1] for row in candidate])
    candidate_dec = np.array([row[2] for row in candidate])
    candidate_distance = np.array([row[3] for row in candidate])
    metrics = [
        ("RA (deg)", wrap_degrees(candidate_ra - reference_ra)),
        ("Declination (deg)", candidate_dec - reference_dec),
        (
            "Angular separation (deg)",
            angular_separation(reference_ra, reference_dec, candidate_ra, candidate_dec),
        ),
        ("Distance (AU)", candidate_distance - reference_distance),
    ]

    print(f"\n{label}")
    print(f"  Reference: {reference_path.name}")
    print(f"  Candidate: {candidate_path.name}")
    print(f"  Samples: {len(reference):,}; {reference[0][0]} to {reference[-1][0]}")
    print("  Metric                         mean          RMS       max |difference|")
    for name, values in metrics:
        print(
            f"  {name:<27} {np.mean(values):>10.6f} "
            f"{np.sqrt(np.mean(values * values)):>12.6f} "
            f"{np.max(np.abs(values)):>18.6f}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=DEFAULT_REFERENCE)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument(
        "--include-zero-residual",
        action="store_true",
        help="Also report the archived zero-residual export against the reference.",
    )
    args = parser.parse_args()
    report(args.reference, args.candidate, "Eros candidate versus accepted reference")
    if args.include_zero_residual:
        report(
            args.reference,
            DEFAULT_ZERO_RESIDUAL,
            "Archived zero-residual Eros versus accepted reference",
        )


if __name__ == "__main__":
    main()
