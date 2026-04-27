# FEATURE-ROLES — Ролевая модель и RBAC

Статус: **импортировано из legacy-проекта**  
Квартал: `2026-Q2`  
Дата обновления: `2026-04-27`

## Цель
Собрать в одной feature MVP-правила ролевой модели, продуктового scope и ограничений доступа.

## Контекст
Feature импортирована из `changesWork` и current-system requirements. RBAC в проекте является сквозным слоем, влияющим на видимость разделов, доменные действия и интеграцию с существующим модулем `rscon-sudir`.

## Ideal scope
- единая каноническая модель ролей и их несовместимостей;
- product-scoped и global роли;
- согласованный FE/BE enforcement для UI и API;
- прозрачная интеграция с `rscon-sudir`.

## MVP scope
- роли `prm`, `methodologist`, `approver`, `ratifier`, `admin`;
- product scope и множественные роли;
- базовые матрицы видимости и действий;
- проверки доступа на уровне API и host screens.

## Что исключено из MVP
- сложный ABAC/policy engine;
- отдельный UI для администрирования ролей, если он отсутствует;
- event-sourced история изменения ролей.

## Входные материалы
- `references.md`
- `requirements.md`
- `slices/rbac/requirements/frontend.md`
- `slices/rbac/requirements/backend.md`

## Planning stories
- отдельные planning stories в standalone-проекте пока не нормализованы; imported RBAC scope зафиксирован как единый slice.

## Риски и зависимости
- feature доменно влияет почти на все соседние features;
- изменение RBAC semantics требует consistency sweep по baseline/current и feature requirements.

## Решение по кварталу
- [x] imported cross-feature scope зафиксирован
- [ ] берём как новую квартальную дельту
- [ ] дробим дополнительно
