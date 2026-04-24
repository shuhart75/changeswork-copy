# Симуляции — Список (Backend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulations_page.md`

## Подтверждённый API-контур
`GET /api/simulations/`

## Поддерживаемые query-параметры
- `product_id`
- `status`
- `search`
- `page`
- `page_size`
- `ordering`

## Ожидаемые поля ответа
- `id`
- `display_id`
- `name`
- `mode`
- `status`
- `stage`
- `stage_updated_at`
- `created_at`
- `created_by`

## Ограничения
- Это legacy-imported contract; URI-стиль ещё не выровнен до общего `v1`-паттерна.
- Доступ определяется продуктовым scope и ролью пользователя.
