# Сводка задач MVP v6.8 (Rescoped: no Initiatives, add Chains/Lineage, deployments included; add artifacts/related blocks on Simulation pages/forms)

**Спецификация:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md)  
**План/оценки:** `Gantt v6.8` (см. `planning/mvp/current/gantt/`)

## Термины (важно)

- В рамках MVP v6.8 **Инициативы (Initiative) не реализуются** (CRUD/страницы/ЖЦ исключены из скоупа).
- `Deployment` (Внедрение) есть в MVP и является ключевой сущностью для "цепочек" (lineage) и вывода истории происхождения.
- "Цепочки" в MVP = UI-визуализация **Lineage** (как в spec), а не отдельная CRUD-сущность.
- `Simulation` в MVP **не дорабатываем по бизнес-логике/ЖЦ**, но добавляем на страницы и формы блоки "Артефакты" (URL) и "Связанные сущности" (read-only); важно, что симуляции не участвуют в approval/ratification.
- `auto_ratification=false` означает "очередь ожидания утверждения" с возможностью запустить ratification индивидуально или через Package (см. задачи Packages/Approval).
- Scope note: возможно потребуется декомпозировать задачи по скоркартам для поддержки "создать скоркарту по результатам симуляции" (+3 дня BE и +3 дня FE, оценочно).

## Карта "Gantt -> Task docs"

- **Approval / Package (Фаза 1):**
  - `AN_AP1`, `BE_AP1`: процесс согласования/утверждения: [mvp_tasks_approval_process_backend.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_approval_process_backend.md)
  - `AN_APR1`, `BE_APR1`, `FE_APR1`: страница "Согласования": [mvp_tasks_approvals_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_approvals_page.md)
  - `AN_PKG1`, `BE_PKG1`, `FE_PKG1`: страница "Пакеты": [mvp_tasks_packages_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_packages_page.md)
  - `BE_INT1`: интеграция ЖЦ с результатами согласования: [mvp_tasks_approval_integration.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_approval_integration.md)
  - `BE_ART1`: артефакты (URL ссылки): [mvp_tasks_artifacts_backend.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_artifacts_backend.md)
  - `BE_SC_INT1`: интеграция скоркарт (hook-места статусов/использования): [mvp_tasks_scorecards_integration.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_scorecards_integration.md)
  - `BE_NOT1`: email/уведомления: [mvp_tasks_notifications.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_notifications.md)
  - `QA_PHASE1`: тестирование фазы 1: [mvp_tasks_qa_phase1.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_qa_phase1.md)

- **Chains / Lineage (Цепочки происхождения):**
  - `AN_D1`, `BE_D1`, `FE_D1`: страница "Цепочки" (list): [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_chains_page.md)
  - `BE_DD1`, `FE_DD1`: lineage detail (widget/endpoint): [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_chains_page.md)
  - `BE_CD1`, `FE_CD1`: источники lineage при создании + UX-preview: [mvp_tasks_chains_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_chains_page.md)

- **Deployment (Внедрения):**
  - `AN_C1`, `BE_C1`, `FE_C1`: список внедрений: [mvp_tasks_deployments_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_deployments_page.md)
  - `AN_CHD1`, `BE_CHD1`, `FE_CHD1`: детальная внедрения: [mvp_tasks_deployment_detail_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_deployment_detail_page.md)
  - `AN_CHF1`, `BE_CHF1`, `FE_CHF1`: форма внедрения: [mvp_tasks_deployment_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_deployment_form.md)
  - `BE_CL1`: жизненный цикл внедрения: [mvp_tasks_deployment_lifecycle.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_deployment_lifecycle.md)

- **Scorecards:**
  - `AN_SC1`, `BE_SC1`, `FE_SC1`: список скоркарт: [mvp_tasks_scorecards_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_scorecards_page.md)
  - `AN_SCD1`, `BE_SCD1`, `FE_SCD1`: детальная скоркарты: [mvp_tasks_scorecard_detail_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_scorecard_detail_page.md)
  - `AN_SCF1`, `BE_SCF1`, `FE_SCF1`: форма скоркарты (с `ScorecardVersion`): [mvp_tasks_scorecard_form.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_scorecard_form.md)

- **Pilot:**
  - `AN_P1`, `BE_P1`, `FE_P1`: список пилотов: [mvp_tasks_pilots_page.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_pilots_page.md)
  - `AN_PA1`, `BE_PA1`, `FE_PA1`: блоки "Артефакты" и "Связанные сущности" на страницах пилота (create/edit/detail): [mvp_tasks_pilot_artifacts_related.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_pilot_artifacts_related.md)
  - `FE_PD1`: деталка пилота (см. задачи по пилоту и `FE_PA1`; backend-часть по артефактам/related включена в `BE_PA1`)

- **Simulation (добавить блоки "Артефакты" и "Связанные сущности"):**
  - `FE_SA1`: блоки на страницах/формах симуляции: [mvp_tasks_simulation_artifacts_related.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_simulation_artifacts_related.md)

- **Навигация + финальный QA:**
  - `FE_NAV1`: меню: [mvp_tasks_navigation_menu.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_navigation_menu.md)
  - `QA_PHASE2`, `QA_FINAL`: тестирование фазы 2 и финал: [mvp_tasks_qa_phase2.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_qa_phase2.md), [mvp_tasks_qa_final.md](/home/reutov/Documents/AI/changesWork/planning/mvp/versions/v6.8/tasks/mvp_tasks_qa_final.md)

## Примечания по расхождениям "tasks vs Gantt"

- В `Gantt v6` отсутствует отдельная backend-задача `BE-PD1` (деталка пилота), при этом фронтенд-деталка `FE_PD1` запланирована. Это трактуем как допущение плана: backend-деталка уже существует (или входит в `BE_P1`). Если это не так, нужно добавить backend-работы в план.
