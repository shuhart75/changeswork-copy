#!/usr/bin/env python3
"""
Synchronize terminology across project documents.
Updates old entity names to new names based on entity mapping.
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
    r'.*_v3\.0\.',  # v3.0 files are historical
    r'CHANGELOG',
    r'review_.*',
    r'final_.*',
    r'summary.*',
    r'verification_.*',
    r'resource_conflicts.*',
    r'\.git/',
    r'\.claude/skills/',  # Don't modify the skill itself
]

def should_skip_file(filepath):
    """Check if file should be skipped."""
    filepath_str = str(filepath)
    for pattern in SKIP_PATTERNS:
        if re.search(pattern, filepath_str):
            return True
    return False

def update_file_terminology(filepath, dry_run=True):
    """Update terminology in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        return None, f"Error reading: {e}"

    content = original_content
    changes = []

    # Pattern 1: "Внедрение (Deployment)" in Initiative context -> "Инициатива (Initiative)"
    pattern1 = r'Внедрение\s*\(Deployment\)'
    if re.search(pattern1, content):
        # Check if it's in Initiative context
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if re.search(pattern1, line):
                # Simple heuristic: if line contains "агрегат" or "группировка", it's Initiative context
                if 'агрегат' in line.lower() or 'группировка' in line.lower() or 'архивирование' in line.lower():
                    new_line = re.sub(pattern1, 'Инициатива (Initiative)', line)
                    if new_line != line:
                        changes.append(f"  '{line.strip()[:60]}...' -> '{new_line.strip()[:60]}...'")
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)

    # Pattern 2: "Изменение (Change)" in Deployment context -> "Внедрение (Deployment)"
    pattern2 = r'Изменение\s*\(Change\)'
    if re.search(pattern2, content):
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if re.search(pattern2, line):
                # Simple heuristic: if line contains deployment-related terms
                if 'продуктовое' in line.lower() or 'откат' in line.lower() or 'deployed' in line.lower():
                    new_line = re.sub(pattern2, 'Внедрение (Deployment)', line)
                    if new_line != line:
                        changes.append(f"  '{line.strip()[:60]}...' -> '{new_line.strip()[:60]}...'")
                    new_lines.append(new_line)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        content = '\n'.join(new_lines)

    # Pattern 3: Standalone "Deployment" in Initiative context
    # This is more complex and requires careful context analysis

    if content == original_content:
        return None, None  # No changes

    if not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            return None, f"Error writing: {e}"

    return changes, None

def main():
    """Main function."""
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv

    project_root = Path.cwd()

    if dry_run:
        print("🔍 DRY RUN: Previewing changes (no files will be modified)\n")
    else:
        print("✏️  APPLYING CHANGES: Files will be modified\n")

    all_changes = defaultdict(list)
    scanned_count = 0
    skipped_count = 0

    # Process all .md, .html, and .puml files
    for ext in ['*.md', '*.html', '*.puml']:
        for filepath in project_root.rglob(ext):
            if should_skip_file(filepath):
                skipped_count += 1
                continue

            changes, error = update_file_terminology(filepath, dry_run)

            if error:
                print(f"⚠️  {filepath.relative_to(project_root)}: {error}")
                continue

            scanned_count += 1

            if changes:
                all_changes[filepath] = changes

    # Report results
    print(f"📊 Processed {scanned_count} files (skipped {skipped_count})\n")

    if not all_changes:
        print("✅ No changes needed - all terminology is up to date!")
        return 0

    print(f"📝 {'Would update' if dry_run else 'Updated'} {len(all_changes)} files:\n")

    for filepath, changes in sorted(all_changes.items()):
        rel_path = filepath.relative_to(project_root)
        print(f"\n📄 {rel_path}")
        print("─" * 80)
        for change in changes:
            print(change)

    if dry_run:
        print(f"\n💡 Run without --dry-run to apply these changes")
    else:
        print(f"\n✅ Successfully updated {len(all_changes)} files")

    return 0

if __name__ == '__main__':
    exit(main())
