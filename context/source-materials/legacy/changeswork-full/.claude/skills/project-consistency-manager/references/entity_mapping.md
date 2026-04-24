# Entity Mapping

This document defines the canonical entity names and their mappings across versions.

## Current Version: 3.1

### Primary Entities

| v3.0 Term (Old) | v3.1 Term (New) | English | Description |
|-----------------|-----------------|---------|-------------|
| Deployment | Initiative | Initiative | Top-level aggregate grouping all strategic work |
| Change | Deployment | Deployment | Product deployment phase of strategy modification |
| Stage | (decomposed) | - | Decomposed into Simulation, Pilot, Deployment |
| Simulation | Simulation | Simulation | Historical data analysis phase |
| Pilot | Pilot | Pilot | Real-world experiment phase |

### Supporting Entities

| Russian | English | Description |
|---------|---------|-------------|
| Скоркарта | Scorecard | Credit decision scorecard |
| Пакет | Package | Group of Pilots/Deployments for joint ratification |
| Lineage | Lineage | Visualization of origin (Simulations → Pilots → Deployments) |

### Roles

| Russian | English | Code | Description |
|---------|---------|------|-------------|
| ПРМ | Product Risk Manager | prm | Manages initiatives for their product |
| Методолог | Methodologist | methodologist | Manages scorecards and documents |
| Согласующий | Approver | approver | Approves at Approval stages |
| Утверждающий | Ratifier | ratifier | Ratifies at Ratification stage |
| Администратор | Administrator | admin | Full access |

## Search Patterns

When checking for old terminology, search for these patterns:

### Russian Context
- `Внедрение` in context of top-level aggregate → should be `Инициатива`
- `Изменение` in context of product deployment → should be `Внедрение`
- `Deployment` in English context referring to top-level → should be `Initiative`
- `Change` in English context referring to product deployment → should be `Deployment`

### Context Clues

**Initiative (Инициатива) context:**
- "агрегат верхнего уровня" (top-level aggregate)
- "группировка всей работы" (grouping all work)
- "содержит Симуляции, Пилоты, Внедрения" (contains Simulations, Pilots, Deployments)
- "архивирование Инициативы" (archiving Initiative)

**Deployment (Внедрение) context:**
- "продуктовое внедрение" (product deployment)
- "фаза внедрения" (deployment phase)
- "откат Внедрения" (rollback Deployment)
- "статус: deployed" (status: deployed)

## Special Cases

### Files That Should NOT Be Changed

- Historical documents (CHANGELOG, review answers, summaries)
- Backup files (*.bak, *.backup)
- Files explicitly marked as v3.0 (unless creating v3.1 version)

### Files That Need Manual Review

- UI prototypes (HTML files) - terminology in JavaScript code and UI labels
- PlantUML diagrams - entity names in diagram syntax
- CLAUDE.md - project instructions for AI assistant
