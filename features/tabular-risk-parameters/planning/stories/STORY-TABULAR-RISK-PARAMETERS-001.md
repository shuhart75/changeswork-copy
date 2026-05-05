# STORY-TABULAR-RISK-PARAMETERS-001

Feature: `features/tabular-risk-parameters/feature.md`  
Статус: **импортировано из legacy-плана и materialized в backlog**  
Дата обновления: `2026-05-04`

## Summary
Backend табличных риск-параметров и интеграция с источниками/запуском симуляции

## Description
Собрать backend-контур табличных риск-параметров: базовую модель, API и логику, получение и обработку данных из смежного РП-контура, передачу табличных РП при запуске симуляции, а также follow-up по очистке файлов.

## Ideal scope
Полный backend-конвейер табличных риск-параметров без ручных временных артефактов, с устойчивыми интеграциями и операционной очисткой временных данных.

## MVP scope
- API, БД и базовая логика;
- интеграция с РП для получения и обработки табличных РП;
- интеграция с ФП Симуляция при запуске;
- scheduler очистки файлов.

## Analyst anchor estimate
- AN: 0 человеко-дней
- FE: 0 человеко-дней
- BE: 12 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Team estimate
- AN: 0 человеко-дней
- FE: 0 человеко-дней
- BE: 12 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Agreed estimate
- AN: 0 человеко-дней
- FE: 0 человеко-дней
- BE: 12 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2430`
- `RSCON-2431`
- `RSCON-2432`
- `RSCON-2452`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от simulation-related запуска и от доступности источника табличных РП;
- follow-up `RSCON-2452` трактуем как продолжение того же backend-контура, а не как отдельную feature.

## Notes for quarter planning
Planning story собрана из legacy generic `BE_RISK_TABLE`, но оценка и actualization выровнены по реальному backlog, который уже существует в актуальном трекинге.
