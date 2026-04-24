# Core Documents

Documents that require versioning when significant changes are made.

## Versioning Strategy

**Create new version when:**
- Adding or removing entities from the domain model
- Changing entity relationships in the data model
- Adding or removing states in state machines
- Major UI restructuring in prototypes
- Significant architectural changes in CLAUDE.md

**Update in place when:**
- Fixing typos or formatting
- Clarifying existing descriptions
- Adding examples without changing structure
- Minor UI tweaks

## Core Documents List

### 1. Domain Model
- **File pattern:** `domain_model_v*.md`
- **Current version:** v3.1
- **Description:** Complete domain model specification with bounded contexts, aggregates, business rules
- **Versioning trigger:** Entity changes, relationship changes, new business rules

### 2. Data Model
- **File pattern:** `changes_data_model_v*.puml`
- **Current version:** v3.1
- **Description:** PlantUML entity-relationship diagram
- **Versioning trigger:** Table changes, relationship changes, new entities

### 3. State Machine
- **File pattern:** `changes_state_machine_v*.puml`
- **Current version:** v3.1
- **Description:** PlantUML state diagrams for all entities
- **Versioning trigger:** New states, new transitions, lifecycle changes

### 4. CLAUDE.md
- **File pattern:** `CLAUDE_v*.md` (or `CLAUDE.md` for current)
- **Current version:** v3.1 (as CLAUDE_v3.1.md)
- **Description:** Project instructions for Claude Code AI assistant
- **Versioning trigger:** Architectural changes, new business rules, role changes

### 5. UI Prototype
- **File pattern:** `risk_strategy_ui_v*_table.html` or `risk_strategy_ui_mvp.html`
- **Current version:** v3 (table), mvp (latest)
- **Description:** Interactive React/Material-UI prototype
- **Versioning trigger:** Major UI restructuring, new views, significant UX changes

## Supporting Documents

These documents should be updated in place, not versioned:

- MVP scope and stories (`mvp_scope_*.md`, `mvp_stories_*.md`)
- MVP tasks (`mvp_tasks_*.md`)
- Presentations (`presentation_*.md`)
- FAQ and glossary (`faq_*.md`, `glossary.md`)
- Executive summaries (`executive_summary.md`)
- Use cases (`use_cases.md`)
- README files (`README_*.md`)
- Timeline and planning (`mvp_timeline_*.md`, `mvp_development_plan*.md`)

## Version Numbering

- **Major version (X.0):** Significant architectural changes, entity restructuring
- **Minor version (X.Y):** Entity renaming, new entities, relationship changes
- **No version number:** In-place updates for supporting documents

## Current Version Status

| Document | Current Version | Last Updated | Status |
|----------|----------------|--------------|--------|
| domain_model | v3.1 | 2026-03-10 | ✅ Current |
| changes_data_model | v3.1 | 2026-03-10 | ✅ Current |
| changes_state_machine | v3.1 | 2026-03-10 | ✅ Current |
| CLAUDE.md | v3.1 | 2026-03-10 | ✅ Current |
| risk_strategy_ui | mvp | 2026-03-06 | ⚠️ Needs terminology update |
