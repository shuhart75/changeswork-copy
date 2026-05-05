# STORY-TABULAR-RISK-PARAMETERS-002

Feature: `features/tabular-risk-parameters/feature.md`  
Статус: **импортировано из legacy-плана и materialized в backlog**  
Дата обновления: `2026-05-04`

## Summary
Frontend форма изменения табличных риск-параметров

## Description
Переделать frontend-форму изменения риск-параметров под табличный сценарий, чтобы пользователь мог работать с новым набором данных в рамках существующего бизнес-потока.

## Ideal scope
Полноценная табличная форма изменения риск-параметров с устойчивым UX для длинных наборов строк и продуктовых различий.

## MVP scope
- переделка текущей формы изменения риск-параметров;
- работа с табличным набором данных в существующем потоке;
- без отдельной list/workspace-страницы.

## Analyst anchor estimate
- AN: 0 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Team estimate
- AN: 0 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Agreed estimate
- AN: 0 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 10 человеко-дней

## Actualization state
- `materialized`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- `RSCON-2429`

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- frontend-сценарий зависит от backend-контракта табличных РП;
- фактический исполнитель уже указан как `FE1`, что и используем в execution-слое.

## Notes for quarter planning
Legacy generic `FE_RISK_TABLE` был слишком грубым; story нормализована по реальной backlog-задаче `RSCON-2429`.
