#!/usr/bin/env python3
"""Validate PlantUML gantt against repo 'Planning Laws'.

Scope (portable):
- Parse a PlantUML gantt file containing task lines like:
    [Label] as [ID] on {RES} lasts N days
  and constraint lines like:
    [A] starts at [B]'s end
- Enforce that tasks allocated to the same resource do not overlap in time
  (i.e., resource load never exceeds 100% of its declared max).

Notes:
- This validator is intentionally conservative. It does not attempt to fully
  emulate PlantUML; it validates feasibility under the repo's modeling
  conventions.
- It assumes a single calendar: Mon–Fri workdays + explicit closed dates.
- It supports resource productivity annotations like {F2:50%} by stretching
  task duration in calendar workdays: effective_days = ceil(baseline / p).
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Dict, List, Optional, Set, Tuple


TASK_RE = re.compile(
    r"^\[(?P<label>[^\]]+)\]\s+as\s+\[(?P<id>[^\]]+)\]\s+on\s+\{(?P<res>[^}]+)\}\s+lasts\s+(?P<days>\d+)\s+days\s*$"
)

# Examples:
#   [A] starts at [B]'s end
#   [A] starts at [B]'s start
DEP_RE = re.compile(
    r"^\[(?P<a>[^\]]+)\]\s+starts\s+at\s+\[(?P<b>[^\]]+)\]'s\s+(?P<kind>start|end)\s*$"
)

PROJECT_START_RE = re.compile(r"^Project\s+starts\s+the\s+(?P<day>\d+)(?:st|nd|rd|th)\s+of\s+(?P<month>[a-zA-Z]+)\s+(?P<year>\d{4})\s*$")
CLOSED_DATE_RE = re.compile(r"^(?P<y>\d{4})/(?P<m>\d{2})/(?P<d>\d{2})\s+is\s+closed\s*$")

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


@dataclass(frozen=True)
class Task:
    id: str
    label: str
    resource: str
    baseline_days: int
    productivity: float  # 1.0 == 100%


@dataclass
class ScheduleItem:
    task: Task
    start: date
    end: date  # inclusive end-of-day (workday)


def parse_resource_token(token: str) -> Tuple[str, float]:
    """Parse {F2:50%} or {F2}. Returns (resource_name, productivity)."""
    token = token.strip()
    if ":" not in token:
        return token, 1.0
    name, rest = token.split(":", 1)
    rest = rest.strip()
    m = re.fullmatch(r"(?P<pct>\d+(?:\.\d+)?)%", rest)
    if not m:
        # Unknown annotation; be strict.
        raise ValueError(f"Unsupported resource annotation: {{{token}}}")
    pct = float(m.group("pct"))
    if pct <= 0 or pct > 100:
        raise ValueError(f"Invalid productivity percent in {{{token}}}")
    return name.strip(), pct / 100.0


def parse_gantt(path: str) -> Tuple[date, Set[date], Dict[str, Task], List[Tuple[str, str, str]]]:
    """Return (project_start, closed_dates, tasks, deps).

    deps: list of (a, b, kind) where kind in {"start", "end"}.
    """
    project_start: Optional[date] = None
    closed: Set[date] = set()
    tasks: Dict[str, Task] = {}
    deps: List[Tuple[str, str, str]] = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("'"):
                continue

            m = PROJECT_START_RE.match(line)
            if m:
                day = int(m.group("day"))
                month_name = m.group("month").lower()
                year = int(m.group("year"))
                if month_name not in MONTHS:
                    raise ValueError(f"Unknown month in project start: {m.group('month')}")
                project_start = date(year, MONTHS[month_name], day)
                continue

            m = CLOSED_DATE_RE.match(line)
            if m:
                y, mo, d = int(m.group("y")), int(m.group("m")), int(m.group("d"))
                closed.add(date(y, mo, d))
                continue

            m = TASK_RE.match(line)
            if m:
                label = m.group("label")
                tid = m.group("id")
                res_token = m.group("res")
                baseline_days = int(m.group("days"))

                res_name, prod = parse_resource_token(res_token)

                if tid in tasks:
                    raise ValueError(f"Duplicate task id: {tid}")
                tasks[tid] = Task(
                    id=tid,
                    label=label,
                    resource=res_name,
                    baseline_days=baseline_days,
                    productivity=prod,
                )
                continue

            m = DEP_RE.match(line)
            if m:
                deps.append((m.group("a"), m.group("b"), m.group("kind")))
                continue

    if project_start is None:
        raise ValueError("Could not find 'Project starts the ...' line")

    return project_start, closed, tasks, deps


def is_workday(d: date, closed: Set[date]) -> bool:
    if d in closed:
        return False
    # Mon-Fri
    return d.weekday() < 5


def next_workday(d: date, closed: Set[date]) -> date:
    cur = d
    while not is_workday(cur, closed):
        cur += timedelta(days=1)
    return cur


def add_workdays(start: date, workdays: int, closed: Set[date]) -> date:
    """Return inclusive end date after 'workdays' workdays starting at 'start'.

    If workdays == 1: end == start (if start is a workday).
    """
    if workdays <= 0:
        raise ValueError("workdays must be positive")

    cur = next_workday(start, closed)
    remaining = workdays - 1
    while remaining > 0:
        cur += timedelta(days=1)
        if is_workday(cur, closed):
            remaining -= 1
    return cur


def ceil_div(a: int, b: float) -> int:
    return int(math.ceil(a / b))


def topo_order(tasks: Dict[str, Task], deps: List[Tuple[str, str, str]]) -> List[str]:
    # Build edges b -> a
    incoming: Dict[str, int] = {tid: 0 for tid in tasks}
    outgoing: Dict[str, List[str]] = {tid: [] for tid in tasks}

    for a, b, _kind in deps:
        if a not in tasks or b not in tasks:
            # Ignore constraints involving non-task ids (defensive)
            continue
        outgoing[b].append(a)
        incoming[a] += 1

    q = [tid for tid, deg in incoming.items() if deg == 0]
    order: List[str] = []

    while q:
        tid = q.pop()
        order.append(tid)
        for nxt in outgoing[tid]:
            incoming[nxt] -= 1
            if incoming[nxt] == 0:
                q.append(nxt)

    if len(order) != len(tasks):
        # Cycle or missing tasks in deps
        # Provide a helpful hint.
        cyclic = [tid for tid, deg in incoming.items() if deg > 0]
        raise ValueError(f"Dependency graph has a cycle or unresolved refs. In-cycle: {', '.join(cyclic[:10])}")

    return order


def compute_schedule(
    project_start: date,
    closed: Set[date],
    tasks: Dict[str, Task],
    deps: List[Tuple[str, str, str]],
) -> Dict[str, ScheduleItem]:
    # Pre-index deps by dependent task
    dep_index: Dict[str, List[Tuple[str, str]]] = {tid: [] for tid in tasks}
    for a, b, kind in deps:
        if a in tasks and b in tasks:
            dep_index[a].append((b, kind))

    order = topo_order(tasks, deps)
    sched: Dict[str, ScheduleItem] = {}

    for tid in order:
        task = tasks[tid]

        # Earliest start is project start, bumped by dependencies.
        earliest = project_start
        for b, kind in dep_index.get(tid, []):
            pred = sched[b]
            if kind == "end":
                candidate = pred.end + timedelta(days=1)
            else:  # start
                candidate = pred.start
            if candidate > earliest:
                earliest = candidate

        start = next_workday(earliest, closed)
        effective_days = ceil_div(task.baseline_days, task.productivity)
        end = add_workdays(start, effective_days, closed)

        sched[tid] = ScheduleItem(task=task, start=start, end=end)

    return sched


def find_overlaps(items: List[ScheduleItem]) -> List[Tuple[ScheduleItem, ScheduleItem]]:
    overlaps: List[Tuple[ScheduleItem, ScheduleItem]] = []
    items_sorted = sorted(items, key=lambda x: (x.start, x.end))

    for i in range(len(items_sorted)):
        a = items_sorted[i]
        for j in range(i + 1, len(items_sorted)):
            b = items_sorted[j]
            if b.start > a.end:
                break
            # overlap (inclusive end)
            overlaps.append((a, b))

    return overlaps


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate PlantUML gantt against Planning Laws")
    ap.add_argument("gantt", help="Path to PlantUML gantt .puml file")
    ap.add_argument("--show-schedule", action="store_true", help="Print computed task schedule")
    args = ap.parse_args(argv)

    try:
        project_start, closed, tasks, deps = parse_gantt(args.gantt)
        sched = compute_schedule(project_start, closed, tasks, deps)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    by_res: Dict[str, List[ScheduleItem]] = {}
    for item in sched.values():
        by_res.setdefault(item.task.resource, []).append(item)

    any_errors = False

    for res, items in sorted(by_res.items(), key=lambda x: x[0]):
        ovs = find_overlaps(items)
        if ovs:
            any_errors = True
            print(f"\nOVERLAPS for resource {res}:")
            for a, b in ovs:
                print(
                    f"  - {a.task.id} ({a.start}..{a.end}, {a.task.baseline_days}d @ {a.task.productivity:.2f})"
                    f" overlaps {b.task.id} ({b.start}..{b.end}, {b.task.baseline_days}d @ {b.task.productivity:.2f})"
                )

    if args.show_schedule:
        print("\nSCHEDULE:")
        for tid, item in sorted(sched.items(), key=lambda x: (x[1].start, x[1].end, x[0])):
            t = item.task
            eff = ceil_div(t.baseline_days, t.productivity)
            print(
                f"  {t.id:16} {item.start}..{item.end}  res={t.resource}  baseline={t.baseline_days}d  prod={t.productivity:.2f}  effective={eff}d"
            )

    if any_errors:
        print("\nFAIL: capacity law violated (>100% load via overlaps).", file=sys.stderr)
        return 1

    print("OK: no overlaps detected; capacity law satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
