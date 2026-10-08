#!/usr/bin/env python3
"""Generate a compact Markdown report from analyze_ephemerides.py outputs.

Example:
    py scripts/generate_report.py \
        --summary reports/moon_apparent_of_date_summary.json \
        --annual reports/moon_apparent_of_date_annual_stats.csv \
        --output reports/moon_apparent_of_date_ephemeris_report.md

Optionally provide --baseline-summary to add before/after improvement figures.
"""

import argparse
import csv
import json
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv(path):
    if not path:
        return []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def fmt(x, digits=4):
    if x is None or x == "":
        return "—"
    return f"{float(x):.{digits}f}"


def improvement(old, new):
    if not old:
        return None
    return 100.0 * (old - new) / old


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--summary", required=True)
    p.add_argument("--annual")
    p.add_argument("--baseline-summary")
    p.add_argument("--model-label")
    p.add_argument("--output", default="reports/moon_apparent_of_date_ephemeris_report.md")
    args = p.parse_args(argv)

    s = load_json(args.summary)
    baseline = load_json(args.baseline_summary) if args.baseline_summary else None
    if s.get('reference_mode') != 'apparent-of-date' or (baseline and baseline.get('reference_mode') != 'apparent-of-date'):
        raise ValueError('Only apparent-of-date summaries are supported')
    annual = load_csv(args.annual)

    lines = []
    body = s.get("body", "moon")
    lines.append(f"# TYCHOS {body.title()} Ephemeris Audit")
    lines.append("")
    lines.append(f"**Model:** {args.model_label or ('Current TYCHOS lunar-plane branch' if body == 'moon' else 'TYCHOS ' + body)}")
    lines.append("")
    lines.append("## Dataset")
    lines.append("")
    lines.append(f"- Samples: **{s['n_samples']}**")
    lines.append(f"- Interval: **{s['start']} → {s['stop']}**")
    lines.append(f"- Median cadence: **{fmt(s.get('cadence_hours_median'), 3)} h**")
    lines.append(f"- Reference: **{s['reference']}**")
    lines.append(f"- Ecliptic residual analysis: {s['ecliptic_rotation']}")
    provenance = s.get("provenance")
    if provenance:
        lines.append(f"- Analysis generated (UTC): {provenance['analyzed_at_utc']}")
        lines.append(f"- Export configuration: {provenance['export_label']}")
        lines.append("- Input hashes and any explicitly supplied export settings are recorded in the summary JSON.")
    lines.append("")

    lines.append("## Current residuals")
    lines.append("")
    lines.append("| Metric | Mean | RMS | P95 abs. | Max abs. |")
    lines.append("|---|---:|---:|---:|---:|")
    metric_rows = ([('RA (coordinate)', 'ra_residual')] if 'ra_residual' in s else []) + [
        ("Declination", "declination_residual"),
        ("Angular separation", "angular_separation"),
    ]
    for label, key in metric_rows:
        d = s[key]
        lines.append(
            f"| {label} | {fmt(d['mean_deg'])}° | {fmt(d['rms_deg'])}° | {fmt(d['p95_abs_deg'])}° | {fmt(d['max_abs_deg'])}° |"
        )
    lines.append("")

    if baseline:
        lines.append("## Baseline comparison")
        lines.append("")
        lines.append("| Metric | Baseline RMS | Current RMS | Improvement |")
        lines.append("|---|---:|---:|---:|")
        baseline_rows = [
            ("RA (coordinate)", "ra_residual"),
            ("Declination", "declination_residual"),
            ("Angular separation", "angular_separation"),
        ]
        for label, key in baseline_rows:
            old = baseline[key]["rms_deg"]
            new = s[key]["rms_deg"]
            imp = improvement(old, new)
            lines.append(f"| {label} | {fmt(old)}° | {fmt(new)}° | {fmt(imp, 2)}% |")
        lines.append("")

    if annual:
        lines.append("## Annual stability")
        lines.append("")
        lines.append("| Year | N | RMS RA | RMS Dec | RMS separation |")
        lines.append("|---:|---:|---:|---:|---:|")
        for r in annual:
            lines.append(
                f"| {r['year']} | {r['n']} | {fmt(r['rms_dra_deg'])}° | "
                f"{fmt(r['rms_ddec_deg'])}° | {fmt(r['rms_sep_deg'])}° |"
            )
        lines.append("")

    lines.append("## Interpretation notes")
    lines.append("")
    lines.append("- JPL apparent coordinates include light-time, light deflection, stellar aberration, precession and nutation.")
    lines.append("- J2000 ecliptic residuals are intentionally omitted because fixed J2000 obliquity is not valid for true-of-date RA/Dec.")
    lines.append("- Compare RA, declination and angular separation using the same epochs and declared export settings.")
    lines.append("- A lower residual does not establish exact equivalence of the native TYCHOS and JPL coordinate conventions.")
    lines.append("")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written to: {output}")


if __name__ == "__main__":
    main()
