# Симуляции — Форма создания и редактирования (Backend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_form.md`

## Подтверждённый API-контур
- `POST /api/simulations/`
- `PUT /api/simulations/{id}/`

## Основные правила
- симуляция создаётся в статусе `draft`;
- `deployment_id` обязателен и должен существовать;
- период данных обязателен и валиден (`from <= to`);
- тип симуляции должен входить в поддерживаемый набор MVP;
- редактирование разрешено только в статусе `draft`;
- артефакты не хранятся в payload симуляции, а живут через отдельные artifact endpoints.
