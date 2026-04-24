# Симуляции — Lifecycle UX (Frontend)

Статус: **legacy imported existing coverage**
Область: baseline
Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_simulation_lifecycle.md`
- `context/source-materials/current-system/diagrams/raw/spec_state_machine.puml`

## Что фиксируем на уровне UI
- отображение статусов `draft`, `running`, `completed`, `failed`;
- отсутствие integration с approval / ratification;
- доступность lifecycle-действий только для ролей, которым это разрешено по продукту;
- completed/failed simulation трактуется как immutable для обычного редактирования.
