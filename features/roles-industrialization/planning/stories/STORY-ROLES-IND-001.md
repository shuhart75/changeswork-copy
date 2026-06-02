# STORY-ROLES-IND-001

Feature: `features/roles-industrialization/feature.md`  
Статус: **новая planning story**  
Дата обновления: `2026-06-01`

## Summary
Каталог ролей и матрица совместимости

## Description
Зафиксировать промышленный каталог ролей АС КОДА, список продуктовых кодов `{space.code}` и правила совместимости ролей, чтобы Q3-дельта была отделена от уже существующего Q2 RBAC control layer.

## Ideal scope
Единая каноническая модель ролей, продуктовых кодов и ограничений совмещения, пригодная для дальнейшего baseline promotion и cross-feature enforcement.

## MVP scope

- глобальные роли `auditor`, `experiment_limited_view`, `experiment_admin`;
- продуктовые роли `experiment_editor_{space.code}`, `metodolog_{space.code}`, `simulation_specialist_{space.code}`;
- справочник `{space.code}` из источника;
- матрица совместимости ролей;
- явная граница между Q2 imported RBAC scope и новой Q3-дельтой.

## Analyst anchor estimate

- AN: 2 человеко-дней
- FE: 1 человеко-дней
- BE: 3 человеко-дней
- QA: 1 человеко-дней
- Total: 7 человеко-дней

## Team estimate

- AN: 2 человеко-дней
- FE: 1 человеко-дней
- BE: 3 человеко-дней
- QA: 1 человеко-дней
- Total: 7 человеко-дней

## Agreed estimate

- AN: 2 человеко-дней
- FE: 1 человеко-дней
- BE: 3 человеко-дней
- QA: 1 человеко-дней
- Total: 7 человеко-дней

## Actualization state

- `virtual`

## Mapping mode

- `explicit`

## Replaced by implementation tasks

- none yet

## Residual virtual tasks on actual-progress

- none

## Dependencies and assumptions

- не переоткрывает Q2 `features/roles/`, а описывает только новую целевую модель;
- для `experiment_limited_view` используется рабочее допущение read-only, пока не появится более детальная функциональная спецификация.

## Notes for quarter planning

Опирается на `/home/reutov/Downloads/roll_model_koda.md` и должен остаться отдельной Q3 story, не смешанной с imported RBAC story `STORY-ROLES-001`.
