#!/usr/bin/env python3
"""
Convert PlantUML Gantt chart to ProjectLibre CSV format
"""

import re
import csv
from datetime import datetime
from typing import Dict, List
import sys

class Task:
    def __init__(self, name, duration, resource=None, color=None):
        self.id = None
        self.name = name
        self.duration = duration  # in days
        self.resource = resource
        self.color = color
        self.predecessors = []  # list of task aliases
        self.alias = None

class PlantUMLParser:
    def __init__(self, content):
        self.content = content
        self.tasks = []
        self.task_by_alias = {}
        self.project_start = None
        self.closed_days = []
        self.title = ""

    def parse(self):
        lines = self.content.split('\n')

        for line in lines:
            line = line.strip()

            # Parse title
            if line.startswith('title '):
                self.title = line[6:].strip()

            # Parse project start
            if line.startswith('Project starts'):
                match = re.search(r'(\d+)(?:st|nd|rd|th) of (\w+) (\d+)', line)
                if match:
                    day, month, year = match.groups()
                    month_map = {
                        'january': 1, 'february': 2, 'march': 3, 'april': 4,
                        'may': 5, 'june': 6, 'july': 7, 'august': 8,
                        'september': 9, 'october': 10, 'november': 11, 'december': 12
                    }
                    self.project_start = datetime(int(year), month_map[month.lower()], int(day))

            # Parse closed days
            if 'is closed' in line:
                match = re.search(r'(\d{4})/(\d{2})/(\d{2})', line)
                if match:
                    year, month, day = match.groups()
                    self.closed_days.append(datetime(int(year), int(month), int(day)))

            # Parse tasks
            if line.startswith('[') and '] as [' in line:
                self.parse_task(line)

        # Parse dependencies and colors in second pass
        self.parse_dependencies(lines)

        # Assign IDs
        for i, task in enumerate(self.tasks, 1):
            task.id = i

        return self

    def parse_task(self, line):
        # [Task Name] as [ALIAS] on {RESOURCE} lasts N days
        match = re.match(r'\[([^\]]+)\]\s+as\s+\[([^\]]+)\](?:\s+on\s+\{([^}]+)\})?\s+lasts\s+(\d+)\s+days?', line)
        if not match:
            return

        name, alias, resource, duration = match.groups()
        task = Task(name, int(duration), resource)
        task.alias = alias

        self.tasks.append(task)
        self.task_by_alias[alias] = task

    def parse_dependencies(self, all_lines):
        """Parse dependencies in a second pass after all tasks are created"""
        for line in all_lines:
            line = line.strip()

            # Look for color
            if 'is colored in' in line:
                match = re.match(r'\[([^\]]+)\]\s+is colored in (\w+)', line)
                if match:
                    alias, color = match.groups()
                    if alias in self.task_by_alias:
                        self.task_by_alias[alias].color = color

            # Look for dependencies: [ALIAS] starts at [OTHER_ALIAS]'s end
            if 'starts at' in line and "'s end" in line:
                match = re.match(r'\[([^\]]+)\]\s+starts at \[([^\]]+)\]\'s end', line)
                if match:
                    task_alias, pred_alias = match.groups()
                    if task_alias in self.task_by_alias and pred_alias in self.task_by_alias:
                        self.task_by_alias[task_alias].predecessors.append(pred_alias)

def create_projectlibre_csv(parser: PlantUMLParser, output_file: str):
    """Generate ProjectLibre CSV format"""

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Header row
        writer.writerow([
            'ID',
            'Name',
            'Duration',
            'Start',
            'Finish',
            'Predecessors',
            'Resource Names',
            'Notes'
        ])

        # Write tasks
        for task in parser.tasks:
            # Build predecessors string
            pred_str = ''
            if task.predecessors:
                pred_ids = []
                for pred_alias in task.predecessors:
                    if pred_alias in parser.task_by_alias:
                        pred_task = parser.task_by_alias[pred_alias]
                        pred_ids.append(str(pred_task.id))
                pred_str = ';'.join(pred_ids)

            # Duration in days
            duration_str = f"{task.duration}d"

            writer.writerow([
                task.id,
                task.name,
                duration_str,
                '',  # Start - will be calculated
                '',  # Finish - will be calculated
                pred_str,
                task.resource or '',
                task.color or ''
            ])

def main():
    if len(sys.argv) < 2:
        print("Usage: plantuml_to_projectlibre_csv.py <input.puml> [output.csv]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.puml', '.csv')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = PlantUMLParser(content)
    parser.parse()

    create_projectlibre_csv(parser, output_file)

    print(f"Converted {len(parser.tasks)} tasks")
    print(f"Output: {output_file}")
    print(f"\nTo import in ProjectLibre:")
    print(f"1. Open ProjectLibre")
    print(f"2. File -> Import -> CSV")
    print(f"3. Select {output_file}")

if __name__ == '__main__':
    main()
