# Симуляции — Детальная страница (Backend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_detail_page.md`

## Подтверждённый API-контур
- `GET /api/simulations/{id}/`
- `GET /api/simulations/{id}/related/`

## Что должна возвращать деталка
- `id`
- `display_id`
- `name`
- `status`
- `product`
- `created_at`
- `started_at`
- `completed_at`
- `created_by`
- `artifacts_count`
- `related_pilots_count`
- `related_changes_count`

## Связанные сущности
- read-only связи строятся через скоркарты;
- simulation detail не живёт отдельно от cross-feature связи с `Pilot` и `Deployment`.
