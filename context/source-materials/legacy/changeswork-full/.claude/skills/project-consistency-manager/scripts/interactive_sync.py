#!/usr/bin/env python3
"""
Interactive terminology synchronization.
Shows each issue and asks for user confirmation before applying changes.
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Files to skip
SKIP_PATTERNS = [
    r'.*\.backup$',
    r'.*\.bak$',
    r'.*_v3\.0\.',
    r'CHANGELOG',
    r'review_.*',
    r'final_.*',
    r'summary.*',
    r'verification_.*',
    r'resource_conflicts.*',
    r'\.git/',
    r'\.claude/skills/',
]

# Context patterns
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

def should_skip_file(filepath):
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath_str):
            return True
    return False

def get_file_issues(filepath):
    """Get all terminology issues in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception as e:
        return None, f"Error reading: {e}"

    issues = []

    for line_num, line in enumerate(lines, 1):
        # Check for "Внедрение (Deployment)" in Initiative context
        if re.search(r'Внедрение\s*\(Deployment\)', line):
            context_lines = lines[max(0, line_num-2):min(len(lines), line_num+2)]
            context = ' '.join(context_lines)

            for ctx_pattern in INITIATIVE_CONTEXT:
                if ctx_pattern in context.lower():
                    issues.append({
                        'line_num': line_num,
                        'line': line,
                        'old': 'Внедрение (Deployment)',
                        'new': 'Инициатива (Initiative)',
                        'reason': 'Initiative context'
                    })
                    break

        # Check for standalone "Deployment" in Initiative context
        if re.search(r'\bDeployment\b', line) and 'Deployment' in line:
            context_lines = lines[max(0, line_num-2):min(len(lines), line_num+2)]
            context = ' '.join(context_lines)

            # Skip if it's "Deployment (Внедрение)" - that's correct in v3.1
            if 'Deployment (Внедрение)' in line or 'Deployment (внедрение)' in line:
                continue

            for ctx_pattern in INITIATIVE_CONTEXT:
                if ctx_pattern in context.lower():
                    # This is tricky - need to replace "Deployment" with "Initiative"
                    # but only in Initiative context
                    issues.append({
                        'line_num': line_num,
                        'line': line,
                        'old': 'Deployment',
                        'new': 'Initiative',
                        'reason': 'Initiative context (standalone)'
                    })
                    break

        # Check for "Изменение (Change)" in Deployment context
        if re.search(r'Изменение\s*\(Change\)', line):
            context_lines = lines[max(0, line_num-2):min(len(lines), line_num+2)]
            context = ' '.join(context_lines)

            for ctx_pattern in DEPLOYMENT_CONTEXT:
                if ctx_pattern in context.lower():
                    issues.append({
                        'line_num': line_num,
                        'line': line,
                        'old': 'Изменение (Change)',
                        'new': 'Внедрение (Deployment)',
                        'reason': 'Deployment context'
                    })
                    break

        # Check for standalone "Change" in Deployment context
        if re.search(r'\bChange\b', line) and 'Change' in line:
            context_lines = lines[max(0, line_num-2):min(len(lines), line_num+2)]
            context = ' '.join(context_lines)

            # Skip if it's "Change (Изменение)" - that's old terminology
            if 'Change (Изменение)' in line or 'Change (изменение)' in line:
                continue

            for ctx_pattern in DEPLOYMENT_CONTEXT:
                if ctx_pattern in context.lower():
                    issues.append({
                        'line_num': line_num,
                        'line': line,
                        'old': 'Change',
                        'new': 'Deployment',
                        'reason': 'Deployment context (standalone)'
                    })
                    break

    return issues, None

def apply_change(filepath, line_num, old_text, new_text):
    """Apply a single change to a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if line_num > len(lines):
            return False, "Line number out of range"

        original_line = lines[line_num - 1]
        if old_text not in original_line:
            return False, f"Old text not found in line"

        new_line = original_line.replace(old_text, new_text, 1)
        lines[line_num - 1] = new_line

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return True, None
    except Exception as e:
        return False, str(e)

def main():
    """Main interactive function."""
    project_root = Path.cwd()

    print("🔄 Interactive Terminology Synchronization")
    print("=" * 80)
    print()

    # Collect all issues
    print("📊 Scanning files...")
    all_issues = {}

    for ext in ['*.md', '*.html', '*.puml']:
        for filepath in project_root.rglob(ext):
            if should_skip_file(filepath):
                continue

            issues, error = get_file_issues(filepath)
            if error:
                continue

            if issues:
                all_issues[filepath] = issues

    if not all_issues:
        print("✅ No issues found!")
        return 0

    total_issues = sum(len(issues) for issues in all_issues.values())
    print(f"Found {total_issues} issues in {len(all_issues)} files\n")

    # Interactive review
    applied = 0
    skipped = 0

    for filepath, issues in sorted(all_issues.items()):
        rel_path = filepath.relative_to(project_root)
        print(f"\n📄 {rel_path}")
        print("─" * 80)

        for i, issue in enumerate(issues, 1):
            print(f"\nIssue {i}/{len(issues)}:")
            print(f"  Line {issue['line_num']}: {issue['reason']}")
            print(f"  Current: {issue['line'][:100]}")
            print(f"  Change:  '{issue['old']}' → '{issue['new']}'")

            while True:
                response = input("\n  Apply? [y]es / [n]o / [q]uit: ").lower().strip()

                if response == 'q':
                    print(f"\n📊 Summary: Applied {applied}, Skipped {skipped}")
                    return 0

                if response == 'y':
                    success, error = apply_change(filepath, issue['line_num'], issue['old'], issue['new'])
                    if success:
                        print("  ✅ Applied")
                        applied += 1
                    else:
                        print(f"  ❌ Error: {error}")
                        skipped += 1
                    break

                if response == 'n':
                    print("  ⏭️  Skipped")
                    skipped += 1
                    break

                print("  Invalid input. Please enter y, n, or q.")

    print(f"\n{'='*80}")
    print(f"📊 Summary: Applied {applied}, Skipped {skipped}")
    print("✅ Interactive sync complete!")

    return 0

if __name__ == '__main__':
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        exit(1)
