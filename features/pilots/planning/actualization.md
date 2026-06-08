# Actualization map

Feature: `features/pilots/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- Для `pilots` actual-progress показываем существующие imported execution items и real-задачи, которые появились в текущем execution snapshot.
- `RSCON-2487` materializes pilot backend delta для симуляции конфигурации пилотов; старые virtual items остаются видимыми в task layer как imported coverage.

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-PILOTS-001 | Workspace пилотов: артефакты и lifecycle approval | 2026-04-01 | 13 | materialized | inferred | RSCON-2487 |  |  |
