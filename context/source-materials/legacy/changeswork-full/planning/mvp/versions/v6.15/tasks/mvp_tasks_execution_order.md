# Порядок выполнения задач MVP (v6.15)

Источник порядка и оценок: `gantt/mvp_gantt_chart_current.puml` (source: ProjectLibre `Q2.pod`).

Детальный скоуп (AN+DEV) по каждой задаче: `tasks/mvp_tasks_projectlibre_alignment.md`.

## Группы и порядок (внутри группы)

1. Роли: `AN_ROLES` -> `BE_ROLES`
2. Артефакты:
   `AN_ART_BE` -> `BE_ART` -> `AN_FE_PILOT_ART` -> `FE_PILOT_ART` -> `AN_FE_SIM_ART` -> `FE_SIM_ART`
3. Согласования/утверждения:
   `AN_AP_CORE` -> `BE_AP_CORE` -> `AN_PILOT_LC_AP` -> `BE_PILOT_LC_AP` -> `AN_AP_PAGE_BE` -> `BE_AP_PAGE` -> `AN_AP_PAGE_FE` -> `FE_AP_PAGE`
   и параллельно ветка пакетов:
   `AN_PKG_BE` -> `BE_PKG_PAGE` -> `AN_PKG_FE` -> `FE_PKG_PAGE`
4. Внедрения:
   `AN_DEP_BE` -> `BE_DEP_API` -> `AN_DEP_LC` -> `BE_DEP_LC` -> `AN_FE_DEP_LIST` -> `FE_DEP_LIST` -> `AN_FE_DEP_FORM` -> `FE_DEP_FORM`
5. Скоркарты (без списка):
   `AN_SC_BE` -> `BE_SC_API` -> `AN_SCD_BE` -> `BE_SCD` -> `AN_SCD_FE` -> `FE_SCD` -> `AN_SCF_BE` -> `BE_SCF` -> `AN_SCF_FE` -> `FE_SCF`
6. Уведомления: `AN_NOT` -> `BE_NOT`
7. Trace: `AN_TRACE_BE` -> `BE_TRACE` -> `AN_TRACE_FE` -> `FE_TRACE`
8. QA: `QA_SETUP` -> `QA_ART` -> `QA_AP` -> `QA_SC` -> `QA_TRACE` -> `QA_REG`
