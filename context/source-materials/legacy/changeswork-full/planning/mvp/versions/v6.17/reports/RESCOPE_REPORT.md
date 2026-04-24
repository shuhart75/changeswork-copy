# Отчет по рескоупу MVP (v6.3)

**Дата:** 2026-03-11  
**Основа спецификации:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md) (v3.1)  
**Основа оценок:** Gantt v6 (длительности/зависимости сохранены, изменены только названия/смысл D-трека)

## Что изменилось относительно v6.2

### 1) Инициативы исключены из MVP

- Убраны задачи и страницы для `Initiative` (CRUD/деталка/создание/ЖЦ) из планирования v6.3.
- В task-доках удалены обязательные ссылки на `initiative_id` и группировки по Initiative.

### 2) Добавлены "цепочки" как Lineage

- В MVP v6.3 "цепочки" трактуются как **Lineage** (визуализация происхождения через связи "создано из"), без CRUD-сущности `chain`.
- Добавлен task-док: [`tasks/mvp_tasks_chains_page.md`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/tasks/mvp_tasks_chains_page.md).
- В Gantt v6 задачи D-трека переиспользованы по оценкам, но переименованы под Chains/Lineage:
  - `AN_D1/BE_D1/FE_D1` = Chains list
  - `BE_DD1/FE_DD1` = Lineage detail widget/endpoint
  - `BE_CD1/FE_CD1` = Auto-link источников + preview в формах

### 3) Симуляции не участвуют в согласованиях

- `Simulation` остается с независимым жизненным циклом (draft/running/completed/failed).
- Согласования/утверждения применяются только к `Pilot`/`Deployment`/`Package` (как было до правок).

## Точки входа v6.3

- Gantt: [`gantt/mvp_gantt_chart_current.puml`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/gantt/mvp_gantt_chart_current.puml)
- Tasks index: [`tasks/mvp_tasks_summary.md`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/tasks/mvp_tasks_summary.md)
- Prototype: [`prototype.html`](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.3/prototype.html)
