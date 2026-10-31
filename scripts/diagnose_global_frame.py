"""Diagnose whether a single rigid equatorial-frame rotation explains residuals.

This is deliberately read-only research.  It fits one small 3-D rotation from
the Sun's TYCHOS-to-JPL vector residuals, applies that *same* rotation to every
available body, and reports the change in apparent RA/Dec/angular residuals.
It does not modify an export or claim that a fitted rotation belongs in the
celestial model.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


DEFAULT_BODIES = (
    "sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",
    "uranus", "neptune", "pluto",
)


def wrap_degrees(value: np.ndarray) -> np.ndarray:
    return (value + 180.0) % 360.0 - 180.0


def radec_to_vector(ra_deg: np.ndarray, dec_deg: np.ndarray) -> np.ndarray:
    ra = np.deg2rad(ra_deg)
    dec = np.deg2rad(dec_deg)
    return np.column_stack((
        np.cos(dec) * np.cos(ra),
        np.sin(dec),
        np.cos(dec) * np.sin(ra),
    ))


def vector_to_radec(vector: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    vector = vector / np.linalg.norm(vector, axis=1)[:, None]
    ra = np.rad2deg(np.arctan2(vector[:, 2], vector[:, 0])) % 360.0
    dec = np.rad2deg(np.arcsin(np.clip(vector[:, 1], -1.0, 1.0)))
    return ra, dec


def angular_distance_deg(first: np.ndarray, second: np.ndarray) -> np.ndarray:
    dot = np.einsum("ij,ij->i", first, second)
    return np.rad2deg(np.arccos(np.clip(dot, -1.0, 1.0)))


def rms(value: np.ndarray) -> float:
    return float(np.sqrt(np.mean(value * value)))


def fit_small_rotation(model: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Return omega in radians where corrected ~= model + omega x model."""
    x, y, z = model.T
    design = np.concatenate((
        np.column_stack((np.zeros_like(x), z, -y)),
        np.column_stack((-z, np.zeros_like(x), x)),
        np.column_stack((y, -x, np.zeros_like(x))),
    ))
    # The design stacks all X equations, then Y, then Z equations.
    target = (reference - model).T.reshape(-1)
    return np.linalg.lstsq(design, target, rcond=None)[0]


def apply_small_rotation(vector: np.ndarray, omega: np.ndarray) -> np.ndarray:
    corrected = vector + np.cross(np.broadcast_to(omega, vector.shape), vector)
    return corrected / np.linalg.norm(corrected, axis=1)[:, None]


def metrics(model: np.ndarray, reference: np.ndarray) -> dict[str, float]:
    model_ra, model_dec = vector_to_radec(model)
    ref_ra, ref_dec = vector_to_radec(reference)
    dra = wrap_degrees(model_ra - ref_ra)
    ddec = model_dec - ref_dec
    sep = angular_distance_deg(model, reference)
    return {
        "ra_mean": float(np.mean(dra)),
        "ra_rms": rms(dra),
        "dec_mean": float(np.mean(ddec)),
        "dec_rms": rms(ddec),
        "sep_mean": float(np.mean(sep)),
        "sep_rms": rms(sep),
    }


def read_vectors(path: Path) -> tuple[np.ndarray, np.ndarray]:
    rows = np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
    model = radec_to_vector(rows["ty_ra_deg"], rows["ty_dec_deg"])
    reference = radec_to_vector(rows["jpl_ra_deg"], rows["jpl_dec_deg"])
    return model, reference


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="analysis folder containing *_residuals.csv")
    parser.add_argument("--output", type=Path, help="Markdown output; defaults to <folder>/global_frame_diagnostic.md")
    parser.add_argument("--bodies", nargs="*", default=DEFAULT_BODIES)
    args = parser.parse_args()

    sun_path = args.folder / "sun_apparent_of_date_residuals.csv"
    if not sun_path.exists():
        raise FileNotFoundError(f"Sun residual CSV not found: {sun_path}")

    sun_model, sun_reference = read_vectors(sun_path)
    omega = fit_small_rotation(sun_model, sun_reference)
    omega_arcmin = np.rad2deg(omega) * 60.0
    magnitude_arcmin = float(np.linalg.norm(omega_arcmin))

    lines = [
        "# Global reference-frame diagnostic",
        "",
        "This is a read-only diagnostic. It fits one constant small 3-D rotation "
        "from the Sun residuals and applies that exact rotation to every body. "
        "It does not modify TYCHOSIUM or any ephemeris export.",
        "",
        "## Fitted Sun-derived rotation",
        "",
        f"- Equatorial X/Y/Z components: `{omega_arcmin[0]:+.5f}`, `{omega_arcmin[1]:+.5f}`, `{omega_arcmin[2]:+.5f}` arcmin.",
        f"- Magnitude: `{magnitude_arcmin:.5f}` arcmin.",
        "",
        "If this were a meaningful global frame mismatch, it should improve several "
        "bodies coherently. A body that barely improves is dominated by local geometry.",
        "",
        "| Body | Angular RMS before | Angular RMS after common rotation | Change | Interpretation |",
        "| --- | ---: | ---: | ---: | --- |",
    ]

    for body in args.bodies:
        path = args.folder / f"{body}_apparent_of_date_residuals.csv"
        if not path.exists():
            continue
        model, reference = read_vectors(path)
        before = metrics(model, reference)
        after = metrics(apply_small_rotation(model, omega), reference)
        change = 100.0 * (before["sep_rms"] - after["sep_rms"]) / before["sep_rms"]
        interpretation = "common-frame compatible" if change > 5.0 else "mostly local residual"
        lines.append(
            f"| {body.title()} | {before['sep_rms']:.6f} deg | {after['sep_rms']:.6f} deg | "
            f"{change:+.2f}% | {interpretation} |"
        )

    lines.extend((
        "",
        "## Interpretation limit",
        "",
        "A successful diagnostic establishes only that a constant coordinate rotation "
        "could explain part of the comparison residual. It does not establish a physical "
        "cause, nor justify adding an export-level correction. Periodic or branch-specific "
        "residuals require separate geometrical investigation.",
        "",
    ))

    output = args.output or args.folder / "global_frame_diagnostic.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
