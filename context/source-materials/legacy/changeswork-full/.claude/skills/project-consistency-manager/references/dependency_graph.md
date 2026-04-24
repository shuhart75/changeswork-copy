# Dependency Graph

Understanding which documents depend on each other and how changes propagate.

## Dependency Hierarchy

```
domain_model_v3.1.md (SOURCE OF TRUTH)
    ├── changes_data_model_v3.1.puml (implements domain model as database schema)
    ├── changes_state_machine_v3.1.puml (implements entity lifecycles)
    ├── CLAUDE_v3.1.md (summarizes architecture and business rules)
    └── risk_strategy_ui_*.html (implements UI based on domain model)
        └── mvp_stories_*.md (user stories based on UI)
            └── mvp_tasks_*.md (implementation tasks)
```

## Propagation Rules

### When domain_model changes:

1. **changes_data_model.puml** - Update entity names, relationships, tables
2. **changes_state_machine.puml** - Update state diagrams if lifecycles changed
3. **CLAUDE.md** - Update architecture summary, business rules, role matrix
4. **risk_strategy_ui.html** - Update entity names in UI, forms, tables
5. **mvp_stories_*.md** - Update user stories if functionality changed
6. **mvp_tasks_*.md** - Update task descriptions if implementation changed
7. **glossary.md** - Update terminology definitions
8. **All other .md files** - Update entity references

### When changes_data_model changes:

1. **domain_model.md** - Verify alignment (data model should follow domain model)
2. **mvp_stories_backend.md** - Update API and database stories
3. **mvp_tasks_*_backend.md** - Update backend implementation tasks

### When changes_state_machine changes:

1. **domain_model.md** - Verify lifecycle descriptions match
2. **mvp_stories_*.md** - Update stories related to state transitions
3. **mvp_tasks_*_lifecycle.md** - Update lifecycle implementation tasks

### When CLAUDE.md changes:

1. **No downstream dependencies** - This is a summary document for AI assistant

### When risk_strategy_ui changes:

1. **mvp_stories_frontend.md** - Update UI-related stories
2. **mvp_tasks_*_page.md** - Update page implementation tasks
3. **mvp_tasks_*_form.md** - Update form implementation tasks

## Consistency Checks

### Domain Model ↔ Data Model
- Every entity in domain model should have corresponding table(s) in data model
- Relationships in domain model should match foreign keys in data model
- Aggregates in domain model should have clear table ownership in data model

### Domain Model ↔ State Machine
- Every entity with lifecycle in domain model should have state diagram
- States in domain model should match states in state machine
- Transitions in domain model should match transitions in state machine

### Domain Model ↔ CLAUDE.md
- Architecture description in CLAUDE.md should match domain model
- Business rules in CLAUDE.md should match domain model
- Role matrix in CLAUDE.md should match domain model

### Domain Model ↔ UI Prototype
- Entity names in UI should match domain model
- Forms in UI should match entity attributes in domain model
- Workflows in UI should match lifecycles in domain model

## Critical Consistency Points

1. **Entity Names** - Must be identical across all documents
2. **State Names** - Must match between domain model, state machine, and UI
3. **Relationship Cardinality** - Must match between domain model and data model
4. **Business Rules** - Must be consistent across domain model, CLAUDE.md, and implementation tasks
5. **Role Permissions** - Must match between domain model and CLAUDE.md

## Validation Checklist

When making changes, verify:

- [ ] Entity names consistent across all files
- [ ] Domain model and data model aligned
- [ ] Domain model and state machine aligned
- [ ] CLAUDE.md reflects current architecture
- [ ] UI prototype uses correct terminology
- [ ] MVP stories reference correct entities
- [ ] MVP tasks reference correct entities
- [ ] Glossary definitions up to date
- [ ] No orphaned references to old terminology
