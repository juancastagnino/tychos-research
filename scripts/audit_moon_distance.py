#!/usr/bin/env python3
"""Compare TYCHOS Moon distance with JPL Horizons at identical timestamps."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import re

from ephemeris_io import jpl_blocks, select_block, tychos_blocks

AU_KM = 149_597_870.7
ROOT = Path(__file__).resolve().parents[1]


def percentile(values, fraction):
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - position) + ordered[upper] * (position - lower)


def read_tychos_moon(path):
    text = Path(path).read_text(encoding="utf-8-sig")
    block = select_block(tychos_blocks(text), "moon", "TYCHOS")
    rows = {}
    for line in block.splitlines():
        parts = [part.strip() for part in line.split("|")]
        if len(parts) < 5 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", parts[0]):
            continue
        match = re.fullmatch(r"([-+]?\d+(?:\.\d+)?)\s*km", parts[4], re.I)
        if not match:
            continue
        timestamp = datetime.strptime(parts[0] + " " + parts[1], "%Y-%m-%d %H:%M:%S")
        rows[timestamp] = float(match.group(1))
    return rows


def read_jpl_moon(path, target_id="301"):
    text = Path(path).read_text(encoding="utf-8-sig")
    block = select_block(jpl_blocks(text), target_id, "JPL")
    before, table = block.split("$$SOE", 1)
    table, _ = table.split("$$EOE", 1)
    header = next((line for line in before.splitlines() if "Date__(UT)" in line), None)
    if not header:
        raise ValueError("JPL Moon block has no CSV table header")
    columns = [column.strip().lower() for column in header.split(",")]
    try:
        distance_index = columns.index("delta")
    except ValueError as error:
        raise ValueError(
            "JPL bundle has no geocentric range column; redownload it with QUANTITIES='1,2,20'"
        ) from error
    rows = {}
    for raw in table.splitlines():
        columns = [column.strip() for column in raw.split(",")]
        if len(columns) <= distance_index:
            continue
        try:
            timestamp = datetime.strptime(columns[0], "%Y-%b-%d %H:%M:%S")
            rows[timestamp] = float(columns[distance_index]) * AU_KM
        except ValueError:
            continue
    return rows


def nearest(rows, target):
    return min(rows, key=lambda row: abs(row[0] - target))


def main(argv=None):
    defaults = json.loads(Path(__file__).with_name("analysis_config.json").read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tychos", type=Path, default=ROOT / defaults["tychos"])
    parser.add_argument("--jpl", type=Path, default=ROOT / defaults["jpl"])
    parser.add_argument("--output", type=Path, default=ROOT / "reports" / "moon_distance_audit.md")
    parser.add_argument("--event", default="2015-03-20 09:45:38")
    args = parser.parse_args(argv)

    tychos = read_tychos_moon(args.tychos)
    jpl = read_jpl_moon(args.jpl)
    common = sorted(set(tychos) & set(jpl))
    if not common:
        raise SystemExit("No common Moon timestamps")
    rows = [(date, tychos[date], jpl[date], tychos[date] - jpl[date]) for date in common]
    errors = [row[3] for row in rows]
    absolute = [abs(value) for value in errors]
    event = nearest(rows, datetime.fromisoformat(args.event))
    worst = max(rows, key=lambda row: abs(row[3]))
    ty_min = min(rows, key=lambda row: row[1])
    ty_max = max(rows, key=lambda row: row[1])
    jp_min = min(rows, key=lambda row: row[2])
    jp_max = max(rows, key=lambda row: row[2])

    def line(row):
        return f"{row[0]} | {row[1]:,.0f} | {row[2]:,.0f} | {row[3]:+,.0f}"

    report = f"""# Moon distance audit

Matched geocentric timestamps: `{len(rows):,}`.

| Statistic | Value |
|---|---:|
| Mean TYCHOS − JPL | `{sum(errors)/len(errors):+,.1f} km` |
| RMS distance error | `{math.sqrt(sum(value*value for value in errors)/len(errors)):,.1f} km` |
| Mean absolute error | `{sum(absolute)/len(absolute):,.1f} km` |
| 95th percentile absolute error | `{percentile(absolute, .95):,.1f} km` |
| Maximum absolute error | `{abs(worst[3]):,.1f} km` |

| Event | Timestamp | TYCHOS km | JPL km | Difference km |
|---|---|---:|---:|---:|
| Requested event, nearest sample | {line(event)} |
| Worst matched sample | {line(worst)} |
| TYCHOS minimum | {line(ty_min)} |
| TYCHOS maximum | {line(ty_max)} |
| JPL minimum | {line(jp_min)} |
| JPL maximum | {line(jp_max)} |

Positive differences mean TYCHOS places the Moon farther from Earth.
"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(report)
    print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
