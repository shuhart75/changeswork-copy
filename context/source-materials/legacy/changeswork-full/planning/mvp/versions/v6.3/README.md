# MVP Planning v6.3 (Rescoped)

**Base spec:** `spec/domain_model.md` (v3.1)  
**Base schedule:** Gantt v6 (см. `gantt/`)

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
- `docs/` импортированы из v6.0 как полнота артефактов; для MVP v6.3 источником правды по работам считать `tasks/` и `gantt/`.

Рекомендуемая точка входа по скоупу: `docs/mvp_scope_v6.3.md`.
