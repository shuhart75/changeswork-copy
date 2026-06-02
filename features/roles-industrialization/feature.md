# FEATURE-ROLES-INDUSTRIALIZATION — Промышленная ролевая модель АС КОДА

Статус: **в проработке**  
Квартал: `2026-Q3`  
Дата обновления: `2026-06-01`

## Цель
Выделить в отдельную Q3 feature промышленную доработку ролевой модели АС КОДА: каталог глобальных и продуктовых ролей, матрицу совместимости и endpoint-level правила доступа.

## Контекст
Feature создана по результатам intake из внешнего источника `/home/reutov/Downloads/roll_model_koda.md`. В репозитории уже есть `features/roles/` как imported Q2 control layer для MVP RBAC, поэтому новая feature не подменяет этот слой, а добавляет отдельную квартальную дельту на следующий квартал.

## Ideal scope

- единый канонический каталог ролей с product-scoped pattern roles;
- непротиворечивая матрица совместимости ролей;
- endpoint-by-endpoint матрица прав для backend enforcement и FE visibility;
- явный пакет cross-feature propagation в `pilots`, `simulations`, `artifacts` и baseline/current;
- единая терминология по `space.code`, продуктовым ролям и ограничениям совмещения.

## MVP scope

- глобальные роли `auditor`, `experiment_limited_view`, `experiment_admin`;
- продуктовые роли `experiment_editor_{space.code}`, `metodolog_{space.code}`, `simulation_specialist_{space.code}`;
- справочник продуктовых кодов `{space.code}`;
- матрица совместимости ролей;
- маппинг ролей на endpoint operations из источника;
- living requirements для последующей cross-feature синхронизации.

## Что исключено из MVP

- перепланирование `planning/2026-Q2`;
- ретроактивная замена Q2 control-layer в `features/roles/`;
- release-promotion в `baseline/current/`;
- UI для администрирования ролей;
- фактическое выполнение всех соседних FE/BE правок в одном planning/requirements-проходе.

## Входные материалы

- `references.md`
- `requirements.md`
- `/home/reutov/Downloads/roll_model_koda.md`
- `features/roles/feature.md`
- `features/roles/requirements.md`

## Planning stories

- `planning/stories/STORY-ROLES-IND-001.md`
- `planning/stories/STORY-ROLES-IND-002.md`
- `planning/stories/STORY-ROLES-IND-003.md`

## Риски и зависимости

- в источнике не детализированы уникальные полномочия `experiment_limited_view`, поэтому часть read-only semantics фиксируется как рабочее допущение;
- новая feature доменно влияет на `features/roles/`, `features/pilots/`, `features/simulations/`, `features/artifacts/` и baseline/current;
- квартальный execution-tracking для Q3 нужно будет заводить отдельно, потому что текущий генератор `actual-progress` не изолирует feature по кварталу автоматически.

## Решение по кварталу

- [x] берём в квартал
- [ ] переносим
- [ ] дробим дополнительно
