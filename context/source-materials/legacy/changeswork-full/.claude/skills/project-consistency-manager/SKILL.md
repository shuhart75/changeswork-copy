---
name: project-consistency-manager
description: Manage consistency across interconnected project documents with terminology synchronization and versioning. Use when the user asks to: (1) Check if terminology changes are reflected everywhere, (2) Synchronize or sync all documents, (3) Find inconsistencies between domain model and data model, (4) Create new versions of core documents after significant changes, (5) Verify that entity renaming is complete across all files.
---

# Project Consistency Manager

Manage consistency across large projects with interconnected documents, ensuring terminology synchronization and proper versioning of critical artifacts.

## Core Capabilities

1. **Terminology Synchronization** - Find and update entity names across all project documents
2. **Consistency Validation** - Check that changes in one document are reflected in dependent documents
3. **Version Management** - Create new versions of core documents when significant changes occur
4. **Dependency Tracking** - Understand which documents depend on each other

## Quick Start

### Check Terminology Consistency

When the user asks to check if renaming is reflected everywhere:

```bash
python3 scripts/check_terminology.py
```

This scans all documents and reports where old terminology still exists.

### Synchronize Terminology

When the user asks to sync all documents or synchronize everything:

```bash
python3 scripts/sync_terminology.py --dry-run  # Preview changes
python3 scripts/sync_terminology.py            # Apply changes
```

This updates terminology across all documents based on the entity mapping in `references/entity_mapping.md`.

### Interactive Synchronization

When the user wants to review and approve each change:

```bash
python3 scripts/interactive_sync.py
```

This shows each issue one by one and asks for confirmation before applying changes.

### Create New Version

When significant changes are made to core documents:

```bash
python3 scripts/create_version.py <document-name> <new-version>
```

Example: `python3 scripts/create_version.py domain_model 3.2`

### Check Overall Consistency

When the user asks to verify consistency:

```bash
python3 scripts/check_consistency.py
```

This validates that domain model, data model, state machines, and UI are aligned.

## Entity Mapping

See `references/entity_mapping.md` for the complete mapping of entity names and their translations.

## Core Documents

See `references/core_documents.md` for the list of documents that require versioning.

## Dependency Graph

See `references/dependency_graph.md` for understanding which documents depend on each other.

## Workflow

1. **Before making changes**: Run `check_consistency.py` to establish baseline
2. **Make changes**: Edit core documents (domain model, data model, etc.)
3. **Check impact**: Run `check_terminology.py` to see what needs updating
4. **Synchronize**: Run `sync_terminology.py` to propagate changes
5. **Version**: Run `create_version.py` for core documents if changes are significant
6. **Validate**: Run `check_consistency.py` to confirm everything is aligned

## Important Notes

- Always use `--dry-run` first to preview changes before applying
- Core documents (domain_model, data_model, state_machine, CLAUDE.md, UI prototypes) should be versioned
- Supporting documents (MVP tasks, presentations, etc.) should be updated in place
- The scripts preserve file encoding and line endings
