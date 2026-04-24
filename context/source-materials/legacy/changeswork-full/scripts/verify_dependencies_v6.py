#!/usr/bin/env python3
import re

import sys
from pathlib import Path


def _usage() -> str:
    return (
        "Usage:\n"
        "  python3 verify_dependencies_v6.py [path/to/gantt.puml]\n\n"
        "Default file name (if omitted): mvp_gantt_chart_v6.puml (in current working directory)\n"
    )


gantt_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mvp_gantt_chart_v6.puml")
if not gantt_path.exists():
    raise SystemExit(f"File not found: {gantt_path}\n\n{_usage()}")

lines = gantt_path.read_text(encoding="utf-8").splitlines(keepends=False)

tasks = {}

for line in lines:
    # Match task definition
    match = re.match(r'\[([^\]]+)\] as \[([^\]]+)\] on \{([A-Z0-9]+)(?::\d+%)?\} lasts (\d+) days', line)
    if match:
        name, code, resource, duration = match.groups()
        tasks[code] = {
            'name': name,
            'resource': resource,
            'duration': int(duration),
            'starts_at': []
        }
    
    # Match dependency
    dep_match = re.match(r"\[([^\]]+)\] starts at \[([^\]]+)\]", line)
    if dep_match:
        code, dep = dep_match.groups()
        if code in tasks:
            tasks[code]['starts_at'].append(dep)

# Check analytics dependencies
print("=== Analytics tasks that should have backend dependencies ===")
analytics_tasks = {k: v for k, v in tasks.items() if k.startswith('AN_')}
backend_tasks = {k: v for k, v in tasks.items() if k.startswith('BE_')}

for be_code, be_task in backend_tasks.items():
    deps = be_task["starts_at"]
    if any(d.startswith("AN_") for d in deps):
        print(f"✓ {be_code} depends on analytics: {', '.join(sorted([d for d in deps if d.startswith('AN_')]))}")
    elif any(not d.startswith("M") for d in deps):
        other = [d for d in deps if not d.startswith("M")]
        if other:
            print(f"⚠ {be_code} depends on {', '.join(other)} (not analytics)")

print("\n=== Frontend tasks that should have backend dependencies ===")
frontend_tasks = {k: v for k, v in tasks.items() if k.startswith('FE_')}

for fe_code, fe_task in frontend_tasks.items():
    deps = fe_task["starts_at"]
    if any(d.startswith("BE_") for d in deps):
        print(f"✓ {fe_code} depends on backend: {', '.join(sorted([d for d in deps if d.startswith('BE_')]))}")
    elif deps:
        print(f"⚠ {fe_code} depends on {', '.join(deps)} (not backend)")

print("\n=== Resource sequences (checking for gaps) ===")
for resource in ['A1', 'A2', 'B1', 'B2', 'B3', 'F1', 'F2']:
    res_tasks = [(k, v) for k, v in tasks.items() if v['resource'] == resource]
    print(f"\n{resource}: {len(res_tasks)} tasks")
    for code, task in res_tasks[:5]:
        dep = ", ".join(task["starts_at"]) if task["starts_at"] else "START"
        print(f"  {code} ({task['duration']}d) <- {dep}")
