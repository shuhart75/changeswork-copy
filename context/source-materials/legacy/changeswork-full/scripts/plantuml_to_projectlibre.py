#!/usr/bin/env python3
"""
Convert PlantUML Gantt chart to ProjectLibre format (.pod XML)
"""

import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import sys

class Task:
    def __init__(self, name, duration, resource=None, color=None):
        self.id = None
        self.name = name
        self.duration = duration  # in days
        self.resource = resource
        self.color = color
        self.predecessors = []  # list of (task_id, type)
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
                self.parse_task(line, lines, -1)

        # Parse dependencies and colors in second pass
        self.parse_dependencies(lines)

        # Assign IDs
        for i, task in enumerate(self.tasks, 1):
            task.id = i

        return self

    def parse_task(self, line, all_lines, line_idx):
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

def create_projectlibre_xml(parser: PlantUMLParser) -> str:
    """Generate ProjectLibre XML format (MSPDI)"""

    # Register namespace
    ns = 'http://schemas.microsoft.com/project'
    ET.register_namespace('', ns)

    root = ET.Element('{%s}Project' % ns, {
        'xmlns': ns
    })

    # Properties
    properties = ET.SubElement(root, 'properties')

    # Phases (not used)
    phases = ET.SubElement(root, 'phases')

    # Calendars
    calendars = ET.SubElement(root, 'calendars')
    day_types = ET.SubElement(calendars, 'day-types')

    # Standard calendar
    calendar = ET.SubElement(calendars, 'calendar', {
        'id': '1',
        'name': 'Default'
    })

    # Tasks
    tasks_elem = ET.SubElement(root, 'tasks')

    for task in parser.tasks:
        task_elem = ET.SubElement(tasks_elem, 'task', {
            'id': str(task.id),
            'name': task.name,
            'note': '',
            'work': str(task.duration * 28800),  # 8 hours per day in seconds
            'duration': str(task.duration * 86400),  # in seconds
            'start': '0',
            'end': '0',
            'work-start': '0',
            'percent-complete': '0',
            'priority': '0',
            'type': 'normal',
            'scheduling': 'fixed-work'
        })

        # Add predecessors
        if task.predecessors:
            predecessors_elem = ET.SubElement(task_elem, 'predecessors')
            for pred_alias in task.predecessors:
                if pred_alias in parser.task_by_alias:
                    pred_task = parser.task_by_alias[pred_alias]
                    pred_elem = ET.SubElement(predecessors_elem, 'predecessor', {
                        'predecessor-id': str(pred_task.id),
                        'type': 'FS',  # Finish-to-Start
                        'lag': '0'
                    })

    # Resources
    resources_elem = ET.SubElement(root, 'resources')
    resource_names = set(t.resource for t in parser.tasks if t.resource)

    for i, res_name in enumerate(sorted(resource_names), 1):
        resource = ET.SubElement(resources_elem, 'resource', {
            'id': str(i),
            'name': res_name,
            'short-name': '',
            'type': '1',
            'units': '0',
            'email': '',
            'phone': '',
            'standard-rate': '0',
            'overtime-rate': '0',
            'calendar': '1'
        })

    # Allocations
    allocations_elem = ET.SubElement(root, 'allocations')

    alloc_id = 1
    resource_map = {name: i+1 for i, name in enumerate(sorted(resource_names))}

    for task in parser.tasks:
        if task.resource and task.resource in resource_map:
            allocation = ET.SubElement(allocations_elem, 'allocation', {
                'task-id': str(task.id),
                'resource-id': str(resource_map[task.resource]),
                'units': '100'
            })
            alloc_id += 1

    # Pretty print
    indent_xml(root)

    return '<?xml version="1.0"?>\n' + ET.tostring(root, encoding='unicode')

def indent_xml(elem, level=0):
    """Add indentation to XML for readability"""
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def main():
    if len(sys.argv) < 2:
        print("Usage: plantuml_to_projectlibre.py <input.puml> [output.pod]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.puml', '.pod')

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    parser = PlantUMLParser(content)
    parser.parse()

    xml_content = create_projectlibre_xml(parser)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    print(f"Converted {len(parser.tasks)} tasks")
    print(f"Output: {output_file}")

if __name__ == '__main__':
    main()
