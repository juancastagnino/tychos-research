#!/usr/bin/env python3
"""Compare and report selected bodies, replacing fixed outputs on each run."""
import argparse
import csv
from datetime import datetime, timezone
import errno
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time

import analyze_ephemerides
import compare_ephemerides
import generate_report
from download_jpl import load_defaults
from ephemeris_io import tychos_blocks, jpl_blocks, validate_jpl_header, select_block

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
DERIVED = ROOT / "data/derived"

REFERENCE_OUTPUTS = {
    "apparent-of-date": {"suffix": "_apparent_of_date", "short_label": "True-of-date apparent"},
}


def publish_file(source, destination, attempts=5, retry_delay=0.25):
    """Publish a complete file atomically, tolerating brief OneDrive locks."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staged_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    staged = Path(staged_name)
    try:
        shutil.copyfile(source, staged)
        for attempt in range(attempts):
            try:
                os.replace(staged, destination)
                return
            except OSError as error:
                retryable = error.errno in (errno.EACCES, errno.EINVAL) or getattr(
                    error, "winerror", None
                ) in (5, 32)
                if not retryable or attempt == attempts - 1:
                    raise OSError(
                        f"Could not replace {destination}. Close it in Excel or "
                        "another program and, if necessary, pause OneDrive sync, "
                        f"then rerun the analysis. Original error: {error}"
                    ) from error
                time.sleep(retry_delay)
    finally:
        staged.unlink(missing_ok=True)


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_inputs(body, config, tychos_path, jpl_path, blocks=None):
    if blocks is None:
        blocks = (tychos_blocks(tychos_path.read_text(encoding="utf-8-sig")),
                  jpl_blocks(jpl_path.read_text(encoding="utf-8-sig")))
    ty_text = select_block(blocks[0], body, "TYCHOS")
    jp_text = select_block(blocks[1], config['target_id'], "JPL")
    validate_jpl_header(jp_text)
    ty = compare_ephemerides.parse_tychos(ty_text, strict=True)
    jp = compare_ephemerides.parse_jpl(jp_text, strict=True)
    if not ty or set(ty) != set(jp):
        raise ValueError(f"{body}: empty data or different timestamps; align the two exports")
    result = {}
    for key, path in (("tychos", tychos_path), ("jpl", jpl_path)):
        path = path.resolve()
        name = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        result[key] = {"path": name, "sha256": fingerprint(path)}
    return result


def safe_cell(value):
    return str(value).replace("|", "/").replace("\n", " ")


def write_overview(configs):
    lines = ["# Ephemeris comparison by body", "",
             "Latest results per body. Different intervals or export configurations are not a controlled A/B comparison.", "",
             "Input status compares file hashes only; it does not verify which simulator settings produced an export.", "",
             "| Body | JPL reference | Input status | Samples | Interval | RMS RA | RMS Dec | RMS separation | Export configuration |",
             "|---|---|---|---:|---|---:|---:|---:|---|"]
    for body, config in configs.items():
        found = False
        for mode, output in REFERENCE_OUTPUTS.items():
            prefix = body + output["suffix"]
            path = REPORTS / f"{prefix}_summary.json"
            if not path.exists():
                continue
            found = True
            s = json.loads(path.read_text(encoding="utf-8"))
            provenance = s.get("provenance", {})
            inputs = provenance.get("inputs", {})
            fresh = all(k in inputs and (ROOT/inputs[k]["path"]).exists()
                        and fingerprint(ROOT/inputs[k]["path"]) == inputs[k]["sha256"] for k in ("tychos", "jpl"))
            status = "Current" if fresh else "Stale or unverified"
            dec = f"{s['declination_residual']['rms_deg']:.6f}°"
            sep = f"{s['angular_separation']['rms_deg']:.6f}°"
            ra = f"{s['ra_residual']['rms_deg']:.6f}°"
            label = safe_cell(provenance.get("export_label", "Not recorded"))
            reference = safe_cell(s.get("reference", output["short_label"]))
            lines.append(
                f"| [{body}]({prefix}_ephemeris_report.md) | {reference} | {status} | {s['n_samples']} | "
                f"{s['start']} to {s['stop']} | {ra} | {dec} | {sep} | {label} |"
            )
        if not found:
            lines.append(f"| {body} | — | No analysis | — | — | — | — | — | — |")
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS/"ephemeris_overview.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def write_notes(summaries):
    lines = ["# Analysis notes", "", "Diagnostics from the bodies processed in this run; hypotheses are not physical conclusions.", "",
             "Read the [research README](../README.md) for the retained baselines and comparison conventions.", ""]
    for prefix, s in summaries.items():
        body = s["body"]
        reference_label = "true-of-date apparent"
        lines += [f"## {body.title()} — {reference_label}", "", f"Interval: {s['start']} to {s['stop']}; {s['n_samples']} samples.", "",
                  f"Export configuration: {s['provenance']['export_label']}", ""]
        for name, key in (("RA", "ra_residual"), ("Declination", "declination_residual"), ("Angular separation", "angular_separation")):
            v = s[key]
            lines.append(f"- {name}: mean {v['mean_deg']:.6f} deg; RMS {v['rms_deg']:.6f} deg.")
        with (REPORTS/f"{prefix}_fft_peaks.csv").open(encoding='utf-8', newline='') as stream:
            peaks = list(csv.DictReader(stream))[:4]
        if peaks:
            observable = s.get("fft_observable", "right ascension residual")
            lines += [f"- Largest {observable} FFT peaks (finite-window estimates, not fitted orbital periods):"]
            lines += [f"  - {float(p['period_days']):.3f} days, approximately {float(p['amplitude_deg']):.4f} deg." for p in peaks]
        else:
            lines.append("- No FFT peaks available; verify sample count and cadence regularity.")
        lines += [""]
    lines += ["## Questions to investigate", "",
              "- Test whether biases and fitted coefficients transfer to a separate time interval.",
              "- Before interpreting an RA drift as an orbital-speed error or precession, verify the reference conventions and look for shared behavior across bodies. Similar numerical rates alone do not establish a cause.",
              "- Compare global coordinate changes using the same epochs and export settings for all bodies in this run.", ""]
    (REPORTS/'analysis_notes.md').write_text('\n'.join(lines), encoding='utf-8')


def main(argv=None):
    defaults = load_defaults()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bodies", nargs="*", help="Body names from bodies.json, e.g. moon sun mars")
    parser.add_argument("--all", action="store_true", help="Process all registered bodies present in BOTH combined inputs")
    parser.add_argument("--tychos", type=Path, default=ROOT/defaults['tychos'])
    parser.add_argument("--jpl", type=Path, default=ROOT/defaults['jpl'])
    parser.add_argument("--label", help="User-declared export configuration, not inferred from current settings")
    parser.add_argument("--export-settings", type=Path, help="Optional JSON settings known to have been used for these exports")
    parser.add_argument(
        "--reference",
        choices=("apparent-of-date",),
        default="apparent-of-date",
        help="Only apparent-of-date RA/Dec is supported",
    )
    parser.add_argument("--overview-only", action="store_true", help="Refresh input freshness statuses without rerunning analyses")
    args = parser.parse_args(argv)
    configs = json.loads(Path(__file__).with_name("bodies.json").read_text(encoding="utf-8"))
    if args.overview_only:
        if args.bodies or args.all or args.label or args.export_settings:
            parser.error("--overview-only cannot be combined with analysis options")
        write_overview(configs)
        return
    if args.bodies and args.all:
        parser.error("Specify body names OR --all")
    tychos_path, jpl_path = args.tychos.resolve(), args.jpl.resolve()
    blocks = (tychos_blocks(tychos_path.read_text(encoding="utf-8-sig")),
              jpl_blocks(jpl_path.read_text(encoding="utf-8-sig")))
    bodies = list(dict.fromkeys(args.bodies or defaults['bodies']))
    if args.all:
        bodies = [b for b, c in configs.items() if b in blocks[0] and c['target_id'] in blocks[1]]
        for b, c in configs.items():
            if (b in blocks[0] or c['target_id'] in blocks[1]) and b not in bodies:
                print(f"Skipping {b}: present in only one input")
    if not bodies:
        parser.error("No registered bodies present in both inputs")
    unknown = set(bodies)-set(configs)
    if unknown:
        parser.error(f"Unknown bodies: {sorted(unknown)}")
    # Validate every requested body before replacing any output.
    inputs = {body: check_inputs(body, configs[body], tychos_path, jpl_path, blocks) for body in bodies}
    export_settings = json.loads(args.export_settings.read_text(encoding="utf-8")) if args.export_settings else None
    reference_modes = (args.reference,)
    publications = []
    summaries = {}
    with tempfile.TemporaryDirectory(prefix="tychos-analysis-") as temporary:
        for body in bodies:
            config = configs[body]
            stage = Path(temporary)/body
            stage.mkdir()
            comparison = stage/f"{body}_comparison.csv"
            final_comparison = DERIVED/comparison.name
            compare_ephemerides.main([str(tychos_path), str(jpl_path), '--body', body, '--target-id', config['target_id'], '-o', str(comparison), '--strict'])
            for reference_mode in reference_modes:
                prefix = body + REFERENCE_OUTPUTS[reference_mode]["suffix"]
                analyze_ephemerides.main([
                    str(comparison), "--body", body, "--prefix", prefix,
                    "--out-dir", str(stage), "--reference", reference_mode,
                ])
                summary_path = stage/f"{prefix}_summary.json"
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                old_path = REPORTS/summary_path.name
                old = json.loads(old_path.read_text(encoding="utf-8")).get("provenance", {}) if old_path.exists() else {}
                same_export = old.get("inputs", {}).get("tychos", {}).get("sha256") == inputs[body]["tychos"]["sha256"]
                label = args.label or (old.get("export_label") if same_export else None) or "Not recorded; current settings do not establish export settings"
                settings = export_settings if args.export_settings else (old.get("declared_export_settings") if same_export and not args.label else None)
                summary["input_file"] = final_comparison.relative_to(ROOT).as_posix()
                summary["provenance"] = {"analyzed_at_utc": datetime.now(timezone.utc).isoformat(),
                                         "inputs": inputs[body], "export_label": label,
                                         "declared_export_settings": settings,
                                         "settings_note": "User-declared, not embedded or verified by the TYCHOS export"}
                summaries[prefix] = summary
                summary_path.write_text(json.dumps(summary, indent=2)+"\n", encoding="utf-8")
                report_args = ["--summary", str(summary_path), "--annual", str(stage/f"{prefix}_annual_stats.csv"),
                               "--model-label", f"TYCHOS {body} / {REFERENCE_OUTPUTS[reference_mode]['short_label']}",
                               "--output", str(stage/f"{prefix}_ephemeris_report.md")]
                generate_report.main(report_args)
            for path in stage.iterdir():
                publications.append((path, final_comparison if path == comparison else REPORTS/path.name))
        for body in bodies:
            for source in ("tychos", "jpl"):
                if fingerprint(ROOT/inputs[body][source]["path"]) != inputs[body][source]["sha256"]:
                    raise ValueError("Input changed during analysis; outputs were not replaced")
        for source, destination in publications:
            publish_file(source, destination)
    write_overview(configs)
    write_notes(summaries)
    print("Updated reports/ephemeris_overview.md")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
