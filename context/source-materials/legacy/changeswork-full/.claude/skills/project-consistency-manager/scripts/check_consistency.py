#!/usr/bin/env python3
"""
Check overall consistency between core documents.
Validates that domain model, data model, state machines, and UI are aligned.
"""

import re
from pathlib import Path
from collections import defaultdict

def extract_entities_from_domain_model(filepath):
    """Extract entity names from domain model."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entities = set()

    # Look for entity definitions (e.g., "**Инициатива (Initiative)**")
    pattern = r'\*\*([А-Яа-я]+)\s*\(([A-Za-z]+)\)\*\*'
    for match in re.finditer(pattern, content):
        russian_name = match.group(1)
        english_name = match.group(2)
        entities.add((russian_name, english_name))

    return entities

def extract_entities_from_data_model(filepath):
    """Extract table names from data model."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    tables = set()

    # Look for PlantUML entity definitions
    pattern = r'entity\s+"([^"]+)"'
    for match in re.finditer(pattern, content):
        table_name = match.group(1)
        tables.add(table_name)

    return tables

def extract_entities_from_state_machine(filepath):
    """Extract state machine entity names."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entities = set()

    # Look for state machine titles
    pattern = r'title\s+([А-Яа-я]+)\s+\(([A-Za-z]+)\)'
    for match in re.finditer(pattern, content):
        russian_name = match.group(1)
        english_name = match.group(2)
        entities.add((russian_name, english_name))

    return entities

def check_domain_data_alignment(domain_entities, data_tables):
    """Check if domain entities have corresponding tables."""
    issues = []

    # Expected table mappings
    expected_tables = {
        'Initiative': 'initiative',
        'Simulation': 'simulation',
        'Pilot': 'pilot',
        'Deployment': 'deployment',
        'Scorecard': 'scorecard',
        'Package': 'package',
    }

    for russian, english in domain_entities:
        if english in expected_tables:
            expected_table = expected_tables[english]
            if expected_table not in data_tables:
                issues.append(f"❌ Entity '{english}' in domain model but no '{expected_table}' table in data model")

    return issues

def check_domain_state_alignment(domain_entities, state_entities):
    """Check if domain entities have state machines."""
    issues = []

    # Entities that should have state machines
    stateful_entities = {'Initiative', 'Simulation', 'Pilot', 'Deployment'}

    domain_english = {e[1] for e in domain_entities}
    state_english = {e[1] for e in state_entities}

    for entity in stateful_entities:
        if entity in domain_english and entity not in state_english:
            issues.append(f"❌ Entity '{entity}' in domain model but no state machine found")

    return issues

def main():
    """Main function."""
    project_root = Path.cwd()

    print("🔍 Checking consistency between core documents...\n")

    # Load documents
    domain_model = project_root / 'domain_model_v3.1.md'
    data_model = project_root / 'changes_data_model_v3.1.puml'
    state_machine = project_root / 'changes_state_machine_v3.1.puml'

    if not domain_model.exists():
        print(f"❌ Domain model not found: {domain_model}")
        return 1

    if not data_model.exists():
        print(f"❌ Data model not found: {data_model}")
        return 1

    if not state_machine.exists():
        print(f"❌ State machine not found: {state_machine}")
        return 1

    # Extract entities
    print("📖 Reading domain model...")
    domain_entities = extract_entities_from_domain_model(domain_model)
    print(f"   Found {len(domain_entities)} entities")

    print("📖 Reading data model...")
    data_tables = extract_entities_from_data_model(data_model)
    print(f"   Found {len(data_tables)} tables")

    print("📖 Reading state machines...")
    state_entities = extract_entities_from_state_machine(state_machine)
    print(f"   Found {len(state_entities)} state machines\n")

    # Check alignments
    all_issues = []

    print("🔍 Checking domain model ↔ data model alignment...")
    issues = check_domain_data_alignment(domain_entities, data_tables)
    all_issues.extend(issues)
    if not issues:
        print("   ✅ Aligned")
    else:
        for issue in issues:
            print(f"   {issue}")

    print("\n🔍 Checking domain model ↔ state machine alignment...")
    issues = check_domain_state_alignment(domain_entities, state_entities)
    all_issues.extend(issues)
    if not issues:
        print("   ✅ Aligned")
    else:
        for issue in issues:
            print(f"   {issue}")

    # Summary
    print(f"\n{'='*80}")
    if not all_issues:
        print("✅ All core documents are consistent!")
        return 0
    else:
        print(f"⚠️  Found {len(all_issues)} consistency issues")
        print("\n💡 Review the issues above and update the relevant documents")
        return 1

if __name__ == '__main__':
    exit(main())
