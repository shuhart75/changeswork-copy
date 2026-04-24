# MVP Planning v6.14

**Base spec:** `spec/domain_model.md`  
**Base schedule:** Gantt v6.14 (см. `gantt/`, файл `mvp_gantt_chart_current.puml` указывает на `mvp_gantt_chart_v6.14.puml`)

## Entry points

- Prototype (MVP): `prototype.html` (symlink to `prototypes/current.html`)
- Gantt: `gantt/mvp_gantt_chart_current.puml`
- Tasks index: `tasks/mvp_tasks_summary.md`
- MVP scope / plan / stories / timeline: `docs/`

## Notes (MVP v6.14 scope)

- **Инициативы (Initiative)** исключены из MVP (CRUD/страницы/ЖЦ не делаем).
- **Внедрения (Deployments)** включены в MVP: список, деталка, форма создания/редактирования, ЖЦ, версии, approval/ratification.
- Симуляции НЕ участвуют в согласовании/утверждении (существующий ЖЦ не меняем).
- Блоки **"Артефакты" (URL)** и **"Связанные сущности"** добавляем на страницы и формы: Simulation, Pilot, Deployment.
- Страницы **"Цепочки"** и lineage widget **не делаем** (ни в MVP, ни вообще). В MVP остаются только источники `created_from`: автосоздание на create + preview в формах.
- **Список скоркарт** (страница/роут/пункт меню) исключен из MVP; в MVP остаются **деталка** и **создание/редактирование** скоркарты.
- Уточнены правила ratification (поэлементные статусы в пакете), статусы при reject (`approval_rejected` / `ratification_rejected`) и обязательный recall.

Рекомендуемая точка входа по задачам: `tasks/mvp_tasks_execution_order.md`.
