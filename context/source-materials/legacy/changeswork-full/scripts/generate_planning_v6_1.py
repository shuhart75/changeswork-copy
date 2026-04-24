#!/usr/bin/env python3
"""
Generate aligned planning artifacts (v6.1) from:
- Source of truth for domain terms: spec/domain_model.md (v3.1)
- Source of truth for schedule/estimates: planning/mvp/gantt/mvp_gantt_chart_v6.puml

The generator:
- Creates planning/mvp/versions/v6.1/
- Copies and lightly rewrites the v6 Gantt (labels/terminology only, same codes/durations/deps)
- Copies tasks/*.md into versions/v6.1/tasks/ with:
  - estimate lines updated to match Gantt v6 durations (where task codes match)
  - terminology aligned to spec v3.1 (Initiative vs Deployment vs Change) via file-scoped rewrites
  - common field rename: deployment_id -> initiative_id where it represents the parent aggregate

This is intentionally conservative: it avoids deep content redesign and focuses on removing
contradictions between tasks, Gantt, and spec terminology.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_GANTT = ROOT / "planning/mvp/gantt/mvp_gantt_chart_v6.puml"
SRC_TASKS_DIR = ROOT / "planning/mvp/tasks"

OUT_DIR = ROOT / "planning/mvp/versions/v6.1"
OUT_GANTT_DIR = OUT_DIR / "gantt"
OUT_TASKS_DIR = OUT_DIR / "tasks"


@dataclass(frozen=True)
class TaskDef:
    code: str
    name: str
    resource: str
    duration_days: int


def _plural_days(n: int) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return "день"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return "дня"
    return "дней"


def parse_gantt_tasks(path: Path) -> dict[str, TaskDef]:
    text = path.read_text(encoding="utf-8")
    tasks: dict[str, TaskDef] = {}
    # Example:
    # [Backend процесс согласования] as [BE_AP1] on {B1} lasts 8 days
    # [Frontend страницы Пакеты] as [FE_PKG1] on {F2:50%} lasts 8 days
    pat = re.compile(
        r"^\[([^\]]+)\]\s+as\s+\[([^\]]+)\]\s+on\s+\{([^}]+)\}\s+lasts\s+(\d+)\s+days\s*$",
        re.MULTILINE,
    )
    for name, code, resource, dur in pat.findall(text):
        tasks[code] = TaskDef(code=code, name=name, resource=resource, duration_days=int(dur))
    return tasks


def _rewrite_estimates(md: str, gantt: dict[str, TaskDef]) -> str:
    """
    Update lines like:
    **Оценка:** 2 дня
    within a section that starts with:
    ## AN-D1: ...

    We map AN-D1 -> AN_D1 for gantt lookup.
    """
    lines = md.splitlines(keepends=False)
    out: list[str] = []

    current_code: str | None = None
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+([A-Z]+-[A-Z0-9]+)\s*:", line)
        if m:
            current_code = m.group(1)
            out.append(line)
            continue

        if current_code and "**Оценка:**" in line:
            gantt_code = current_code.replace("-", "_")
            if gantt_code in gantt:
                d = gantt[gantt_code].duration_days
                out.append(re.sub(r"\*\*Оценка:\*\*\s*.+$", f"**Оценка:** {d} {_plural_days(d)}", line))
                continue

        out.append(line)

    return "\n".join(out) + ("\n" if md.endswith("\n") else "")


def _bulk_replace(text: str, repls: list[tuple[str, str]]) -> str:
    for a, b in repls:
        text = text.replace(a, b)
    return text


def rewrite_task_doc(src_path: Path, md: str) -> tuple[str, str]:
    """
    Returns (new_relative_path, new_text)
    """
    name = src_path.name

    # Baseline replacements: parent FK rename (old planning used deployment_id as parent).
    # Keep it simple; if a particular doc still needs deployment_id as an entity id,
    # we will fix it manually after generation.
    md = md.replace("deployment_id", "initiative_id")

    # Light terminology alignment, file-scoped to avoid breaking semantics elsewhere.
    if name in {
        "mvp_tasks_deployments_page.md",
        "mvp_tasks_create_deployment_page.md",
        "mvp_tasks_deployment_detail_page.md",
    }:
        # These "Deployments" pages actually match Initiative (draft/active/deployed/archived).
        md = _bulk_replace(
            md,
            [
                ("\"Внедрения\"", "\"Инициативы\""),
                ("(Deployments", "(Initiatives"),
                ("Deployments", "Initiatives"),
                ("DEP-XXX", "INIT-XXX"),
                ("Название внедрения", "Название инициативы"),
                ("списка внедрений", "списка инициатив"),
                ("к списку внедрений", "к списку инициатив"),
                ("на странице списка внедрений", "на странице списка инициатив"),
                ("Кнопка \"Создать внедрение\"", "Кнопка \"Создать инициативу\""),
                ("\"Создать внедрение\"", "\"Создать инициативу\""),
                ("Deployment", "Initiative"),
                ("deployment", "initiative"),
                ("Внедрение (deployment)", "Инициатива (initiative)"),
                ("внедрение (deployment)", "инициатива (initiative)"),
                ("Список внедрений", "Список инициатив"),
                ("детальной страницы \"Внедрение\"", "детальной страницы \"Инициатива\""),
                ("детальной страницы Внедрения", "детальной страницы Инициативы"),
                ("Форма создания внедрения", "Форма создания инициативы"),
                ("Создание внедрения", "Создание инициативы"),
                ("создавать внедрения", "создавать инициативы"),
                ("создания внедрения", "создания инициативы"),
                ("внедрения своего продукта", "инициативы своего продукта"),
                ("все внедрения", "все инициативы"),
            ],
        )
        out_name = name
        out_name = out_name.replace("deployments", "initiatives")
        out_name = out_name.replace("deployment_detail", "initiative_detail")
        out_name = out_name.replace("create_deployment", "create_initiative")
        return out_name, md

    if name in {
        "mvp_tasks_changes_page.md",
        "mvp_tasks_change_form.md",
        "mvp_tasks_change_detail_page.md",
        "mvp_tasks_change_lifecycle.md",
    }:
        # "Changes" match spec v3.1 entity "Deployment" (product rollout).
        md = _bulk_replace(
            md,
            [
                ("\"Изменения\"", "\"Внедрения\""),
                ("(Changes", "(Deployments"),
                ("Changes", "Deployments"),
                ("CHG-XXX", "DEP-XXX"),
                ("Список изменений", "Список внедрений"),
                ("Change", "Deployment"),
                ("Изменение", "Внедрение"),
                ("изменение", "внедрение"),
                ("Изменениями", "Внедрениями"),
                ("Изменений", "Внедрений"),
                ("Изменения", "Внедрения"),
                ("статусов изменения", "статусов внедрения"),
                ("changes", "deployments"),
                ("change", "deployment"),
            ],
        )
        out_name = name
        out_name = out_name.replace("changes", "deployments")
        out_name = out_name.replace("change_", "deployment_")
        return out_name, md

    # Other docs: parent naming used "Внедрение (deployment)" to mean the aggregate;
    # per spec this is Initiative.
    md = _bulk_replace(
        md,
        [
            ("Внедрение (deployment)", "Инициатива (initiative)"),
            ("внедрение (deployment)", "инициатива (initiative)"),
            ("внедрения (deployment)", "инициативы (initiative)"),
            ("внедрению (deployment)", "инициативе (initiative)"),
        ],
    )

    return name, md


def rewrite_gantt(src: str) -> str:
    # Keep the schedule intact; adjust labels only to match spec terms.
    out = src
    out = out.replace("title План разработки MVP - Аналитика вперед (v6)", "title План разработки MVP - Аналитика вперед (v6.1, aligned to spec v3.1)")

    # D* tasks: Initiative pages.
    out = out.replace("[Аналитика внедрения]", "[Аналитика инициативы]")
    out = out.replace("[Аналитика создания внедрения]", "[Аналитика создания инициативы]")
    out = out.replace("[Backend списка внедрений]", "[Backend списка инициатив]")
    out = out.replace("[Backend деталки внедрения]", "[Backend деталки инициативы]")
    out = out.replace("[Backend создания внедрения]", "[Backend создания инициативы]")
    out = out.replace("[Frontend списка внедрений]", "[Frontend списка инициатив]")
    out = out.replace("[Frontend деталки внедрения]", "[Frontend деталки инициативы]")
    out = out.replace("[Frontend создания внедрения]", "[Frontend создания инициативы]")

    # C* tasks: Deployment (product rollout).
    out = out.replace("[Аналитика списка изменений]", "[Аналитика списка внедрений]")
    out = out.replace("[Backend списка изменений]", "[Backend списка внедрений]")
    out = out.replace("[Frontend списка изменений]", "[Frontend списка внедрений]")
    out = out.replace("[Аналитика деталки изменения]", "[Аналитика деталки внедрения]")
    out = out.replace("[Backend деталки изменения]", "[Backend деталки внедрения]")
    out = out.replace("[Frontend деталки изменения]", "[Frontend деталки внедрения]")
    out = out.replace("[Аналитика формы изменения]", "[Аналитика формы внедрения]")
    out = out.replace("[Backend формы изменения]", "[Backend формы внедрения]")
    out = out.replace("[Frontend формы изменения]", "[Frontend формы внедрения]")

    # Keep "Пакеты/Согласования" labels as-is; their detailed semantics are documented in tasks.
    return out


def main() -> int:
    if not SRC_GANTT.exists():
        raise SystemExit(f"Missing source gantt: {SRC_GANTT}")
    if not SRC_TASKS_DIR.exists():
        raise SystemExit(f"Missing source tasks dir: {SRC_TASKS_DIR}")

    gantt_tasks = parse_gantt_tasks(SRC_GANTT)

    # Prepare output dirs
    OUT_GANTT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TASKS_DIR.mkdir(parents=True, exist_ok=True)

    # Write Gantt
    gantt_src_text = SRC_GANTT.read_text(encoding="utf-8")
    gantt_out_text = rewrite_gantt(gantt_src_text)
    (OUT_GANTT_DIR / "mvp_gantt_chart_v6.1_aligned.puml").write_text(gantt_out_text, encoding="utf-8")

    # Copy+rewrite tasks
    for src_path in sorted(SRC_TASKS_DIR.glob("*.md")):
        md = src_path.read_text(encoding="utf-8")
        md = _rewrite_estimates(md, gantt_tasks)
        out_rel_name, md = rewrite_task_doc(src_path, md)
        (OUT_TASKS_DIR / out_rel_name).write_text(md, encoding="utf-8")

    # Minimal version README
    readme = """# MVP Planning v6.1 (Aligned)

**Base spec:** `spec/domain_model.md` (v3.1)
**Base schedule:** `planning/mvp/gantt/mvp_gantt_chart_v6.puml` (v6)

This version exists to remove contradictions between task docs and the v6 Gantt by:
- aligning terminology to the v3.1 domain model (Initiative / Simulation / Pilot / Deployment)
- syncing task estimates in markdown with Gantt v6 durations (task codes)

Notes:
- Task codes are preserved (AN-D1/BE-D1/FE-D1 etc). In this aligned version, the `D*` track refers to **Initiatives**.
- The `C*` track refers to **Deployments** (product rollouts), formerly called "Changes" in older planning materials.
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
