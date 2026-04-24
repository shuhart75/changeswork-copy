#!/usr/bin/env python3
"""
Check terminology consistency across project documents.
Scans all files and reports where old terminology still exists.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Entity mapping: old term -> new term
TERMINOLOGY_MAP = {
    # Russian terms (context-sensitive)
    'Внедрение': 'Инициатива',  # When referring to top-level aggregate
    'Изменение': 'Внедрение',   # When referring to product deployment
    # English terms (context-sensitive)
    'Deployment': 'Initiative',  # When referring to top-level aggregate
    'Change': 'Deployment',      # When referring to product deployment
}

# Context patterns to help identify correct usage
INITIATIVE_CONTEXT = [
    'агрегат верхнего уровня',
    'группировка',
    'архивирование',
    'top-level aggregate',
    'grouping',
    'archiving',
]

DEPLOYMENT_CONTEXT = [
    'продуктовое внедрение',
    'откат',
    'deployed',
    'product deployment',
    'rollback',
]

# Files to skip
SKIP_PATTERNS = [
    r'.*\.backup$',
    r'.*\.bak$',
    r'.*_v3\.0\.',  # v3.0 files are historical
    r'CHANGELOG',
    r'review_.*',
    r'final_.*',
    r'summary.*',
    r'verification_.*',
    r'\.git/',
    r'\.claude/skills/',  # Don't scan the skill itself
]

def should_skip_file(filepath):
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath_str):
            return True
    return False

def scan_file(filepath):
    """Scan a file for old terminology."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return None, f"Error reading file: {e}"

    findings = []

    for line_num, line in enumerate(lines, 1):
        # Check for old Russian terms
        if 'Внедрение' in line or 'Deployment' in line:
            # Check context to determine if it's old terminology
            context = ' '.join(lines[max(0, line_num-2):min(len(lines), line_num+2)])

            # Check if it's in Initiative context (should be Инициатива/Initiative)
            for ctx_pattern in INITIATIVE_CONTEXT:
                if ctx_pattern in context.lower():
                    findings.append({
                        'line': line_num,
                        'text': line.strip(),
                        'issue': 'Old term "Внедрение/Deployment" in Initiative context',
                        'suggestion': 'Should be "Инициатива/Initiative"'
                    })
                    break

        if 'Изменение' in line or 'Change' in line:
            # Check if it's referring to the entity (should be Внедрение/Deployment)
            # Skip if it's just "изменение" as a common word
            if re.search(r'\bИзменение\b', line) or re.search(r'\bChange\b', line):
                # Check context
                context = ' '.join(lines[max(0, line_num-2):min(len(lines), line_num+2)])

                for ctx_pattern in DEPLOYMENT_CONTEXT:
                    if ctx_pattern in context.lower():
                        findings.append({
                            'line': line_num,
                            'text': line.strip(),
                            'issue': 'Old term "Изменение/Change" in Deployment context',
                            'suggestion': 'Should be "Внедрение/Deployment"'
                        })
                        break

    return findings, None

def main():
    """Main function."""
    project_root = Path.cwd()

    print("🔍 Scanning project for terminology consistency...\n")

    all_findings = defaultdict(list)
    scanned_count = 0
    skipped_count = 0

    # Scan all .md, .html, and .puml files
    for ext in ['*.md', '*.html', '*.puml']:
        for filepath in project_root.rglob(ext):
            if should_skip_file(filepath):
                skipped_count += 1
                continue

            findings, error = scan_file(filepath)

            if error:
                print(f"⚠️  {filepath.relative_to(project_root)}: {error}")
                continue

            scanned_count += 1

            if findings:
                all_findings[filepath] = findings

    # Report findings
    print(f"📊 Scanned {scanned_count} files (skipped {skipped_count})\n")

    if not all_findings:
        print("✅ No terminology issues found!")
        return 0

    print(f"⚠️  Found potential issues in {len(all_findings)} files:\n")

    for filepath, findings in sorted(all_findings.items()):
        rel_path = filepath.relative_to(project_root)
        print(f"\n📄 {rel_path}")
        print("─" * 80)

        for finding in findings:
            print(f"  Line {finding['line']}: {finding['issue']}")
            print(f"    {finding['text'][:100]}")
            print(f"    💡 {finding['suggestion']}")
            print()

    print(f"\n📈 Summary: {sum(len(f) for f in all_findings.values())} potential issues found")

    return 1

if __name__ == '__main__':
    exit(main())
