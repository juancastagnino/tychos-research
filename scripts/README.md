# Maintained analysis scripts

Reusable Python tools for the independent `tychos-research` repository.
Run commands from the repository root. See the [root README](../README.md)
for environment setup, input configuration and the complete comparison workflow.
The simulator and model settings are maintained in a separate project.

## Normal workflow

| File | Responsibility |
|---|---|
| `analysis_config.json` | Default bodies, interval, cadence and input paths |
| `bodies.json` | TYCHOS body names and JPL Horizons target IDs |
| `download_jpl.py` | Download one Horizons bundle containing only apparent true-of-date coordinates |
| `run_analysis.py` | Validate inputs and orchestrate comparison, analysis and report generation |
| `compare_ephemerides.py` | Match TYCHOS and JPL samples for one body |
| `analyze_ephemerides.py` | Calculate RA/Dec/angular metrics, annual statistics and FFT diagnostics |
| `generate_report.py` | Render a per-body Markdown report |
| `ephemeris_io.py` | Shared strict parsers for TYCHOS and Horizons exports |
| `compare_summary_metrics.py` | Compare generated summary JSON files with any preserved baseline directory |
| `requirements.txt` | Python dependencies |

`run_analysis.py` is the normal entry point. The lower-level scripts are kept
separate so they remain testable and reusable, but ordinarily should not be run
by hand.

## Tests

`test_reference_modes.py` checks apparent true-of-date processing, backward-compatible bundle parsing,
rejection of fixed-frame modes and RA residual diagnostics.

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s scripts -p "test_*.py"
```

## Research convention

All comparisons use apparent-of-date RA/Dec. Fixed-frame ICRF/J2000 and `both`
options are no longer supported. Historical baselines remain unchanged.

Generated reports are replaceable evidence. Preserve the reports, raw exports,
`analysis_config.json` and the exact celestial model together before starting a
new parameter experiment.

## Additional workflows

- [Machine learning](machine_learning/README.md): per-body and shared residual diagnostics.
- [Stellarium](stellarium/README.md): prepare and validate a separate coordinate dataset.

Each workflow documents its own tests. The standard pipeline writes comparisons
to `data/derived/` and reports to `reports/`; it does not update
`00-old-tychos/` or `00-binary-baseline/`.
