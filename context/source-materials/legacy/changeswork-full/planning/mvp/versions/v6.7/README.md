# MVP Planning v6.7 (Pilots pages: artifacts+related; pilot form out of scope)

**Base spec:** `spec/domain_model.md` (v3.1)  
**Base schedule:** Gantt v6 (см. `gantt/`, файл `mvp_gantt_chart_current.puml` указывает на `mvp_gantt_chart_v6.7.puml`)

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
- Добавлено уточнение по аналитике/UX выбора маршрута согласования при отправке сущности на согласование (входит в `AN_AP1`, +3 дня к аналитике процесса согласования).
- Из MVP убраны задачи по форме пилота (`AN/BE/FE-PF1`); вместо этого добавлены задачи на добавление блоков "Артефакты" и "Связанные сущности" на страницы пилота (create/edit/detail): `AN/BE/FE-PA1` (3+3+3).
- `docs/` импортированы из v6.0 как полнота артефактов; для MVP v6.7 источником правды по работам считать `tasks/` и `gantt/`.

Рекомендуемая точка входа по скоупу: `docs/mvp_scope_v6.3.md` (содержит rescoped-скоуп; имя файла историческое).
