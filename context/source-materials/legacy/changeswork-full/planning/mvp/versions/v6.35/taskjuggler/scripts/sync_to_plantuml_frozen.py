#!/usr/bin/env python3
"""Generate a frozen PlantUML gantt from a TaskJuggler CSV schedule.

This generator intentionally does not emit dependency lines. PlantUML is used as a
presentation layer only; TaskJuggler remains the planning source of truth.
"""

from __future__ import annotations

import argparse
import csv
import dataclasses
import datetime as dt
import math
import re
from pathlib import Path


_HOLIDAY_RE = re.compile(r"^(\d{4})/(\d{2})/(\d{2}) is closed\s*$")
_SECTION_RE = re.compile(r"^-- .+ --\s*$")
_TASK_DEF_RE = re.compile(
    r"^\[(?P<name>.+?)\] as \[(?P<id>[A-Za-z0-9_]+)\] on \{(?P<res>[^}]+)\} lasts (?P<days>\d+) days\s*$"
)
_MILESTONE_DEF_RE = re.compile(r"^\[(?P<name>.+?)\] as \[(?P<id>[A-Za-z0-9_]+)\] happens at .*$")
_COLOR_RE = re.compile(r"^\[(?P<id>[A-Za-z0-9_]+)\] is colored in (?P<color>.+?)\s*$")
_START_RE = re.compile(r"^\[(?P<id>[A-Za-z0-9_]+)\] starts (?P<date>\d{4}/\d{2}/\d{2})\s*$")
_GENERATED_HEADER_PREFIXES = (
    "' FROZEN VIEW (generated from TaskJuggler CSV)",
    "'   Template:",
    "'   Schedule:",
    "'   TaskJuggler is the planning source of truth.",
    "'   PlantUML is emitted without dependency logic to avoid false overloads.",
)


@dataclasses.dataclass(frozen=True)
class TemplateItem:
    kind: str  # section | comment | task | milestone
    raw: str
    task_id: str | None = None
    name: str | None = None
    resource: str | None = None
    color: str | None = None
    start: str | None = None
    original_lines: tuple[str, ...] = ()


@dataclasses.dataclass(frozen=True)
class ScheduleRow:
    task_id: str
    name: str
    resources: str
    start: dt.date
    end: dt.date
    duration_days: int
    complete: int


def _parse_date_yyyy_mm_dd(value: str) -> dt.date:
    return dt.date.fromisoformat(value.strip())


def _puml_date(value: dt.date) -> str:
    return value.strftime("%Y/%m/%d")


def _is_workday(day: dt.date, holidays: set[dt.date]) -> bool:
    return day.weekday() < 5 and day not in holidays


def _workdays_between(start: dt.date, end: dt.date, holidays: set[dt.date]) -> int:
    if end <= start:
        return 0

    current = start
    days = 0
    one_day = dt.timedelta(days=1)
    while current < end:
        if _is_workday(current, holidays):
            days += 1
        current += one_day
    return days


def parse_template(path: Path) -> tuple[list[str], list[TemplateItem], set[dt.date]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header: list[str] = []
    items: list[TemplateItem] = []
    holidays: set[dt.date] = set()

    in_body = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        holiday_match = _HOLIDAY_RE.match(stripped)
        if holiday_match:
            holidays.add(
                dt.date(
                    int(holiday_match.group(1)),
                    int(holiday_match.group(2)),
                    int(holiday_match.group(3)),
                )
            )

        if not in_body:
            if stripped == "'":
                i += 1
                continue
            if any(stripped.startswith(prefix) for prefix in _GENERATED_HEADER_PREFIXES):
                i += 1
                continue
            if _SECTION_RE.match(stripped) or _TASK_DEF_RE.match(stripped) or _MILESTONE_DEF_RE.match(stripped):
                in_body = True
            else:
                header.append(line)
                i += 1
                continue

        if stripped == "@endgantt":
            break

        if not stripped:
            i += 1
            continue

        if _SECTION_RE.match(stripped):
            items.append(TemplateItem(kind="section", raw=line, original_lines=(line,)))
            i += 1
            continue

        if stripped.startswith("'"):
            items.append(TemplateItem(kind="comment", raw=line, original_lines=(line,)))
            i += 1
            continue

        task_match = _TASK_DEF_RE.match(stripped)
        milestone_match = _MILESTONE_DEF_RE.match(stripped)
        if not task_match and not milestone_match:
            i += 1
            continue

        item_lines = [line]
        color = None
        start = None
        task_id = task_match.group("id") if task_match else milestone_match.group("id")
        name = task_match.group("name") if task_match else milestone_match.group("name")
        resource = task_match.group("res") if task_match else None
        kind = "task" if task_match else "milestone"
        i += 1

        while i < len(lines):
            next_line = lines[i]
            next_stripped = next_line.strip()
            if (
                next_stripped == "@endgantt"
                or _SECTION_RE.match(next_stripped)
                or _TASK_DEF_RE.match(next_stripped)
                or _MILESTONE_DEF_RE.match(next_stripped)
            ):
                break

            item_lines.append(next_line)
            color_match = _COLOR_RE.match(next_stripped)
            if color_match and color_match.group("id") == task_id:
                color = color_match.group("color")

            start_match = _START_RE.match(next_stripped)
            if start_match and start_match.group("id") == task_id:
                start = start_match.group("date")

            i += 1

        items.append(
            TemplateItem(
                kind=kind,
                raw=line,
                task_id=task_id,
                name=name,
                resource=resource,
                color=color,
                start=start,
                original_lines=tuple(item_lines),
            )
        )

    return header, items, holidays


def read_csv(path: Path) -> dict[str, ScheduleRow]:
    rows: dict[str, ScheduleRow] = {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
        except csv.Error:
            dialect = csv.excel
            dialect.delimiter = ";"

        reader = csv.DictReader(fh, dialect=dialect)
        for row in reader:
            normalized = {str(k).strip().lower(): ("" if v is None else str(v)) for k, v in row.items()}
            task_id = normalized.get("id", "").strip()
            if not task_id:
                continue

            start_s = normalized.get("start", "").strip()
            end_s = normalized.get("end", "").strip()
            if not start_s or not end_s:
                continue

            duration_s = normalized.get("duration", "0").strip()
            try:
                duration_days = max(0, math.ceil(float(duration_s)))
            except ValueError:
                duration_days = 0

            complete_s = normalized.get("completion", normalized.get("complete", "0")).strip().rstrip("% ")
            try:
                complete = int(float(complete_s))
            except ValueError:
                complete = 0

            rows[task_id] = ScheduleRow(
                task_id=task_id,
                name=normalized.get("name", "").strip(),
                resources=normalized.get("resources", "").strip(),
                start=_parse_date_yyyy_mm_dd(start_s),
                end=_parse_date_yyyy_mm_dd(end_s),
                duration_days=duration_days,
                complete=max(0, min(100, complete)),
            )
    return rows


def build_resource_legend(schedule: dict[str, ScheduleRow], items: list[TemplateItem]) -> list[str]:
    resource_windows: dict[str, tuple[dt.date, dt.date]] = {}
    resource_labels = {
        "A1": "Analyst 1",
        "A2": "Analyst 2",
        "B1": "Backend Dev 1",
        "B2": "Backend Dev 2",
        "B3": "Backend Dev 3",
        "F1": "Frontend Dev 1",
        "F2:50%": "Frontend Dev 2, 50%",
        "F2": "Frontend Dev 2, 100%",
        "B2:50%": "Backend Dev 2 -> FE, 50%",
        "B3:50%": "Backend Dev 3 -> FE, 50%",
        "Q1": "QA",
    }

    for item in items:
        if item.kind != "task" or not item.task_id or not item.resource:
            continue
        row = schedule.get(item.task_id)
        if row is None:
            continue
        start, end = resource_windows.get(item.resource, (row.start, row.end))
        resource_windows[item.resource] = (min(start, row.start), max(end, row.end))

    legend = [
        "legend bottom",
        "  |= Цвет |= Тип работ |",
        "  |<#lightgreen>| Аналитика |",
        "  |<#lightblue>| Backend |",
        "  |<#lightcoral>| Frontend |",
        "  |<#gold>| QA |",
        "  |<#silver>| Отпуск / недоступность |",
        "  |<#orange>| Milestone |",
        "  ",
    ]

    legend.append("  |= Ресурс |= Использование на диаграмме |= Окно загрузки по TJ |")
    for resource in ["A1", "A2", "B1", "B2", "B3", "F1", "F2:50%", "F2", "B2:50%", "B3:50%", "Q1"]:
        window = resource_windows.get(resource)
        window_s = "-"
        if window:
            window_s = f"{_puml_date(window[0])}..{_puml_date(window[1])}"
        legend.append(f"  | {resource} | {resource_labels[resource]} | {window_s} |")

    legend.extend(
        [
            "  ",
            "  Отпуска отображаются отдельными серебристыми блоками на шкале.",
            "endlegend",
        ]
    )
    return legend


def generate_frozen_puml(*, template_path: Path, csv_path: Path, out_path: Path) -> None:
    header, items, holidays = parse_template(template_path)
    schedule = read_csv(csv_path)

    out_lines: list[str] = []
    out_lines.extend(header)
    out_lines.extend(
        [
            "'",
            "' FROZEN VIEW (generated from TaskJuggler CSV)",
            f"'   Template: {template_path}",
            f"'   Schedule: {csv_path}",
            "'   TaskJuggler is the planning source of truth.",
            "'   PlantUML is emitted without dependency logic to avoid false overloads.",
            "'",
            "",
        ]
    )

    for item in items:
        if item.kind == "section":
            out_lines.append(item.raw)
            out_lines.append("")
            continue

        if item.kind == "comment":
            out_lines.append(item.raw)
            continue

        if not item.task_id:
            continue

        row = schedule.get(item.task_id)
        if row is None:
            out_lines.extend(item.original_lines)
            out_lines.append("")
            continue

        if item.kind == "milestone":
            out_lines.append(f"[{item.name}] as [{item.task_id}] happens at {_puml_date(row.start)}")
            if item.color:
                out_lines.append(f"[{item.task_id}] is colored in {item.color}")
            out_lines.append("")
            continue

        duration = row.duration_days or _workdays_between(row.start, row.end, holidays)
        if duration <= 0:
            duration = 1

        resource = item.resource or row.resources or "UNASSIGNED"
        out_lines.append(f"[{item.name}] as [{item.task_id}] on {{{resource}}} lasts {duration} days")
        out_lines.append(f"[{item.task_id}] starts {_puml_date(row.start)}")
        if item.color:
            out_lines.append(f"[{item.task_id}] is colored in {item.color}")
        if row.complete > 0:
            out_lines.append(f"[{item.task_id}] is {row.complete}% completed")
        out_lines.append("")

    mvp_done = schedule.get("MVP_DONE")
    all_done = schedule.get("ALL_DONE")
    if mvp_done or all_done:
        out_lines.append("note bottom")
        if mvp_done:
            out_lines.append(f"  MVP_DONE: {_puml_date(mvp_done.start)}")
        if all_done:
            out_lines.append(f"  ALL_DONE: {_puml_date(all_done.start)}")
        out_lines.append("end note")
        out_lines.append("")

    out_lines.extend(build_resource_legend(schedule, items))
    out_lines.append("")
    out_lines.append("@endgantt")
    out_lines.append("")

    normalized_lines: list[str] = []
    prev_blank = False
    for line in out_lines:
        if line.strip() == "'":
            continue
        is_blank = line.strip() == ""
        if is_blank and prev_blank:
            continue
        normalized_lines.append(line)
        prev_blank = is_blank

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(normalized_lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        default="planning/mvp/versions/v6.23/gantt/mvp_gantt_chart_commander_current.puml",
        help="PlantUML template used for sections, comments, colors and resource labels.",
    )
    parser.add_argument(
        "--csv",
        default="/tmp/tj-current/mvp_actual.csv",
        help="TaskJuggler CSV schedule.",
    )
    parser.add_argument(
        "--out",
        default="planning/mvp/versions/v6.23/gantt/mvp_gantt_chart_commander_current.puml",
        help="Generated frozen PlantUML output path.",
    )
    args = parser.parse_args()

    template_path = Path(args.template)
    csv_path = Path(args.csv)
    out_path = Path(args.out)

    if not template_path.exists():
        raise SystemExit(f"Template not found: {template_path}")
    if not csv_path.exists():
        raise SystemExit(f"CSV not found: {csv_path}")

    generate_frozen_puml(template_path=template_path, csv_path=csv_path, out_path=out_path)
    print(f"OK: wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
