# QA задачи: Тестирование MVP (2 рабочих недели)

## QA-PHASE1: Тестирование MVP

**Тип:** Story  
**Приоритет:** Высокий  
**Оценка:** 10 дней (2 рабочих недели, подтверждено)  

### Summary
Комплексное тестирование всего MVP: Approval/Ratification + Packages, Внедрения, Пилоты, Скоркарты, Цепочки (Lineage), Артефакты (URL), блоки на Симуляциях, уведомления и навигация.

### Scope

1. **Approval/Ratification + Packages (core)**
- Submit на согласование для `PilotVersion` и `DeploymentVersion`.
- Мультистейдж approval (Approval stages): принять решение по assignment (approve/reject).
- `auto_ratification=false`: очередь `awaiting_ratification` + возможность утвердить индивидуально или через Package.
- Package:
  - минимум 2 элемента
  - batch approve/reject работает только для выбранных items (с галочками)
  - не выбранные items остаются индивидуально в очереди утверждения
  - статус/комментарии хранятся **на item**, не на Package (в item-history префикс "одобрено в составе пакета...")
- Reject не возвращает в draft: `approval_rejected` / `ratification_rejected` (редактирование + повторная отправка + архив).
- Отзыв (recall) обязателен: item / selected items / package целиком.
- Комментарий всегда опционален.

2. **Внедрения (Deployments)**
- Список/деталка/форма внедрения.
- Версионирование внедрения: изменения только через новую версию.
- ЖЦ внедрения: submit_for_approval → approve → (awaiting_ratification) → ratify → deploy/rollback.
- Блоки "Артефакты" (URL) и "Связанные сущности" (read-only) на деталке/формах.

3. **Пилоты (Pilots)**
- Адаптация существующего ЖЦ пилота под согласование/утверждение и работу с версиями (активная версия/не-active).
- Список/деталка пилота.
- Блоки "Артефакты" (URL) и "Связанные сущности" на create/edit/detail.

4. **Скоркарты (Scorecards)**
- Список/деталка/форма скоркарты (ScorecardVersion).
- Интеграция статуса скоркарты с Pilot/Deployment (см. `BE_SC_INT1`).
- Важно: артефакты к скоркарте не прикрепляются.

5. **Источники created_from**
- Автосоздание источников (`PilotSource`/`DeploymentSource`) при создании Pilot/Deployment на основе скоркарт.
- Preview источников в формах Pilot/Deployment по выбранным скоркартам (best-effort, не блокирует сохранение).

6. **Артефакты (Artifacts)**
- Артефакты как URL-ссылки: list/create/delete.
- Привязка только к `Simulation`/`Pilot`/`Deployment` (Initiative вне MVP).

7. **Симуляции (Simulations)**
- ЖЦ/approval не трогаем, но проверяем блоки:
  - "Артефакты" и "Связанные сущности" на detail/create/edit (create: disabled/empty, edit: работает).

8. **Уведомления и навигация**
- Email уведомления на ключевые события Approval/Ratification/Deploy/Rollback/Recall.
- Навигация/меню: доступность новых страниц.

### Key Scenarios (must-pass)

- PilotVersion: draft → submit_for_approval → approve → awaiting_ratification → ratify (индивидуально) → успешное завершение → activation (если применимо по ЖЦ).
- DeploymentVersion: draft → submit_for_approval → approve → awaiting_ratification → ratify через Package (2+ items) → deploy → rollback (опционально).
- Approve/Reject через пакет только выбранных items: выбранные получают решение, не выбранные остаются индивидуально в очереди.
- Reject на approval → `approval_rejected` → edit → resubmit → успешное завершение.
- Reject на ratification → `ratification_rejected` → edit → resubmit → успешное завершение.
- Recall на approval и на ratification: item, items в пакете, пакет целиком.
- Артефакты (URL) на Pilot/Deployment/Simulation: add/delete + права + валидация URL.
- Связанные сущности на Pilot/Deployment/Simulation: корректные связи "через скоркарты".
- Источники: sources auto-link → preview источников в формах.
- Scorecards: статус отображается в деталке; источники/использование отображаются.

### Acceptance Criteria

- [ ] Пройдены end-to-end сценарии Approval/Ratification (индивидуально и через Package)
- [ ] Пройдены сценарии reject/recall/resubmit
- [ ] Работают страницы "Согласования" и "Пакеты" (включая просмотр комментариев/истории и batch действия)
- [ ] Работают страницы Внедрений (list/detail/form/versions/ЖЦ)
- [ ] Работают страницы Пилотов (list/detail + блоки)
- [ ] Работают страницы Скоркарт (detail/form) + интеграция статуса (`BE_SC_INT1`)
- [ ] Работает автосоздание источников + preview источников в формах
- [ ] Артефакты (URL) работают на Simulation/Pilot/Deployment
- [ ] Проверена матрица прав/видимости (403 там, где нельзя)
- [ ] Уведомления (email) отправляются на ключевых событиях
- [ ] Критические баги исправлены (blocker/critical = 0)

### Dependencies

- Все задачи разработки MVP из Gantt v6.14 (backend + frontend), в частности:
  - `BE_AP1`, `BE_INT1`, `BE_PL1`, `BE_NOT1`
  - `BE_CL1`, `BE_C1`, `BE_CHD1`, `BE_CHF1`
  - `BE_SC_INT1`, `BE_SCD1`, `BE_SCF1`
  - `BE_CD1`
  - `BE_PA1`, `FE_PA1`, `FE_SA1`
  - `FE_APR1`, `FE_PKG1`, `FE_NAV1`

### Deliverables

- Отчет о тестировании (с чек-листом по ключевым сценариям)
- Список найденных багов с приоритетами

---

## Критический путь (по Ганту)

В `Gantt v6.14` QA стартует после завершения ключевых UI-веток (минимум `FE_NAV1` и `FE_SCF1`) и покрывает весь MVP.
