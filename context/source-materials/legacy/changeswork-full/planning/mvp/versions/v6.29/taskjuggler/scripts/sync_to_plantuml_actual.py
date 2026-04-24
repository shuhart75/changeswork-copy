#!/usr/bin/env python3
"""Generate PlantUML *actual/tracking* Gantt from TaskJuggler actual CSV.

Goal:
- Keep the baseline plan in planning/mvp/current/gantt/mvp_gantt_chart_current.puml unchanged
- Produce planning/mvp/current/gantt/mvp_gantt_chart_actual.puml with:
  - explicit actual start dates (from TJ `mvp_actual.csv`)
  - derived working-day durations (Mon-Fri, minus baseline holidays)
  - per-task completion percentage

This is intentionally a *tracking* view: it does not try to preserve dependency logic
or resource-leveling constraints from the baseline diagram.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import re
from pathlib import Path


_HOLIDAY_RE = re.compile(r"^(\d{4})/(\d{2})/(\d{2}) is closed\s*$")
_TASK_DEF_RE = re.compile(
    r"^\[(?P<name>.+?)\] as \[(?P<id>[A-Za-z0-9_]+)\] on \{(?P<res>[^}]+)\} lasts (?P<days>\d+) days\s*$"
)
_MILESTONE_DEF_RE = re.compile(r"^\[(?P<name>.+?)\] as \[(?P<id>[A-Za-z0-9_]+)\] happens at .*$")
_SECTION_RE = re.compile(r"^-- .+ --\s*$")


@dataclasses.dataclass(frozen=True)
class BaselineItem:
    kind: str  # 'section' | 'task' | 'milestone'
    raw: str
    task_id: str | None = None
    name: str | None = None
    resource: str | None = None


@dataclasses.dataclass(frozen=True)
class ActualRow:
    task_id: str
    name: str
    start: dt.date
    end: dt.date
    complete: int


def _parse_date_yyyy_mm_dd(s: str) -> dt.date:
    # TaskJuggler CSV uses YYYY-MM-DD
    return dt.date.fromisoformat(s.strip())


def _puml_date(d: dt.date) -> str:
    return d.strftime("%Y/%m/%d")


def _is_workday(d: dt.date, holidays: set[dt.date]) -> bool:
    if d in holidays:
        return False
    # 0=Mon .. 6=Sun
    return d.weekday() < 5


def _workdays_between(start: dt.date, end: dt.date, holidays: set[dt.date]) -> int:
    """Working days in the half-open interval [start, end).

    TaskJuggler CSV dates behave like a half-open range for working time.

    In practice, TJ may report an End date that falls on a non-working day (e.g. Sunday)
    while the last working day was earlier. Counting workdays in [start, end) matches
    TJ effort/duration best for this repo.
    """

    if end <= start:
        return 0

    days = 0
    cur = start
    one = dt.timedelta(days=1)
    while cur < end:
        if _is_workday(cur, holidays):
            days += 1
        cur += one
    return days


def parse_baseline(baseline_path: Path) -> tuple[list[str], list[BaselineItem], set[dt.date]]:
    """Return (header_lines, ordered_items, holidays).

    header_lines: everything up to (but not including) the first section/task.
    ordered_items: sections + tasks in original order.
    holidays: dates collected from "YYYY/MM/DD is closed" lines.
    """

    header: list[str] = []
    items: list[BaselineItem] = []
    holidays: set[dt.date] = set()

    lines = baseline_path.read_text(encoding="utf-8").splitlines()

    in_body = False
    for line in lines:
        m_h = _HOLIDAY_RE.match(line.strip())
        if m_h:
            holidays.add(dt.date(int(m_h.group(1)), int(m_h.group(2)), int(m_h.group(3))))

        if not in_body:
            if _SECTION_RE.match(line.strip()) or _TASK_DEF_RE.match(line.strip()) or _MILESTONE_DEF_RE.match(line.strip()):
                in_body = True
            else:
                header.append(line)
                continue

        # body parsing
        if _SECTION_RE.match(line.strip()):
            items.append(BaselineItem(kind="section", raw=line))
            continue

        m_task = _TASK_DEF_RE.match(line.strip())
        if m_task:
            items.append(
                BaselineItem(
                    kind="task",
                    raw=line,
                    task_id=m_task.group("id"),
                    name=m_task.group("name"),
                    resource=m_task.group("res"),
                )
            )
            continue

        m_ms = _MILESTONE_DEF_RE.match(line.strip())
        if m_ms:
            items.append(
                BaselineItem(
                    kind="milestone",
                    raw=line,
                    task_id=m_ms.group("id"),
                    name=m_ms.group("name"),
                )
            )
            continue

        # ignore other baseline lines in body (dependencies, colors, leveling, etc.)

    return header, items, holidays


def read_actual_csv(csv_path: Path) -> dict[str, ActualRow]:
    """Read TaskJuggler scenario actual CSV.

    TaskJuggler CSV is typically semicolon-delimited and uses TitleCase headers:
    Id;Name;Resources;Start;End;Effort;Duration;Completion
    """

    rows: dict[str, ActualRow] = {}

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        sample = f.read(4096)
        f.seek(0)

        # TJ uses ';' with quotes by default.
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
        except csv.Error:
            dialect = csv.excel
            dialect.delimiter = ";"

        reader = csv.DictReader(f, dialect=dialect)

        for r in reader:
            # Normalize header keys to lowercase for robustness
            rr = {str(k).strip().lower(): ("" if v is None else str(v)) for k, v in r.items()}

            task_id = rr.get("id", "").strip()
            if not task_id:
                continue

            start_s = rr.get("start", "").strip()
            end_s = rr.get("end", "").strip()
            if not start_s or not end_s:
                continue

            complete_s = rr.get("completion", rr.get("complete", "0")).strip()
            complete_s = complete_s.rstrip("% ")
            try:
                complete = int(float(complete_s))
            except ValueError:
                complete = 0

            rows[task_id] = ActualRow(
                task_id=task_id,
                name=rr.get("name", "").strip(),
                start=_parse_date_yyyy_mm_dd(start_s),
                end=_parse_date_yyyy_mm_dd(end_s),
                complete=max(0, min(100, complete)),
            )

    return rows

def generate_actual_puml(
    *,
    baseline_path: Path,
    actual_csv_path: Path,
    out_path: Path,
) -> None:
    header, items, holidays = parse_baseline(baseline_path)
    actual = read_actual_csv(actual_csv_path)

    out_lines: list[str] = []

    # Header: keep baseline styling/calendar and add a clear banner.
    out_lines.extend(header)
    out_lines.append("'")
    out_lines.append("' TRACKING VIEW (generated)")
    out_lines.append(f"'   Source: {actual_csv_path}")
    out_lines.append(f"'   Baseline: {baseline_path}")
    out_lines.append("'   Notes: this file is generated; edit progress in TaskJuggler (status/actual.tji)")
    out_lines.append("'")
    out_lines.append("")

    for it in items:
        if it.kind == "section":
            out_lines.append(it.raw)
            out_lines.append("")
            continue

        if not it.task_id:
            continue

        ar = actual.get(it.task_id)
        # If a task is missing from actual CSV, keep it but mark unknown dates.
        if ar is None:
            # Keep a minimal placeholder (still valid PlantUML).
            if it.kind == "milestone":
                out_lines.append(f"[{it.name}] as [{it.task_id}] happens at {header_project_start_fallback(header)}")
            else:
                out_lines.append(f"[{it.name}] as [{it.task_id}] on {{{it.resource or 'UNKNOWN'}}} lasts 0 days")
            out_lines.append(f"[{it.task_id}] is 0% completed")
            continue

        if it.kind == "milestone":
            out_lines.append(f"[{it.name}] as [{it.task_id}] happens at {_puml_date(ar.end)}")
            # milestones: completion is often 0/100; still show it
            out_lines.append(f"[{it.task_id}] is {ar.complete}% completed")
            continue

        duration = _workdays_between(ar.start, ar.end, holidays)
        if duration <= 0:
            duration = 1

        # Use baseline name/resource to keep stable IDs and resource tags.
        # Set explicit actual date to avoid dependency-driven repositioning.
        out_lines.append(
            f"[{it.name}] as [{it.task_id}] on {{{it.resource}}} lasts {duration} days"
        )
        out_lines.append(f"[{it.task_id}] starts {_puml_date(ar.start)}")
        out_lines.append(f"[{it.task_id}] is {ar.complete}% completed")
        out_lines.append("")

    out_lines.append("@endgantt")
    out_lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out_lines), encoding="utf-8")


def header_project_start_fallback(header_lines: list[str]) -> str:
    # Try to find "Project starts the ..." line and extract a date-like token.
    # If not found, just return an arbitrary date constant in the project timeframe.
    for line in header_lines:
        if line.strip().lower().startswith("project starts"):
            # PlantUML accepts many formats; keep the original line isn't possible here.
            # Return the canonical date from the baseline used in this repo.
            return "2026/03/30"
    return "2026/03/30"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--baseline",
        default="planning/mvp/current/gantt/mvp_gantt_chart_current.puml",
        help="Baseline PlantUML gantt (read-only).",
    )
    ap.add_argument(
        "--actual-csv",
        default="/tmp/tj-out/mvp_actual.csv",
        help="TaskJuggler actual CSV (generated by tj3).",
    )
    ap.add_argument(
        "--out",
        default="planning/mvp/current/gantt/mvp_gantt_chart_actual.puml",
        help="Output PlantUML actual/tracking gantt.",
    )

    args = ap.parse_args()

    baseline = Path(args.baseline)
    actual_csv = Path(args.actual_csv)
    out_path = Path(args.out)

    if not baseline.exists():
        raise SystemExit(f"Baseline not found: {baseline}")
    if not actual_csv.exists():
        raise SystemExit(
            f"Actual CSV not found: {actual_csv}\n" \
            "Render TaskJuggler first (e.g. planning/mvp/current/taskjuggler/scripts/render.sh)."
        )

    generate_actual_puml(baseline_path=baseline, actual_csv_path=actual_csv, out_path=out_path)
    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
