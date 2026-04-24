# Порядок выполнения задач MVP (v6.6)

Источник оценок и порядка: `planning/mvp/current/gantt/mvp_gantt_chart_current.puml` (Gantt v6.6, rescoped).

## Фаза 0. Аналитика (вся вперед)

- `AN_AP1` Аналитика процесса согласования
- `AN_APR1` Аналитика страницы "Согласования"
- `AN_PKG1` Аналитика страницы "Пакеты"
- `AN_C1` Аналитика списка внедрений
- `AN_P1` Аналитика адаптации пилотов
- `AN_CHD1` Аналитика деталки внедрения
- `AN_CHF1` Аналитика формы внедрения
- `AN_PA1` Аналитика блоков "Артефакты" и "Связанные сущности" на страницах пилота
- `AN_D1` Аналитика цепочек (Lineage)
- `AN_SC1` Аналитика списка скоркарт
- `AN_SCD1` Аналитика деталки скоркарты
- `AN_SCF1` Аналитика формы скоркарты
- `AN_CD1` Аналитика источников lineage ("создано из")

## Фаза 1. Approval/Ratification + Packages

- `BE_AP1` Backend процесс согласования (`ApprovalInstance/Stage/Assignment/Decision`)
- `BE_INT1` Интеграция ЖЦ (Pilot/Deployment) с результатами согласования
- `BE_PL1` ЖЦ пилота
- `BE_ART1` Артефакты (ссылки на документы)
- `BE_SC_INT1` Интеграция скоркарт (hook-места)
- `BE_NOT1` Уведомления
- `BE_APR1` Backend страницы "Согласования"
- `BE_PKG1` Backend страницы "Пакеты"
- `FE_APR1` Frontend страницы "Согласования"
- `FE_PKG1` Frontend страницы "Пакеты"
- `QA_PHASE1` Тестирование фазы 1

## Фаза 2. Внедрения (Deployment)

- `BE_CL1` ЖЦ внедрения (submit_for_approval/deploy/rollback)
- `BE_CHD1` Backend деталки внедрения
- `BE_CHF1` Backend формы внедрения
- `BE_C1` Backend списка внедрений
- `FE_C1` Frontend списка внедрений
- `FE_CHD1` Frontend деталки внедрения
- `FE_CHF1` Frontend формы внедрения

## Фаза 3. Scorecards

- `BE_SC1` Backend списка скоркарт
- `BE_SCD1` Backend деталки скоркарты
- `BE_SCF1` Backend формы скоркарты
- `FE_SC1` Frontend списка скоркарт
- `FE_SCD1` Frontend деталки скоркарты
- `FE_SCF1` Frontend формы скоркарты

## Фаза 4. Pilots (страницы/формы)

- `BE_P1` Backend списка пилотов
- `BE_PA1` Backend блоков "Артефакты" и "Связанные сущности" на пилоте
- `FE_P1` Frontend списка пилотов
- `FE_PD1` Frontend деталки пилота
- `FE_PA1` Frontend блоков "Артефакты" и "Связанные сущности" на пилоте (create/edit/detail)

## Фаза 5. Цепочки (Lineage)

- `BE_D1` Backend цепочек (list)
- `BE_DD1` Backend lineage (detail)
- `BE_CD1` Backend автосоздания источников lineage
- `FE_D1` Frontend цепочек (list)
- `FE_DD1` Frontend lineage (widget)
- `FE_CD1` Frontend preview lineage в формах
- `QA_PHASE5` Тестирование сложных страниц

## Финал

- `FE_NAV1` Навигационное меню
- `QA_PHASE2`, `QA_PHASE3`, `QA_PHASE4` Промежуточные тесты (по плану)
- `QA_FINAL` Финальное тестирование
