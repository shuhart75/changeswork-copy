# Planning Laws (portable)

These rules are **non‑negotiable** for maintaining an executable plan in both **PlantUML Gantt** and **TaskJuggler**.

## 1) Source of truth

- **Tasks, IDs, dependencies and baseline estimates** live in the editable dependency-based PlantUML source:
  - `planning/mvp/current/gantt/mvp_gantt_chart_commander.puml`
- The canonical current baseline view for leadership is the frozen/rendered file:
  - `planning/mvp/current/gantt/mvp_gantt_chart_current.puml`
- The factual tracking / current forecast view lives separately in:
  - `planning/mvp/current/gantt/mvp_gantt_chart_current_actualized.puml`
- Any derived artifact (TaskJuggler, summaries, exports) must mirror it.

## 2) Baseline estimates are sacred

- Every task estimate is expressed in **baseline “100% productivity days”**.
- **Never change** `lasts N days` (PlantUML) / `duration Nd` (TaskJuggler) to “compensate” for reduced capacity.
- Capacity/productivity must be modeled **only** via:
  - PlantUML resource productivity: `{F2:50%}`
  - TaskJuggler resource efficiency: `efficiency 0.5`

If you both (a) increase duration and (b) lower productivity, you will double‑count and the plan becomes wrong.

## 3) Capacity is a hard cap (no oversubscription)

- A resource must **never** be loaded over its declared maximum productivity/capacity.
- In practice this means: **no overlapping tasks** for the same resource (unless you explicitly model parallel capacity, which we don’t in this repo).

This is treated as a **hard constraint**, not a suggestion.

## 4) If you remove gates, you must add leveling constraints

When you allow non‑MVP tasks to start earlier (e.g., remove `depends QA_REG` / remove “starts at QA_REG end”):

- You **must** add explicit **resource‑leveling sequencing constraints** so the schedule remains feasible.
- In PlantUML this is typically done by adding extra `starts at` lines in a dedicated block (after task definitions) to enforce per‑resource sequential execution.
- In TaskJuggler this is done by adding/adjusting `depends` so that tasks allocated to the same resource cannot overlap.

## 5) Calendar alignment

- Work calendar is **Mon–Fri**.
- Holidays/closed days must match between tools.

## 6) Changing productivity over time (e.g., FE2 50% → 100%)

If a resource productivity changes at a known date (example: **FE2 becomes 100% starting 2026‑05‑01**):

- Do **not** try to change productivity mid‑task.
- For any task that crosses the boundary date, classify the whole task as either “before” or “after” by this rule:
  - **If the majority of the task’s (workday) duration is before the date → treat as 50% for the whole task.**
  - **Otherwise → treat as 100% for the whole task.**

Implementation patterns:
- PlantUML: choose `{F2:50%}` or `{F2}` for the entire task.
- TaskJuggler: allocate the task to `F2_50` or `F2_100` (two resources) based on the same classification.

## 7) Validation is mandatory

After any change to the gantt (tasks, dependencies, gating policy, productivity annotations):

- Run the validator and ensure it reports **no overlaps / no >100% load**.
- Run it against the **editable dependency-based source**, not against the frozen rendered baseline and not against the actualized tracking view.

Suggested command (repo-local):

```bash
python3 scripts/validate_gantt_laws.py planning/mvp/current/gantt/mvp_gantt_chart_commander.puml
```

Why:

- `mvp_gantt_chart_current.puml` is currently a frozen rendered view, not the editable source of dependencies.
- `mvp_gantt_chart_current_actualized.puml` contains explicit factual `starts YYYY/MM/DD` dates; the current validator intentionally does not model that format.
- Known limitation of the current validator: explicit-start vacation blocks (`VAC_*`) in `mvp_gantt_chart_commander.puml` may still produce false positives until the validator is extended for that pattern.
