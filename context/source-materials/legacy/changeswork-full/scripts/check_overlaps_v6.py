#!/usr/bin/env python3
import re
from datetime import datetime, timedelta

import sys
from pathlib import Path


def _usage() -> str:
    return (
        "Usage:\n"
        "  python3 check_overlaps_v6.py [path/to/gantt.puml]\n\n"
        "Default file name (if omitted): mvp_gantt_chart_v6.puml (in current working directory)\n"
    )


gantt_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("mvp_gantt_chart_v6.puml")
if not gantt_path.exists():
    raise SystemExit(f"File not found: {gantt_path}\n\n{_usage()}")

content = gantt_path.read_text(encoding="utf-8")

# Extract project start date
start_match = re.search(r'Project starts the (\d+)th of (\w+) (\d+)', content)
if start_match:
    day, month, year = start_match.groups()
    month_map = {'march': 3, 'april': 4, 'may': 5, 'june': 6}
    project_start = datetime(int(year), month_map[month.lower()], int(day))
    print(f"Project starts: {project_start.strftime('%Y-%m-%d')}")

# Parse tasks
lines = content.split('\n')
tasks = {}

for line in lines:
    # Match task definition
    # Resource can be like {F2} or {F2:50%}
    match = re.match(r'\[([^\]]+)\] as \[([^\]]+)\] on \{([A-Z0-9]+)(?::\d+%)?\} lasts (\d+) days', line)
    if match:
        name, code, resource, duration = match.groups()
        tasks[code] = {
            'name': name,
            'resource': resource,
            'duration': int(duration),
            'dependencies': []
        }
    
    # Match dependencies
    dep_match = re.match(r"\[([^\]]+)\] starts at \[([^\]]+)\]", line.strip())
    if dep_match:
        code, dep = dep_match.groups()
        if code in tasks:
            tasks[code]['dependencies'].append(dep)

# Calculate start times (simplified - ignoring weekends/holidays)
def calc_start_time(task_code, tasks, memo={}):
    if task_code in memo:
        return memo[task_code]
    
    if task_code == 'M1' or task_code == 'M2':
        # Milestone - find max end time of dependencies
        return 0
    
    if task_code not in tasks:
        return 0  # Start of project or milestone
    
    task = tasks[task_code]
    if not task['dependencies']:
        start = 0
    else:
        # Start after all dependencies end
        max_end = 0
        for dep in task['dependencies']:
            dep_start = calc_start_time(dep, tasks, memo)
            if dep in tasks:
                dep_end = dep_start + tasks[dep]['duration']
            else:
                dep_end = dep_start
            max_end = max(max_end, dep_end)
        start = max_end
    
    memo[task_code] = start
    return start

# Calculate all start times
start_times = {}
for code in tasks:
    start_times[code] = calc_start_time(code, tasks)

# Check for overlaps by resource
print("\n=== Checking for overlaps by resource ===")
resources = {}
for code, task in tasks.items():
    res = task['resource']
    if res not in resources:
        resources[res] = []
    start = start_times[code]
    end = start + task['duration']
    resources[res].append((start, end, code, task['name']))

overlaps_found = False
for res, task_list in sorted(resources.items()):
    task_list.sort()  # Sort by start time
    print(f"\n{res}: {len(task_list)} tasks")
    
    for i in range(len(task_list)):
        start1, end1, code1, name1 = task_list[i]
        
        # Check if this task overlaps with any subsequent task
        for j in range(i+1, len(task_list)):
            start2, end2, code2, name2 = task_list[j]
            
            # Check for overlap
            if start2 < end1:
                print(f"  ⚠️  OVERLAP: {code1} (days {start1}-{end1}) overlaps with {code2} (days {start2}-{end2})")
                overlaps_found = True
            else:
                break  # No more overlaps possible for this task

if not overlaps_found:
    print("\n✅ No overlaps found! All resources are properly scheduled.")

# Print resource utilization
print("\n=== Resource utilization ===")
for res, task_list in sorted(resources.items()):
    total_days = sum(t[1] - t[0] for t in task_list)
    first_start = min(t[0] for t in task_list)
    last_end = max(t[1] for t in task_list)
    span = last_end - first_start
    utilization = (total_days / span * 100) if span > 0 else 0
    print(f"{res}: {total_days} days work over {span} days span = {utilization:.1f}% utilization")
