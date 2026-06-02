# STORY-ROLES-IND-002

Feature: `features/roles-industrialization/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-06-01`

## Summary
Endpoint access matrix и backend enforcement rules

## Description
Разложить по endpoint operations права новой ролевой модели и зафиксировать backend enforcement rules, чтобы FE visibility и API-проверки опирались на одну таблицу доступа.

## Ideal scope
Полная и непротиворечивая матрица доступа по endpoint-level операциям для experiments, spaces, documents, simulations, files и связанных read-only справочников.

## MVP scope

- таблица endpoint mapping из источника;
- grouping одинаковых read-only прав для `auditor` и `experiment_limited_view`, пока не появится отдельная детализация;
- различение глобальных и product-scoped полномочий;
- правила для create/edit/delete/action operations;
- backend source-of-truth для последующей cross-feature синхронизации.

## Analyst anchor estimate

- AN: 2 человеко-дней
- FE: 2 человеко-дней
- BE: 4 человеко-дней
- QA: 1 человеко-дней
- Total: 9 человеко-дней

## Team estimate

- AN: 2 человеко-дней
- FE: 2 человеко-дней
- BE: 4 человеко-дней
- QA: 1 человеко-дней
- Total: 9 человеко-дней

## Agreed estimate

- AN: 2 человеко-дней
- FE: 2 человеко-дней
- BE: 4 человеко-дней
- QA: 1 человеко-дней
- Total: 9 человеко-дней

## Actualization state

- `virtual`

## Mapping mode

- `explicit`

## Replaced by implementation tasks

- none yet

## Residual virtual tasks on actual-progress

- none

## Dependencies and assumptions

- зависит от story `STORY-ROLES-IND-001`, потому что endpoint mapping должен ссылаться на уже согласованный каталог ролей;
- соседние feature packs будут обновляться отдельным propagation-проходом, а не в рамках перепланирования Q2.

## Notes for quarter planning

Главная цель story — не повторить MVP RBAC на новом языке, а зафиксировать промышленную матрицу прав как новый источник для Q3.
