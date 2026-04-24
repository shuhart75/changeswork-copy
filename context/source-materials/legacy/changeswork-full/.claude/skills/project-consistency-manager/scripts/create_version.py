#!/usr/bin/env python3
"""
Create new version of a core document.
Copies the current version to a new versioned file.
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

# Core document patterns
CORE_DOCUMENTS = {
    'domain_model': {
        'pattern': 'domain_model_v*.md',
        'current': 'domain_model_v3.1.md',
        'template': 'domain_model_v{version}.md',
    },
    'data_model': {
        'pattern': 'changes_data_model_v*.puml',
        'current': 'changes_data_model_v3.1.puml',
        'template': 'changes_data_model_v{version}.puml',
    },
    'state_machine': {
        'pattern': 'changes_state_machine_v*.puml',
        'current': 'changes_state_machine_v3.1.puml',
        'template': 'changes_state_machine_v{version}.puml',
    },
    'claude': {
        'pattern': 'CLAUDE_v*.md',
        'current': 'CLAUDE_v3.1.md',
        'template': 'CLAUDE_v{version}.md',
    },
}

def create_version(document_name, new_version):
    """Create a new version of a core document."""
    if document_name not in CORE_DOCUMENTS:
        print(f"❌ Unknown document: {document_name}")
        print(f"   Available: {', '.join(CORE_DOCUMENTS.keys())}")
        return 1

    doc_info = CORE_DOCUMENTS[document_name]
    project_root = Path.cwd()

    current_file = project_root / doc_info['current']
    if not current_file.exists():
        print(f"❌ Current version not found: {current_file}")
        return 1

    new_filename = doc_info['template'].format(version=new_version)
    new_file = project_root / new_filename

    if new_file.exists():
        print(f"❌ Version already exists: {new_file}")
        return 1

    # Copy file
    try:
        shutil.copy2(current_file, new_file)
        print(f"✅ Created new version: {new_filename}")

        # Update version header if it's a markdown file
        if new_file.suffix == '.md':
            with open(new_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update version number in header
            content = content.replace(
                f"**Версия:** 3.1",
                f"**Версия:** {new_version}"
            )
            content = content.replace(
                f"**Дата:** 2026-03-10",
                f"**Дата:** {datetime.now().strftime('%Y-%m-%d')}"
            )

            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"   Updated version header to {new_version}")

        print(f"\n💡 Next steps:")
        print(f"   1. Edit {new_filename} with your changes")
        print(f"   2. Update CLAUDE.md to reference v{new_version}")
        print(f"   3. Run sync_terminology.py to update references")

        return 0

    except Exception as e:
        print(f"❌ Error creating version: {e}")
        return 1

def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: create_version.py <document-name> <new-version>")
        print(f"\nAvailable documents: {', '.join(CORE_DOCUMENTS.keys())}")
        print("\nExample: create_version.py domain_model 3.2")
        return 1

    document_name = sys.argv[1]
    new_version = sys.argv[2]

    return create_version(document_name, new_version)

if __name__ == '__main__':
    exit(main())
