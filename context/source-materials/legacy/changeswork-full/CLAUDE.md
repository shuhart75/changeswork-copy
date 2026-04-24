# Project Working Agreement (for Claude Code / Agents)

This repository is primarily a **documentation + HTML prototype** handoff (not a runnable product).

## Sources Of Truth

- Domain/spec: `spec/domain_model.md` (primary), plus `spec/data_model.puml`, `spec/state_machine.puml`
- MVP planning (current): `planning/mvp/current/`
- MVP prototype (current): `prototypes/current.html`
- Handoff bundle for team/customer demos: `final-spec/`

## Structure Rules (to avoid parallel artifact trees)

- Do not add new "work files" to repo root. Use:
  - `notes/` for drafts/scratch
  - `archive/` for old materials
- MVP planning is versioned:
  - Frozen versions live in `planning/mvp/versions/v6.*`
  - `planning/mvp/current` must point to exactly one version (symlink)
  - Compatibility symlinks: `planning/mvp/tasks -> current/tasks`, `planning/mvp/gantt -> current/gantt`
- Prototype is part of MVP:
  - Canonical entry: `prototypes/current.html` (symlink to `prototypes/mvp/prototype.html`)
  - Everything else goes to `prototypes/archive/`
  - Compatibility: `Prototipes -> prototypes` (symlink)
- Never edit frozen versions in-place (ex: `planning/mvp/versions/v6.0`, `v6.1`). Create a new version instead.

## Planning Laws (non-negotiable)

These rules apply to **all planning artifacts** (PlantUML gantt, TaskJuggler, and any exports).

- **No >100% utilization** for any resource under any circumstances.
- **Baseline estimates are sacred**: task durations are always in “100% productivity days”. Do not change estimates to compensate for reduced productivity; model capacity only via `{X:NN%}` (PlantUML) / `efficiency` (TaskJuggler).
- **Any removal of non‑MVP “gates”** (e.g., starting non‑MVP work before the MVP milestone) **MUST** be accompanied by explicit **resource-leveling / sequencing constraints** for the affected resources, so that charts never imply parallel work beyond capacity.
- **Always respect declared maximum productivity/capacity** for each resource as a hard upper bound (e.g., `F2:50%` means FE2 cannot be scheduled above 50%; future changes may set other resources to <100%).
- **If a resource productivity changes over time** (example: FE2 becomes 100% from 2026/05/01): do not change mid-task productivity; for tasks crossing the boundary date, classify the whole task as 50% vs 100% by majority of its workdays (before/after).

Operational notes:
- Portable reference: `PLANNING_LAWS.md`
- Validation: `python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_commander.puml`
- PlantUML gantt: enforce this via a dedicated `Resource leveling / sequencing constraints` section (typically at the end of the file).
- TaskJuggler: model capacity via `efficiency` (or equivalent) and add dependencies/limits to prevent overlaps.
- `planning/mvp/current/gantt/mvp_gantt_chart_current.puml` is the frozen baseline view; `planning/mvp/current/gantt/mvp_gantt_chart_current_actualized.puml` is the fact/forecast tracking view. Do not treat either of them as the validator input for dependency checks.
- Known validator limitation: `VAC_*` blocks with explicit `starts YYYY/MM/DD` dates can still trigger false positives in `mvp_gantt_chart_commander.puml`.

## Using planning agents (required workflow)

When using a teammate agent to modify the MVP plan:

1) The agent must read and follow `PLANNING_LAWS.md`.
2) The agent may change only sequencing/dependencies/resource productivity annotations — **not** baseline estimates.
3) After any change to the gantt, the agent must run the validator:

```bash
python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_commander.puml
```

The agent may only present results if the validator reports **OK**.

## Git Workflow

### Branching

- Keep `master` (or `main`) always handoff-ready.
- Work only in feature branches: `work/<area>-<short>`
  - examples: `work/mvp-v6.3-estimates`, `work/prototype-fix-nav`, `work/spec-v3.2`

### Commits

- One purpose per commit.
- Message format: `<area>: <what> (refs: spec vX.Y, mvp v6.Z)`
  - areas: `spec`, `planning`, `prototype`, `docs`, `final-spec`
- If you change MVP estimates/dependencies:
  - update BOTH `planning/mvp/current/gantt/*` and the relevant `planning/mvp/current/tasks/*`

### Tags (snapshots)

- Handoff/demo snapshots (annotated): `handoff-YYYY-MM-DD`
- MVP plan versions: `mvp-v6.2`, `mvp-v6.3`, ...
- Spec versions (if you formalize them): `spec-v3.1`, `spec-v3.2`, ...

Example:
```bash
git checkout -b work/mvp-v6.3-estimates
# ... edits ...
git commit -am "planning: sync estimates with gantt (refs: spec v3.1, mvp v6.3)"
git checkout master
git merge --no-ff work/mvp-v6.3-estimates
git tag -a mvp-v6.3 -m "MVP plan v6.3 (gantt+tasks aligned)"
git tag -a handoff-2026-03-11 -m "Handoff bundle: prototype+spec+mvp plan"
```

## Pre-Merge Checklist (to master/main)

- Prototype changes:
  - `python3 scripts/validate_prototype.py prototypes/current.html`
- MVP planning changes:
  - `planning/mvp/current/` points to the intended `planning/mvp/versions/v6.*`
  - `planning/mvp/tasks` and `planning/mvp/gantt` still point to `current/*`
  - `python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_commander.puml`
- Handoff release:
  - update `final-spec/` to match current spec/planning/prototype
  - tag `handoff-YYYY-MM-DD`

## Note About `spec/GUIDE.md`

`spec/GUIDE.md` currently contains agent-style guidance (historically named "GUIDE").
Use `spec/domain_model.md` as the semantic source of truth regardless of naming.
