# MVP Scope v6.3 (Rescoped)

**Цель:** MVP без реализации `Initiative`, но с полным циклом согласования/утверждения и с отслеживанием "цепочек" (lineage).

## In-scope (делаем в MVP)

- **Simulation**
  - создание/редактирование/запуск/завершение
  - **не участвует** в согласовании/утверждении (независимый ЖЦ)
- **Pilot**
  - создание/редактирование
  - согласование/утверждение через `ApprovalInstance(target_type='pilot')`
- **Deployment**
  - создание/редактирование
  - согласование/утверждение через `ApprovalInstance(target_type='deployment')`
  - deploy/rollback
- **Approval / Ratification**
  - `ApprovalInstance/ApprovalStage/ApprovalAssignment/ApprovalDecision`
  - страница "Согласования" (мои назначения)
- **Reject/Recall правила (MVP):**
  - Reject возвращает сущность в `approval_rejected` или `ratification_rejected` (не в draft)
  - Из этих статусов доступны: редактирование, повторная отправка на согласование/утверждение, архивирование
  - Recall (отзыв с согласования/утверждения) поддержан обязательно
  - Recall поддержан:
    - для Pilot/Deployment индивидуально
    - для элементов в составе Package (отзыв item возвращает его в `awaiting_ratification`, Package продолжает по оставшимся)
    - для Package целиком
- **Packages**
  - ручное формирование Package из элементов в `awaiting_ratification` (Pilot/Deployment)
  - ratification через `ApprovalInstance(target_type='package')`
  - элементы из `awaiting_ratification` могут быть отправлены на ratification и **индивидуально**, и **в составе Package** (по команде пользователя)
- **Chains (Lineage)**
  - страница "Цепочки" как визуализация lineage по связям "создано из"
  - lineage endpoints (GET) + автосоздание `*_source` связей при создании Pilot/Deployment по скоркартам
- **HTML прототип**
  - `prototypes/current.html` остается главным артефактом MVP для демо и передачи

## Out-of-scope (не делаем в MVP)

- `Initiative` (CRUD/страницы/жизненный цикл/архивирование/расчет статуса)
- Любые отдельные CRUD-сущности `chain/*` (цепочка не хранится как отдельная таблица, вычисляется как lineage)

## Точки входа

- План: `planning/mvp/current/`
- Gantt: `planning/mvp/current/gantt/mvp_gantt_chart_current.puml`
- Tasks: `planning/mvp/current/tasks/mvp_tasks_summary.md`
- Prototype: `prototypes/current.html`
