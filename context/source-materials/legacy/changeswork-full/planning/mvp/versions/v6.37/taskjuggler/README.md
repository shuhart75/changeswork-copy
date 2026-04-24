# TaskJuggler (commander baseline / tracking)

This folder contains the TaskJuggler model and generated HTML/CSV reports for the current commander baseline.

## Quick start

TaskJuggler requires the output directory to exist.

```bash
# recommended: repo wrapper (renders + opens output folder)
planning/mvp/current/taskjuggler/scripts/render.sh

# or manually:
mkdir -p /tmp/tj-out

# generate HTML + CSV
# (input file is the canonical symlink to the current version)
tj3 planning/mvp/current/taskjuggler/mvp_current.tjp --output-dir /tmp/tj-out

# or run the pinned file directly
tj3 planning/mvp/current/taskjuggler/mvp_commander.tjp --output-dir /tmp/tj-out
```

The wrapper accepts an optional output dir:

```bash
planning/mvp/current/taskjuggler/scripts/render.sh /tmp/tj-out
```

Outputs are written into the given output directory, including:
- `Overview.html`, `Status.html`, `Resources.html`
- `mvp_plan.csv` (scenario `plan`)
- `mvp_actual.csv` (scenario `actual`)

## Plan vs actual scenarios

The model defines nested scenarios:

- `plan` — baseline schedule (what we want)
- `actual` — tracking schedule (same structure, but supports progress overrides)

Progress updates live in:

- `planning/mvp/current/taskjuggler/status/actual.tji`

We keep tracking simple: update only `% complete` per task.

## Sync TJ tracking → PlantUML (actual diagram)

If you want the TaskJuggler **actual** scenario reflected as a separate PlantUML Gantt (while keeping the baseline plan immutable), use:

```bash
# 1) render TJ (generates /tmp/tj-out/mvp_actual.csv)
planning/mvp/current/taskjuggler/scripts/render.sh

# 2) generate PlantUML tracking diagram
python3 planning/mvp/current/taskjuggler/scripts/sync_to_plantuml_actual.py \
  --actual-csv /tmp/tj-out/mvp_actual.csv \
  --out planning/mvp/current/gantt/mvp_gantt_chart_actual.puml
```

The generated diagram contains:
- explicit actual `start` dates per task (from TJ)
- derived durations in **working days** (Mon-Fri, minus the same closed days as the baseline gantt)
- `is XX% completed` lines

Notes:
- This is a **tracking view**, not a re-optimized plan: it intentionally does not replicate baseline dependencies/leveling constraints.
- Baseline plan stays in `planning/mvp/current/gantt/mvp_gantt_chart_current.puml`.

## Which PlantUML file to validate

Use the validator only for the editable dependency-based source:

```bash
python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_commander.puml
```

Do not use the validator on:
- `planning/mvp/current/gantt/mvp_gantt_chart_current.puml` — frozen rendered baseline view
- `planning/mvp/current/gantt/mvp_gantt_chart_current_actualized.puml` — tracking view with explicit factual start dates

The current validator checks dependency-based feasibility and resource overlaps; it does not model the explicit `starts YYYY/MM/DD` format used in the actualized file.
It also still has a known limitation on explicit-start vacation blocks (`VAC_*`) inside `mvp_gantt_chart_commander.puml`.

## PlantUML parity (ALL_DONE date)

The canonical leadership baseline is the frozen PlantUML Gantt:

- `planning/mvp/current/gantt/mvp_gantt_chart_current.puml`

TaskJuggler is used for the underlying calendar/resource calculation, and the frozen PlantUML view is generated from its `plan` scenario so the two formats do not diverge.

### Current commander dates

With holidays, named vacations, and commander coefficient `1.3`, the current baseline produces:

- `MVP_DONE = 2026-07-16`
- `ALL_DONE = 2026-08-02`
