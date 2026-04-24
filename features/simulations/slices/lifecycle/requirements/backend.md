# Симуляции — Жизненный цикл (Backend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_lifecycle.md`
- `context/source-materials/current-system/diagrams/raw/spec_state_machine.puml`

## Status model
- `draft`
- `running`
- `completed`
- `failed`

## Разрешённые переходы
- `draft -> running`
- `running -> completed`
- `running -> failed`

## Подтверждённый API-контур
- `POST /api/simulations/{id}/start/`
- `POST /api/simulations/{id}/complete/`
- `POST /api/simulations/{id}/fail/`

## Бизнес-правила
- simulation lifecycle независим от approval flow;
- lifecycle-действия разрешены ПРМ своего продукта или админу;
- при `complete` сохраняется `result`;
- при `fail` сохраняется `error_message`.
