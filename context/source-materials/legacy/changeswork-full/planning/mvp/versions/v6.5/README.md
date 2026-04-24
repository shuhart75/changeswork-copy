# MVP Planning v6.5 (Approval Decisions уточнены)

**Base spec:** `spec/domain_model.md` (v3.1)  
**Base schedule:** Gantt v6 (см. `gantt/`, файл `mvp_gantt_chart_current.puml` указывает на `mvp_gantt_chart_v6.5.puml`)

## Entry points

- Prototype (MVP): `prototype.html` (symlink to `prototypes/current.html`)
- Gantt: `gantt/mvp_gantt_chart_current.puml`
- Tasks index: `tasks/mvp_tasks_summary.md`
- Alignment report: `reports/ALIGNMENT_REPORT.md`
- Rescope report: `reports/RESCOPE_REPORT.md`
- MVP scope / plan / stories / timeline: `docs/`

## Notes

- Эта версия фиксирует изменение скоупа MVP:
  - **Инициативы (Initiative)** исключены из MVP (CRUD/страницы/ЖЦ не делаем)
  - добавлено **отслеживание цепочек** как UI-визуализация **Lineage** (см. `tasks/mvp_tasks_chains_page.md`)
  - `Deployment` остается в MVP как продуктовое внедрение
- Симуляции НЕ участвуют в согласовании/утверждении (независимый ЖЦ).
- Уточнена логика ratification + статусы при reject (approval_rejected / ratification_rejected) и обязательный recall.
- `docs/` импортированы из v6.0 как полнота артефактов; для MVP v6.5 источником правды по работам считать `tasks/` и `gantt/`.

Рекомендуемая точка входа по скоупу: `docs/mvp_scope_v6.3.md` (содержит rescoped-скоуп; имя файла историческое).
