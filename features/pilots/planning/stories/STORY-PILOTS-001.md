# STORY-PILOTS-001

Feature: `features/pilots/feature.md`  
Статус: **импортировано из legacy-плана и пока живёт virtual execution items**  
Дата обновления: `2026-05-04`

## Summary
Workspace пилотов: артефакты и lifecycle approval

## Description
Зафиксировать planning-story для pilot-centric execution, который уже виден в imported actualized gantt: FE-блок артефактов на странице пилота и backend lifecycle approval-поток пилота.

## Ideal scope
Единый workspace пилотов с согласованными блоками артефактов, lifecycle actions и approval semantics.

## MVP scope
- аналитика FE-блока артефактов пилота;
- frontend-блок артефактов и UI под ЖЦ;
- аналитика lifecycle approval для пилота;
- backend lifecycle approval для пилота.

## Analyst anchor estimate
- AN: 2 человеко-дня
- FE: 4 человеко-дня
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 11 человеко-дней

## Team estimate
- AN: 2 человеко-дня
- FE: 4 человеко-дня
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 11 человеко-дней

## Agreed estimate
- AN: 2 человеко-дня
- FE: 4 человеко-дня
- BE: 5 человеко-дней
- QA: 0 человеко-дней
- Total: 11 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- `AN_FE_PILOT_ART`
- `FE_PILOT_ART`
- `AN_PILOT_LC_AP`
- `BE_PILOT_LC_AP`

## Dependencies and assumptions
- shared backend артефактов остаётся в feature `artifacts`, а здесь фиксируется pilot-hosted поведение;
- approval/lifecycle semantics зависят от feature `approvals`, но pilot-specific execution сохраняется здесь.

## Notes for quarter planning
Story заведена только сейчас, потому что execution items уже были в imported tracking, но planning-опора для них отсутствовала.
