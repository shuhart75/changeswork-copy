# Сводка задач MVP v6.4 (Rescoped: no Initiatives, add Chains/Lineage, deployments included)

**Спецификация:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)  
**План/оценки:** `Gantt v6` (см. `planning/mvp/current/gantt/`)

## Термины (важно)

- В рамках MVP v6.4 **Инициативы (Initiative) не реализуются** (CRUD/страницы/ЖЦ исключены из скоупа).
- `Deployment` (Внедрение) есть в MVP и является ключевой сущностью для "цепочек" (lineage) и вывода истории происхождения.
- "Цепочки" в MVP = UI-визуализация **Lineage** (как в spec), а не отдельная CRUD-сущность.
- `Simulation` НЕ проходит согласование/утверждение (независимый ЖЦ).

## Карта "Gantt -> Task docs"

- **Approval / Package (Фаза 1):**
  - `AN_AP1`, `BE_AP1`: процесс согласования/утверждения: [mvp_tasks_approval_process_backend.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_approval_process_backend.md)
  - `AN_APR1`, `BE_APR1`, `FE_APR1`: страница "Согласования": [mvp_tasks_approvals_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_approvals_page.md)
  - `AN_PKG1`, `BE_PKG1`, `FE_PKG1`: страница "Пакеты": [mvp_tasks_packages_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_packages_page.md)
  - `BE_INT1`: интеграция ЖЦ с результатами согласования: [mvp_tasks_approval_integration.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_approval_integration.md)
  - `BE_NOT1`: email/уведомления: [mvp_tasks_notifications.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_notifications.md)
  - `QA_PHASE1`: тестирование фазы 1: [mvp_tasks_qa_phase1.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_qa_phase1.md)

- **Chains / Lineage (Цепочки происхождения):**
  - `AN_D1`, `BE_D1`, `FE_D1`: страница "Цепочки" (list): [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_chains_page.md)
  - `BE_DD1`, `FE_DD1`: lineage detail (widget/endpoint): [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_chains_page.md)
  - `BE_CD1`, `FE_CD1`: источники lineage при создании + UX-preview: [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_chains_page.md)

- **Deployment (Внедрения):**
  - `AN_C1`, `BE_C1`, `FE_C1`: список внедрений: [mvp_tasks_deployments_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_deployments_page.md)
  - `AN_CHD1`, `BE_CHD1`, `FE_CHD1`: детальная внедрения: [mvp_tasks_deployment_detail_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_deployment_detail_page.md)
  - `AN_CHF1`, `BE_CHF1`, `FE_CHF1`: форма внедрения: [mvp_tasks_deployment_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_deployment_form.md)
  - `BE_CL1`: жизненный цикл внедрения: [mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_deployment_lifecycle.md)

- **Scorecards:**
  - `AN_SC1`, `BE_SC1`, `FE_SC1`: список скоркарт: [mvp_tasks_scorecards_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_scorecards_page.md)
  - `AN_SCD1`, `BE_SCD1`, `FE_SCD1`: детальная скоркарты: [mvp_tasks_scorecard_detail_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_scorecard_detail_page.md)
  - `AN_SCF1`, `BE_SCF1`, `FE_SCF1`: форма скоркарты (с `ScorecardVersion`): [mvp_tasks_scorecard_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_scorecard_form.md)

- **Simulation / Pilot:**
  - `AN_S1`, `BE_S1`, `FE_S1`: список симуляций: [mvp_tasks_simulations_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_simulations_page.md)
  - `AN_P1`, `BE_P1`, `FE_P1`: список пилотов: [mvp_tasks_pilots_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_pilots_page.md)
  - `AN_SF1`, `BE_SF1`, `FE_SF1`: форма симуляции: [mvp_tasks_simulation_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_simulation_form.md)
  - `AN_PF1`, `BE_PF1`, `FE_PF1`: форма пилота: [mvp_tasks_pilot_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_pilot_form.md)
  - `FE_SD1`, `FE_PD1`: детальные Simulation/Pilot в Gantt есть только как Frontend-задачи; Backend-часть предполагается существующей или включенной в `BE_S1/BE_P1` (см. примечания ниже)

- **Навигация + финальный QA:**
  - `FE_NAV1`: меню: [mvp_tasks_navigation_menu.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_navigation_menu.md)
  - `QA_PHASE2`, `QA_FINAL`: тестирование фазы 2 и финал: [mvp_tasks_qa_phase2.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_qa_phase2.md), [mvp_tasks_qa_final.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.4/tasks/mvp_tasks_qa_final.md)

## Примечания по расхождениям "tasks vs Gantt"

- В `Gantt v6` отсутствуют отдельные backend-задачи `BE-SD1` (деталка симуляции) и `BE-PD1` (деталка пилота), при этом фронтенд-деталки `FE_SD1/FE_PD1` запланированы. Это трактуем как допущение плана: backend-деталки уже существуют (или входят в `BE_S1/BE_P1`). Если это не так, нужно добавить backend-работы в план.
