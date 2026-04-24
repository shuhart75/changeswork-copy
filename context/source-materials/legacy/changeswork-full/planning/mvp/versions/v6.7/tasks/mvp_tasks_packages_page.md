# Задачи для страницы "Пакеты" (Packages View)

## Обзор страницы

**Страница:** Пакеты (Packages View)
**Путь в макете:** Боковое меню → "Пакеты"
**Статус:** Новая разработка

### Что показывает страница (из макета):

**4 вкладки:**
1. **Ожидают утверждения** - PilotVersion/DeploymentVersion с флагом `awaiting_ratification=true` (готовы к формированию Package)
2. **На согласовании/утверждении** - PilotVersion/DeploymentVersion/Package с активным `ApprovalInstance` (текущий этап Approval или Ratification)
3. **Отклонено** - элементы, отклоненные на согласовании/утверждении:
   - PilotVersion/DeploymentVersion со статусом `approval_rejected|ratification_rejected`
   - items пакета со статусом `package_item.status=ratification_rejected`
4. **История** - список Package и завершенных ApprovalInstance (аудит)

**Функционал:**
- Checkbox для выбора элементов (batch операции)
- Кнопка "Отправить на утверждение" для выбранных элементов:
  - если выбран 1 элемент: запуск индивидуальной ratification (без Package)
  - если выбрано 2+ элементов: создание Package и запуск ratification
- Кнопка "Отозвать (N)" для элементов в процессе
- Диалог выбора маршрута утверждения (RatificationRouteDialog)
- Диалог предпросмотра брифа уведомления (BriefPreviewDialog)
- Отображение EntityScorecardBlock для каждого элемента
- Отображение информации об утверждающем (назначен/не назначен)
- Просмотр комментариев/истории решений:
  - в истории Package: состав пакета + комментарии/решения по каждому item
  - в истории каждого item: событие решения в составе Package (с ссылкой на Package и комментарием)
- Клик на элемент → переход к детальному просмотру

**Права доступа:**
- ПРМ видит элементы по всем продуктам, но редактировать/отправлять на согласование/утверждение может только элементы своего продукта.
- Методолог видит все элементы и может формировать Package/запускать ratification (если есть доступ).
- Админ видит все элементы.

**Особенности:**
- Package группирует PilotVersion/DeploymentVersion для совместного утверждения (Ratification)
- Package **не имеет статусов** (статусы на `package_item`: `pending`/`ratified`/`ratification_rejected`/`recalled`/`released`)
- Для MVP: `package_item` также может быть отозван автором/админом: `pending -> recalled` (item возвращается в `awaiting_ratification`)
- Комментарии сохраняются **по каждому item отдельно** (в истории `PackageItemDecision`), даже если ratifier жмёт "одобрить всё".
- Критичность Package = MAX(item.priority) среди всех PilotVersion/DeploymentVersion (вычисляется на лету)
- Batch отправка на утверждение (множественный выбор)
- Email уведомления с предпросмотром брифа

---

## AN-PKG1: Аналитика страницы "Пакеты"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 7 дней

### Summary
Детализация требований для разработки страницы Пакеты (очередь `awaiting_ratification`, создание Package, индивидуальная ratification, recall, история) и batch операций.

### Description

Провести аналитику для разработки страницы Пакеты:

1. **Детализация бизнес-требований:**
   - Определить правила отбора PilotVersion/DeploymentVersion в `awaiting_ratification`
   - Уточнить логику формирования Package (создание без draft, сразу на ratification)
   - Определить правила расчета критичности Package
   - Уточнить логику batch отправки на утверждение
   - Определить правила отзыва с согласования
   - Уточнить формат email уведомлений

2. **Спецификация UI/UX:**
   - Разработка 4 вкладок (Требуют утверждения, На согласовании, Отклонено, История)
   - Дизайн checkbox для batch выбора
   - Спецификация диалога выбора маршрута утверждения
   - Спецификация диалога предпросмотра брифа
   - Дизайн email шаблона уведомления

3. **Спецификация API контракта:**
   - GET /api/ratification-queue/ - список PilotVersion/DeploymentVersion в `awaiting_ratification`
   - POST /api/ratification/start/ - запуск индивидуальной ratification по элементам очереди (без Package)
   - POST /api/packages/ - создание Package из выбранных items + запуск ratification (включая выбор ratifier)
   - POST /api/approval-instances/{id}/recall/ - отзыв из согласования (если поддерживаем в MVP)
   - GET /api/packages/ - история Package (аудит)
   - Параметры запроса (bucket, page, page_size, filters)
   - Коды ошибок (403, 404, 500)

4. **Определение полей для отображения:**
   - Элементы: PilotVersion/DeploymentVersion (ID, название, статус, скоркарты)
   - Утверждающий: назначен/не назначен
   - Причина отклонения (для отклоненных)
   - История: дата, действие, пользователь, причина
   - Комментарии/решения:
     - последний комментарий (если есть)
     - drill-down в историю решений по item и по Package (PackageItemDecision)

5. **Определение маршрута утверждения:**
   - Выбор утверждающего (ratifier)
   - Предпросмотр брифа уведомления

### Acceptance Criteria

- [ ] Бизнес-требования задокументированы
- [ ] API контракт задокументирован
- [ ] Определены все поля для отображения
- [ ] Правила формирования Package описаны
- [ ] Правила batch операций описаны
- [ ] Формат email уведомлений определен
- [ ] Права доступа для ролей определены
- [ ] Правила отображения истории решений (PackageItemDecision) описаны
- [ ] Документ согласован с заказчиком

### Dependencies
Нет

### Deliverables
- Документ "Спецификация страницы Пакеты" (markdown/confluence)
- API контракт для GET /api/packages/, POST /api/packages/submit_for_ratification/, POST /api/packages/recall/
- Шаблон email уведомления

---

## BE-PKG1: Backend для страницы "Пакеты"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 7 дней

### Summary
Разработка Backend для страницы Пакеты (очередь awaiting_ratification, создание Package, индивидуальная ratification, recall, история) с batch операциями и email уведомлениями.

### Description

Разработать Backend для страницы Пакеты:

1. **API Endpoint: GET /api/packages/**

   **Параметры запроса:**
   - `bucket` (optional) - фильтр по "корзине" (awaiting_ratification/in_progress/rejected/history)
   - `page` (optional, default=1) - номер страницы
   - `page_size` (optional, default=20) - размер страницы

	   **Формат ответа:**
	   ```json
	   {
	     "count": 42,
	     "next": "http://api/packages/?page=2",
	     "previous": null,
	     "results": [
	       {
	         "id": "uuid",
	         "type": "pilot_version",
	         "display_id": "PLT-001",
	         "name": "Пилот Premium Q1 2026",
	         "awaiting_ratification": true,
	         "product": {
	           "id": "credit_cards",
	           "name": "Кредитные карты"
	         },
	         "scorecards": [
	           {
	             "id": "uuid",
	             "display_id": "SC-001",
	             "name": "Скоркарта Premium v2.0",
	             "criticality": "high"
	           }
	         ],
	         "ratifier": null,
	         "created_at": "2026-03-01T10:00:00Z"
	       }
	     ]
	   }
	   ```

2. **API Endpoint: POST /api/packages/submit_for_ratification/**

   **Параметры запроса:**
   ```json
   {
     "items": [
       {"type": "pilot_version", "id": "uuid"},
       {"type": "deployment_version", "id": "uuid"}
     ],
     "ratifier_id": "user-uuid"
   }
   ```

   **Бизнес-логика:**
   - Валидация MVP: выбрано минимум 2 элемента (минимальный размер пакета = 2)
   - Валидация: все элементы в `awaiting_ratification=true`
   - Создание Package + PackageItem
   - Запуск ratification через `ApprovalInstance(target_type='package')`
   - Отправка уведомлений ratifier

3. **API Endpoint: POST /api/packages/recall/**

   **Параметры запроса:**
   ```json
   {
     "items": [
       {"type": "pilot_version", "id": "uuid"},
       {"type": "deployment_version", "id": "uuid"}
     ],
     "reason": "Требуется доработка"
   }
   ```

   **Поведение:**
   - Если item находится в `awaiting_ratification=true`: просто снимаем отправку на ratification (остаётся в очереди)
   - Если item находится в активном Package (ratification in_progress): переводим `package_item.status -> recalled` и возвращаем item в `awaiting_ratification`

4. **API Endpoint: POST /api/packages/{id}/recall/** (отзыв Package целиком)
   - Отменяет активный `ApprovalInstance(target_type='package')` и возвращает все items пакета в `awaiting_ratification`

5. **API Endpoint: GET /api/packages/history/**
   - Response должен включать состав Package и комментарии/решения по каждому item (история `PackageItemDecision`), а также ссылку на `ApprovalInstance` пакета (если есть).

   **Параметры запроса:**
   - `page` (optional, default=1) - номер страницы
   - `page_size` (optional, default=20) - размер страницы

6. **Бизнес-логика Package:**

   **БП-1: Формирование Package**
   - Package группирует PilotVersion/DeploymentVersion для совместного ratification
   - Элементы могут быть из разных Deployment (это допустимо)
   - В MVP v6.6 считаем минимально обязательным выбор одного `ratifier` на Package
   - Критичность Package = MAX(criticality) всех элементов (вычисляется на лету)
   - Package это "обертка удобства": одно письмо/одна кнопка для ratifier, при этом решения сохраняются по каждому item.
   - Ratifier может принять решение по всем item сразу или по каждому item отдельно (итоговый статус хранится по item).
   - Recalled items исключаются из проверки "Package обработан" и из batch-действий ratifier.
   - Items со статусом `released` "выпадают" из пакета и становятся индивидуальными элементами для ratification (для того же ratifier).

   **БП-2: Batch отправка на утверждение**
   - Валидация: все элементы находятся в `awaiting_ratification=true`
   - Создание Package + PackageItem
   - Создание `ApprovalInstance(target_type='package')` (ratification)
   - Отправка уведомлений (см. `BE-NOT1`)

   **БП-3: Индивидуальная ratification из очереди**
   - Пользователь выбирает один PilotVersion/DeploymentVersion в `awaiting_ratification=true`
   - Выбирает ratifier (ровно 1, роль Ratifier)
   - Запускает ratification индивидуально (создается `ApprovalInstance` ratification-only для target)
   - Уведомляется выбранный ratifier

7. **Email уведомления:**

   **Шаблон уведомления:**
   - Тема: "Направлено на утверждение: N элемент(ов)"
   - Тело: список элементов (ID, название, статус)
   - Кнопка "Перейти к согласованию" (ссылка на систему)
   - Подпись: "Система управления изменениями риск-стратегий"

8. **Права доступа:**
   - Отправить на утверждение может:
     - ПРМ (только элементы своего продукта),
     - Методолог,
     - Админ
   - Утвердить/отклонить может: только назначенный ratifier
   - Отозвать может: автор, Админ

### Acceptance Criteria

- [ ] GET /api/packages/ endpoint реализован
- [ ] Фильтр `bucket` работает (awaiting_ratification/in_progress/rejected/history)
- [ ] POST /api/packages/submit_for_ratification/ endpoint реализован
- [ ] Batch отправка на утверждение работает
- [ ] POST /api/packages/recall/ endpoint реализован
- [ ] POST /api/packages/{id}/recall/ endpoint реализован (отзыв пакета целиком)
- [ ] GET /api/packages/history/ endpoint реализован
- [ ] Email уведомления отправляются
- [ ] Права доступа реализованы
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] API документация обновлена

### Dependencies
- BE-AP1 (требуется процесс согласования)
- BE-INT1 (требуется интеграция ЖЦ)

---

## FE-PKG1: Frontend для страницы "Пакеты"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 8 дней

### Summary
Разработка UI страницы Пакеты с 4 вкладками, batch операциями, историей решений и диалогами (ratifier + brief preview).

### Description

Разработать Frontend для страницы Пакеты:

1. **Компонент PackagesView:**
   - 4 вкладки: Ожидают утверждения, На согласовании/утверждении, Отклонено, История
   - Responsive дизайн

2. **Вкладка "Ожидают утверждения":**
   - Отображение Pilot и Deployment с `awaiting_ratification=true`
   - Checkbox для каждого элемента (batch выбор)
   - Кнопка "Отправить на утверждение" (активна при выборе):
     - если выбран 1 элемент: запуск индивидуальной ratification (без Package)
     - если выбрано 2+ элементов: создание Package и запуск ratification
   - Отображение EntityScorecardBlock для каждого элемента
   - Отображение информации об утверждающем (назначен/не назначен)
   - Клик на элемент → переход к детальному просмотру

3. **Вкладка "На согласовании/утверждении":**
   - Отображение элементов с активным `ApprovalInstance` (текущий этап Approval или Ratification)
   - Checkbox для каждого элемента
   - Кнопка "Отозвать (N)" (активна при выборе)
   - Отображение EntityScorecardBlock
   - Отображение информации об утверждающем

4. **Вкладка "Отклонено":**
   - Отображение элементов, отклоненных на согласовании/утверждении:
     - PilotVersion/DeploymentVersion со статусом `approval_rejected|ratification_rejected`
     - items пакета со статусом `package_item.status=ratification_rejected`
   - Отображение причины отклонения
   - Отображение этапа отклонения (согласование/утверждение)
   - Клик на элемент → переход к детальному просмотру

5. **Вкладка "История согласований/утверждений":**
   - Список всех согласований (одобрено/отклонено)
   - Дата, действие, пользователь, причина (для отклоненных)
   - Для Package: состав пакета + комментарии/решения по каждому item (PackageItemDecision)
   - Пагинация

6. **Диалог выбора маршрута утверждения (RatificationRouteDialog):**
   - Открывается при клике "Отправить на утверждение"
   - Отображение количества выбранных элементов
   - Dropdown выбора утверждающего (ratifier)
   - Список утверждающих: ФИО, роль
   - Кнопка "Далее: Предпросмотр брифа"
   - Валидация: утверждающий должен быть выбран
   - Если выбран 1 элемент: диалог запускает индивидуальную ratification
   - Если выбрано 2+ элементов: диалог создаёт Package и запускает ratification

7. **Диалог предпросмотра брифа (BriefPreviewDialog):**
   - Открывается после выбора утверждающего
   - Предпросмотр email уведомления
   - Шапка: логотип Сбербанк, зеленый фон
   - Тело: приветствие, список элементов (таблица), кнопка "Перейти к согласованию"
   - Подпись: "Система управления изменениями риск-стратегий", дата
   - Футер: "Это автоматическое уведомление"
   - Кнопка "Отправить" (отправка на утверждение)

8. **EntityScorecardBlock:**
   - Отображение связанных скоркарт (до 2 шт)
   - Клик на скоркарту → переход к детальному просмотру скоркарты
   - Если больше 2 → "+N еще"

9. **Loading и Error состояния:**
    - Skeleton loader при загрузке
    - Error message при ошибке API
    - Empty state если нет данных

10. **API интеграция:**
    - PackageService.getList(filters, page, pageSize)
    - PackageService.submitForRatification(items, ratifierId)
    - PackageService.recall(items, reason)
    - PackageService.getHistory(filters, page, pageSize)
    - Обработка ошибок (403, 404, 500)
    - Toast уведомления при ошибках

11. **Просмотр комментариев (обязательно):**
   - В списках показывать последний комментарий (если есть)
   - В истории/деталке показывать:
     - историю PackageItemDecision для Package/items
     - историю ApprovalInstance/ApprovalDecision для индивидуальных процессов


### Acceptance Criteria

- [ ] PackagesView компонент реализован
- [ ] 4 вкладки работают корректно
- [ ] Checkbox для batch выбора работает
- [ ] Кнопка "Отправить на утверждение" работает
- [ ] Кнопка "Отозвать" работает
- [ ] RatificationRouteDialog реализован
- [ ] Dropdown выбора утверждающего работает
- [ ] BriefPreviewDialog реализован
- [ ] Предпросмотр email корректный
- [ ] Отправка на утверждение работает
- [ ] EntityScorecardBlock отображается корректно
- [ ] Информация об утверждающем отображается
- [ ] Причина отклонения отображается (для отклоненных)
- [ ] История согласований отображается
- [ ] Клик на элемент открывает детальный просмотр
- [ ] Клик на скоркарту открывает детальный просмотр скоркарты
- [ ] Loading состояние (skeleton) работает
- [ ] Error состояние отображается
- [ ] Empty state отображается если нет данных
- [ ] Responsive дизайн работает
- [ ] API интеграция работает корректно
- [ ] Обработка ошибок реализована
- [ ] Unit тесты для компонента (coverage > 70%)

### Dependencies
- AN-PKG1 (требуется UI спецификация)
- BE-PKG1 (требуется готовый API endpoint)

---

## Итоговая зависимость задач

```
AN-PKG1 (7 дней)
  ↓
BE-PKG1 (7 дней)
  ↓
FE-PKG1 (8 дней)
```

**Общая длительность (критический путь):** 22 дня

**Параллельная работа:**
- BE-PKG1 может начаться сразу после AN-PKG1
- FE-PKG1 может начаться только после готовности BE-PKG1

---

## ✅ Ключевые особенности страницы

1. **Новая разработка** - сложная страница с множеством функционала
2. **4 вкладки** - Требуют утверждения, На согласовании, Отклонено, История
4. **Batch операции** - множественный выбор и отправка
5. **Диалог выбора маршрута** - RatificationRouteDialog
6. **Диалог предпросмотра брифа** - BriefPreviewDialog с email шаблоном
7. **EntityScorecardBlock** - отображение связанных скоркарт
8. **Email уведомления** - с предпросмотром перед отправкой
9. **Информация об утверждающем** - назначен/не назначен
10. **История согласований** - полный лог всех действий
11. **Права доступа** - отображаем только доступные пользователю элементы
12. **Responsive дизайн** - адаптация под разные разрешения

---
