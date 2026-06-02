# STORY-ROLES-IND-003

Feature: `features/roles-industrialization/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-06-01`

## Summary
Cross-feature propagation pack и регрессионные правила

## Description
Подготовить пакет правил для переноса новой ролевой модели в соседние feature requirements, host screens и regression coverage, не затрагивая уже зафиксированный Q2 planning scope.

## Ideal scope
Цельный пакет консистентности: новые role names, product scope rules, endpoint matrix, FE visibility rules и regression points для `pilots`, `simulations`, `artifacts` и baseline/current.

## MVP scope

- список затронутых соседних feature packs;
- правила синхронизации FE visibility и backend enforcement;
- регрессионный чеклист по role gating;
- deferred propagation через `domain-impact.md` и `.workflow/consistency-backlog.md`;
- явное разграничение между Q3 requirements и текущим кварталом.

## Analyst anchor estimate

- AN: 2 человеко-дней
- FE: 3 человеко-дней
- BE: 3 человеко-дней
- QA: 2 человеко-дней
- Total: 10 человеко-дней

## Team estimate

- AN: 2 человеко-дней
- FE: 3 человеко-дней
- BE: 3 человеко-дней
- QA: 2 человеко-дней
- Total: 10 человеко-дней

## Agreed estimate

- AN: 2 человеко-дней
- FE: 3 человеко-дней
- BE: 3 человеко-дней
- QA: 2 человеко-дней
- Total: 10 человеко-дней

## Actualization state

- `virtual`

## Mapping mode

- `explicit`

## Replaced by implementation tasks

- none yet

## Residual virtual tasks on actual-progress

- none

## Dependencies and assumptions

- зависит от `STORY-ROLES-IND-001` и `STORY-ROLES-IND-002`;
- не тянет за собой немедленную baseline promotion;
- для Q3 достаточно зафиксировать соседние impact points и tester coverage, даже если полная propagation произойдёт позже.

## Notes for quarter planning

Story нужна именно как отдельный Q3 пакет, чтобы новая ролевая модель не осталась локальной таблицей без маршрута в соседние фичи.
