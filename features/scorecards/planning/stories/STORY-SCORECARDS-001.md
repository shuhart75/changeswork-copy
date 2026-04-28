# STORY-SCORECARDS-001

Feature: `features/scorecards/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Backend foundation, шаблоны и критичность скоркарт

## Description
Подготовить базовую backend-модель скоркарты и её версий, API-контракты, шаблоны продукта и расчёт критичности, чтобы дальше на эту основу опирались workspace, detail и create/edit сценарии.

## Ideal scope
Цельная backend-основа scorecards domain: сущность, versioning, template versions, default config, валидаторы, relations и критичность.

## MVP scope
- сущность `Scorecard` и `ScorecardVersion`;
- шаблоны и default config;
- расчёт критичности;
- backend-контракты, достаточные для detail и create/edit flow.

## Analyst anchor estimate
- AN: 1 человеко-дней
- FE: 0 человеко-дней
- BE: 9 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Team estimate
- AN: 1 человеко-дней
- FE: 0 человеко-дней
- BE: 9 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Agreed estimate
- AN: 1 человеко-дней
- FE: 0 человеко-дней
- BE: 9 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `inferred`

## Replaced by implementation tasks
- `RSCON-2342`
- `RSCON-2343`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от продуктовых шаблонов и договорённостей по доменной модели;
- список скоркарт вне MVP и не должен раздувать backend scope этой story.

## Notes for quarter planning
Story собрана из legacy-потока `AN_SC_BE` + `BE_SC_API`, но в actual-progress материализована более узкими Jira-задачами по backend foundation.
