# QA задачи для Фазы 1: Approval/Ratification + Packages + Notifications

## QA-PHASE1: Тестирование Фазы 1

**Тип:** Story  
**Приоритет:** Высокий  
**Оценка:** 10 дней  

### Summary
Комплексное тестирование процесса согласования/утверждения (Approval/Ratification), страниц "Согласования"/"Пакеты" и уведомлений.

### Scope

1. **Approval/Ratification (core)**
- Submit на согласование для `PilotVersion` и `DeploymentVersion`.
- Мультистейдж approval (Approval stages): принять решение по assignment (approve/reject).
- Reject не возвращает в draft: `approval_rejected` / `ratification_rejected` (редактирование + повторная отправка + архив).
- Отзыв (recall) обязателен:
  - отзыв элемента индивидуально
  - отзыв элементов внутри пакета
  - отзыв пакета целиком
- Комментарий всегда опционален.

2. **Очередь утверждения и Packages**
- `auto_ratification=false`: после завершения approval элемент попадает в `awaiting_ratification` и может быть утвержден:
  - индивидуально
  - в составе Package (для группового утверждения)
- Минимальный размер Package: 2 элемента.
- Решение и комментарии хранятся **на item**, не на Package:
  - если решение принято через пакет, в item-history фиксируем префикс: `одобрено в составе пакета с комментарием: ...` (если комментарий был).
- Batch решения по пакету:
  - approve/reject пакета применимо ко всем выбранным (с галочками) items
  - не выбранные items остаются висеть в очереди утверждения как индивидуальные

3. **Страница "Согласования"** (`FE_APR1`)
- Списки задач согласования/утверждения для пользователя (packages + standalone).
- Просмотр комментариев/истории по item (и контекст пакета, если был).
- Действия approve/reject/ratify в зависимости от роли/этапа.
- Проверка ограничений прав (403 на запрещенные операции).

4. **Страница "Пакеты"** (`FE_PKG1`)
- Сбор 2+ элементов в пакет для группового утверждения.
- Показ полного состава пакета (включая read-only элементы других продуктов).
- Отправка на утверждение: выбор ratifier (если требуется).
- Отзыв: item / selected items / package.
- История: состав пакета + решения/комментарии по каждому item.

5. **Уведомления** (`BE_NOT1`)
- Email на ключевые события submit/approve/reject/recall/ratify.
- Проверка содержания уведомлений на соответствие контексту (item vs package).

### Key Scenarios (must-pass)

- PilotVersion: draft → submit_for_approval → approve → awaiting_ratification → ratify индивидуально → финальный статус.
- DeploymentVersion: draft → submit_for_approval → approve → awaiting_ratification → ratify через Package (2+ items).
- Approve/Reject через пакет только выбранных items: выбранные получают решение, не выбранные остаются индивидуально в очереди.
- Reject на approval → `approval_rejected` → edit → resubmit → успешное завершение.
- Reject на ratification → `ratification_rejected` → edit → resubmit → успешное завершение.
- Recall на approval и на ratification: item, items в пакете, пакет целиком.
- Комментарии:
  - опциональный комментарий на действиях
  - сохранение комментария в истории каждого item, включая "в составе пакета"
  - просмотр комментариев на страницах "Согласования" и "Пакеты"

### Acceptance Criteria

- [ ] Пройдены end-to-end сценарии Approval/Ratification (индивидуально и через Package)
- [ ] Пройдены сценарии reject/recall/resubmit
- [ ] История решений и просмотр комментариев работают (per item, включая "в составе пакета")
- [ ] Batch approve/reject по пакету работает только для выбранных items
- [ ] Не выбранные items корректно остаются индивидуально в очереди утверждения
- [ ] Проверена матрица прав/видимости (403 там, где нельзя)
- [ ] Уведомления (email) отправляются на ключевых событиях
- [ ] Критические баги исправлены (blocker/critical = 0)

### Dependencies

- `BE_AP1`, `BE_INT1`, `BE_NOT1`
- `BE_APR1`, `BE_PKG1`
- `FE_APR1`, `FE_PKG1`

### Deliverables

- Отчет о тестировании (с чек-листом по ключевым сценариям)
- Список найденных багов с приоритетами

---

## Критический путь (по Ганту)

`BE_NOT1` + `FE_APR1` + `FE_PKG1` → `QA_PHASE1`

