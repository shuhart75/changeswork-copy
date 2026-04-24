# Задачи для детальной страницы "Внедрение" (Deployment Detail)

## Обзор страницы

**Страница:** Детальный просмотр внедрения (Deployment Detail View)
**Путь в макете:** Клик на строку в списке внедрений → детальный просмотр
**Статус:** Абсолютно новая страница

### Упрощение для MVP:
**УДАЛЕНА вкладка "Обзор"** — процесс согласования/утверждения будет реализован позже.

### Что показывает страница (из макета, после упрощения):

**Header (шапка страницы):**
- Кнопка "Назад к списку"
- ID внедрения (DEP-XXX)
- Название внедрения
- Описание
- Статус (с автоматическим расчетом и tooltip с причиной)
- Кнопки действий:
  - "Редактировать"
  - "Удалить" (только для draft)
  - "Архивировать" (для всех кроме draft, недоступно если есть deployed изменения)
- Метаданные:
  - Продукт
  - Автор
  - Дата создания
  - Дата обновления

**Вкладки (после удаления "Обзор"):**

1. **Вкладка "Симуляции":**
   - Кнопка "Новая симуляция"
   - Список симуляций с карточками:
     - Checkbox (только для completed симуляций)
     - ID (SIM-XXX), название (кликабельное)
     - Режим симуляции, статус, этап, дата обновления этапа
     - Автор, дата создания
     - Результаты симуляции (AR, Объём выдач, NPV, RC) — только для completed
     - Связи с пилотами и изменениями (чипы)
   - Кнопки для выбранных симуляций:
     - "Создать пилот из выбранных"
     - "Создать изменение из выбранных"
   - Inline форма создания симуляции

2. **Вкладка "Пилоты":**
   - Кнопка "Новый пилот"
   - Список пилотов с карточками:
     - Checkbox (только для completed пилотов)
     - ID (PLT-XXX), название (кликабельное)
     - Код пилота, режим, измерение, статус пилота
     - Статус разметки, эксклюзивность
     - Планируемые даты активации/выключения
     - Связанные скоркарты (блок с чипами)
     - Связи с симуляциями и изменениями (чипы)
   - Кнопка для выбранных пилотов:
     - "Создать изменение из выбранных"
   - Inline форма создания пилота

3. **Вкладка "Изменения":**
   - Кнопка "Новое изменение"
   - Список изменений с карточками:
     - ID (CHG-XXX), название (кликабельное)
     - Статус, создал, создано, развернуто
     - Количество скоркарт
     - Связанные скоркарты (блок с чипами)
     - Связи с симуляциями и пилотами (чипы)
   - Inline форма создания изменения

4. **Вкладка "Скоркарты":**
   - Список скоркарт продукта с карточками:
     - ID (SC-XXX), название (кликабельное)
     - Критичность, статус, источник, версия, дата создания
     - Финансовые эффекты (AR, Объём выдач, NPV, RC)
     - Использование в пилотах и изменениях (чипы)

**Функционал:**
- Навигация между вкладками
- Клик на связанные сущности → переход к их детальному просмотру
- Создание новых сущностей через inline формы
- Выбор completed симуляций/пилотов для создания следующих сущностей
- Редактирование внедрения
- Удаление/архивирование внедрения

**Права доступа:**
- ПРМ может редактировать/удалять/архивировать только свои внедрения
- Методолог может просматривать все, но не может редактировать внедрения
- Админ может всё

---

## AN-DD1: Аналитика детальной страницы "Внедрение"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Детализация требований и проектирование UI/UX для детальной страницы внедрения с вкладками для связанных сущностей (без вкладки "Обзор")

### Description

Провести аналитику и детализацию требований для детальной страницы внедрения:

1. **Детализация бизнес-требований:**
   - Уточнить правила отображения статуса (автоматический расчет)
   - Определить правила удаления внедрения (только draft)
   - Определить правила архивирования (нельзя если есть deployed изменения)
   - Уточнить логику выбора симуляций/пилотов (только completed)
   - Определить правила создания сущностей из выбранных
   - Уточнить правила доступа для разных ролей

2. **Спецификация UI/UX:**
   - Wireframe детальной страницы с header и вкладками
   - Спецификация карточек для каждого типа сущности
   - Дизайн inline форм создания
   - Спецификация чипов для связей между сущностями
   - Спецификация блоков результатов и финансовых эффектов
   - Адаптивность (desktop/tablet/mobile)

3. **Спецификация API контрактов:**
   - GET /api/deployments/{id}/ - детальная информация
   - GET /api/deployments/{id}/simulations/ - список симуляций
   - GET /api/deployments/{id}/pilots/ - список пилотов
   - GET /api/deployments/{id}/changes/ - список изменений
   - GET /api/deployments/{id}/scorecards/ - список скоркарт продукта
   - PUT /api/deployments/{id}/ - редактирование
   - DELETE /api/deployments/{id}/ - удаление
   - POST /api/deployments/{id}/archive/ - архивирование
   - Коды ошибок (403, 404, 409, 500)

4. **Определение структуры данных:**
   - Формат ответа для детальной информации
   - Формат списков связанных сущностей
   - Формат результатов симуляций
   - Формат финансовых эффектов скоркарт
   - Формат связей между сущностями

5. **Правила валидации:**
   - Нельзя удалить внедрение если status != draft
   - Нельзя архивировать если есть deployed изменения
   - Можно выбрать только completed симуляции/пилоты
   - Минимум одна симуляция/пилот для создания следующей сущности

6. **Inline формы:**
   - Форма создания симуляции (название, описание, режим)
   - Форма создания пилота (название, код, режим, измерение, даты, скоркарты)
   - Форма создания изменения (название, описание, скоркарты)

### Acceptance Criteria

- [ ] Бизнес-требования задокументированы и согласованы
- [ ] Wireframe страницы готов (Figma/Sketch или описание)
- [ ] API контракты задокументированы (OpenAPI спецификация или описание)
- [ ] Определена структура данных для всех вкладок
- [ ] Правила автоматического расчета статуса описаны
- [ ] Правила удаления и архивирования описаны
- [ ] Правила выбора и создания сущностей описаны
- [ ] Права доступа для ролей определены
- [ ] Правила валидации описаны
- [ ] Спецификация inline форм готова
- [ ] Адаптивность для разных разрешений учтена
- [ ] Документ согласован с заказчиком

### Dependencies
- AN-D1 (требуется понимание базовой структуры Deployment)
- AN-S1 (требуется понимание структуры Simulation)
- AN-P1 (требуется понимание структуры Pilot)
- AN-C1 (требуется понимание структуры Change)

### Deliverables
- Документ "Спецификация детальной страницы Внедрение" (markdown/confluence)
- API контракты для всех endpoint'ов
- Wireframe или описание UI для всех вкладок
- Спецификация inline форм

---

## BE-DD1: Backend для детальной страницы "Внедрение"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 4 дня

### Summary
Реализация API endpoints для детальной страницы внедрения с получением связанных сущностей, редактированием, удалением и архивированием

### Description

Реализовать Backend API для детальной страницы внедрения:

1. **API Endpoint: GET /api/deployments/{id}/**

   **Формат ответа:**
   ```json
   {
     "id": "uuid",
     "display_id": "DEP-001",
     "name": "Оптимизация риск-стратегии Premium карт",
     "description": "Полное описание внедрения...",
     "product": {
       "id": "credit_cards",
       "label": "Кредитные карты"
     },
     "status": "active",
     "status_calculated": true,
     "status_reason": "Есть активные пилоты",
     "created_at": "2026-03-01T10:00:00Z",
     "updated_at": "2026-03-05T14:30:00Z",
     "created_by": {
       "id": "user-uuid",
       "full_name": "Иван Иванов"
     }
   }
   ```

2. **API Endpoint: GET /api/deployments/{id}/simulations/**

   **Формат ответа:**
   ```json
   {
     "count": 5,
     "results": [
       {
         "id": "uuid",
         "display_id": "SIM-001",
         "name": "Симуляция оптимизации лимитов",
         "mode": "standard",
         "status": "completed",
         "current_stage": "Завершено",
         "stage_updated_at": "2026-03-05T14:30:00Z",
         "created_at": "2026-03-01T10:00:00Z",
         "created_by": {
           "id": "user-uuid",
           "full_name": "Иван Иванов"
         },
         "results": {
           "ar": "+0.5%",
           "volume": "+10M",
           "npv": "+50M",
           "rc": "0.8%"
         },
         "pilot_ids": ["uuid1", "uuid2"],
         "change_ids": ["uuid3"]
       }
     ]
   }
   ```

3. **API Endpoint: GET /api/deployments/{id}/pilots/**

   **Формат ответа:**
   ```json
   {
     "count": 3,
     "results": [
       {
         "id": "uuid",
         "display_id": "PLT-001",
         "code": "PLT-PREMIUM-001",
         "name": "Пилот оптимизации лимитов Premium карт",
         "mode": "ab_test",
         "measurement": "clients",
         "exclusive": false,
         "status": "completed",
         "markup_status": true,
         "planned_start_at": "2026-03-10T00:00:00Z",
         "planned_end_at": "2026-04-10T00:00:00Z",
         "scorecards": [
           {
             "id": "uuid",
             "display_id": "SC-001",
             "name": "Скоркарта Premium v2.0"
           }
         ],
         "simulation_ids": ["uuid1"],
         "change_ids": ["uuid2"]
       }
     ]
   }
   ```

4. **API Endpoint: GET /api/deployments/{id}/changes/**

   **Формат ответа:**
   ```json
   {
     "count": 2,
     "results": [
       {
         "id": "uuid",
         "display_id": "CHG-001",
         "name": "Внедрение оптимизированных лимитов Premium карт",
         "status": "deployed",
         "deployed_at": "2026-03-05T10:00:00Z",
         "created_at": "2026-03-01T10:00:00Z",
         "created_by": {
           "id": "user-uuid",
           "full_name": "Иван Иванов"
         },
         "scorecards_count": 2,
         "scorecards": [
           {
             "id": "uuid",
             "display_id": "SC-001",
             "name": "Скоркарта Premium v2.0"
           }
         ],
         "simulation_ids": ["uuid1"],
         "pilot_ids": ["uuid2"]
       }
     ]
   }
   ```

5. **API Endpoint: GET /api/deployments/{id}/scorecards/**

   **Формат ответа:**
   ```json
   {
     "count": 10,
     "results": [
       {
         "id": "uuid",
         "display_id": "SC-001",
         "name": "Скоркарта Premium v2.0",
         "criticality": "high",
         "status": "active",
         "version": "2.0",
         "created_at": "2026-03-01T10:00:00Z",
         "sources": [
           {
             "type": "simulation",
             "id": "uuid"
           }
         ],
         "financial_effects": {
           "ar": "+0.5%",
           "volume": "+10M",
           "npv": "+50M",
           "rc": "0.8%"
         },
         "used_in_pilots": [
           {
             "id": "uuid",
             "display_id": "PLT-001",
             "name": "Пилот оптимизации лимитов"
           }
         ],
         "used_in_changes": [
           {
             "id": "uuid",
             "display_id": "CHG-001",
             "name": "Внедрение оптимизированных лимитов"
           }
         ]
       }
     ]
   }
   ```


6. **API Endpoint: PUT /api/deployments/{id}/**

   **Тело запроса:**
   ```json
   {
     "name": "Обновленное название",
     "description": "Обновленное описание"
   }
   ```

   **Формат ответа:** Обновленный объект Deployment

7. **API Endpoint: DELETE /api/deployments/{id}/**

   **Валидация:**
   - Только для status = draft
   - HTTP 409 если status != draft

8. **API Endpoint: POST /api/deployments/{id}/archive/**

   **Валидация:**
   - Нельзя архивировать если есть deployed изменения
   - HTTP 409 если есть deployed изменения
   - Устанавливает status = archived для Deployment и всех вложенных сущностей

9. **Бизнес-логика:**
   - Автоматический расчет статуса Deployment:
     - draft: пустое ИЛИ все вложенные в draft
     - active: хотя бы одна вложенная сущность не в draft
     - deployed: хотя бы одно Внедрение в deployed
   - Фильтрация связанных сущностей по deployment_id
   - Права доступа:
     - ПРМ может редактировать/удалять/архивировать только свои внедрения
     - Методолог может только просматривать
     - Админ может всё

10. **Оптимизация:**
    - Select related для product и created_by
    - Prefetch related для simulations, pilots, changes, scorecards
    - Annotate для счетчиков
    - Кэширование списка скоркарт продукта

### Acceptance Criteria

- [ ] GET /api/deployments/{id}/ endpoint реализован
- [ ] GET /api/deployments/{id}/simulations/ endpoint реализован
- [ ] GET /api/deployments/{id}/pilots/ endpoint реализован
- [ ] GET /api/deployments/{id}/changes/ endpoint реализован
- [ ] GET /api/deployments/{id}/scorecards/ endpoint реализован
- [ ] PUT /api/deployments/{id}/ endpoint реализован
- [ ] DELETE /api/deployments/{id}/ endpoint реализован
- [ ] POST /api/deployments/{id}/archive/ endpoint реализован
- [ ] Автоматический расчет статуса реализован
- [ ] Валидация удаления (только draft) реализована
- [ ] Валидация архивирования (нет deployed изменений) реализована
- [ ] Права доступа реализованы (ПРМ только свои, методолог read-only)
- [ ] HTTP 403 возвращается при попытке редактирования чужого внедрения
- [ ] HTTP 409 возвращается при нарушении бизнес-правил
- [ ] Select related/prefetch оптимизация применена
- [ ] Связи между сущностями корректно возвращаются
- [ ] Результаты симуляций включены в ответ
- [ ] Финансовые эффекты скоркарт включены в ответ
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для прав доступа
- [ ] API документация обновлена (Swagger/OpenAPI)
- [ ] Postman коллекция с примерами запросов

### Dependencies
- AN-DD1 (требуется API контракт)
- BE-D1 (базовый endpoint для Deployment)
- BE-S1 (таблица simulation должна существовать)
- BE-P1 (таблица pilot должна существовать)
- BE-C1 (таблица change должна существовать)
- BE-1 (все таблицы должны быть готовы)
- BE-4 (ORM модели должны быть готовы)

### Technical Notes

**Пример автоматического расчета статуса:**
```python
def calculate_status(self):
    simulations = self.simulations.all()
    pilots = self.pilots.all()
    changes = self.changes.all()

    # Если есть deployed изменения
    if changes.filter(status='deployed').exists():
        return 'deployed', 'Есть внедренные изменения'

    # Если есть хотя бы одна не-draft сущность
    if (simulations.exclude(status='draft').exists() or
        pilots.exclude(status='draft').exists() or
        changes.exclude(status='draft').exists()):
        return 'active', 'Есть активные сущности'

    # Иначе draft
    return 'draft', 'Все сущности в черновике'
```

**Пример валидации удаления:**
```python
def delete(self, request, pk=None):
    deployment = self.get_object()
    if deployment.status != 'draft':
        return Response(
            {'error': 'Можно удалить только черновики'},
            status=status.HTTP_409_CONFLICT
        )
    deployment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
```

**Пример валидации архивирования:**
```python
@action(detail=True, methods=['post'])
def archive(self, request, pk=None):
    deployment = self.get_object()

    # Проверка на deployed изменения
    if deployment.changes.filter(status='deployed', rollback_at__isnull=True).exists():
        return Response(
            {'error': 'Нельзя архивировать внедрение с активными deployed изменениями'},
            status=status.HTTP_409_CONFLICT
        )

    # Архивирование всех вложенных сущностей
    deployment.status = 'archived'
    deployment.save()

    deployment.simulations.update(status='archived')
    deployment.pilots.update(status='archived')
    deployment.changes.update(status='archived')

    return Response({'status': 'archived'})
```

---

## FE-DD1: Frontend для детальной страницы "Внедрение"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 10 дней

### Summary
Реализация UI детальной страницы внедрения с вкладками, карточками связанных сущностей, inline формами и навигацией

### Description

Реализовать Frontend для детальной страницы внедрения:

1. **Компонент DeploymentDetailView:**
   - Header с информацией о внедрении
   - Кнопка "Назад к списку"
   - Статус с tooltip (автоматический расчет)
   - Кнопки действий (Редактировать, Удалить/Архивировать)
   - Метаданные (продукт, автор, даты)
   - Tabs для навигации между вкладками
   - Responsive дизайн

2. **Вкладка "Симуляции" (SimulationsTab):**
   - Кнопка "Новая симуляция"
   - Список карточек симуляций:
     - Checkbox (только для completed)
     - ID, название (кликабельное)
     - Режим, статус, этап, дата обновления этапа
     - Автор, дата создания
     - Результаты (AR, Объём выдач, NPV, RC) — только для completed
     - Чипы связей с пилотами и изменениями
   - Кнопки для выбранных:
     - "Создать пилот из выбранных"
     - "Создать изменение из выбранных"
   - Inline форма CreateSimulationFormInline
   - Empty state если нет симуляций

3. **Вкладка "Пилоты" (PilotsTab):**
   - Кнопка "Новый пилот"
   - Список карточек пилотов:
     - Checkbox (только для completed)
     - ID, название (кликабельное)
     - Код, режим, измерение, статус
     - Статус разметки, эксклюзивность
     - Планируемые даты
     - Блок связанных скоркарт (EntityScorecardBlock)
     - Чипы связей с симуляциями и изменениями
   - Кнопка для выбранных:
     - "Создать изменение из выбранных"
   - Inline форма CreatePilotFormInline
   - Empty state если нет пилотов

4. **Вкладка "Изменения" (ChangesTab):**
   - Кнопка "Новое изменение"
   - Список карточек изменений:
     - ID, название (кликабельное)
     - Статус, создал, создано, развернуто
     - Количество скоркарт
     - Блок связанных скоркарт (EntityScorecardBlock)
     - Чипы связей с симуляциями и пилотами
   - Inline форма CreateChangeFormInline
   - Empty state если нет изменений

5. **Вкладка "Скоркарты" (ScorecardsTab):**
   - Список карточек скоркарт:
     - ID, название (кликабельное)
     - Критичность, статус, источник, версия, дата создания
     - Финансовые эффекты (AR, Объём выдач, NPV, RC)
     - Использование в пилотах и изменениях (чипы)
   - Empty state если нет скоркарт

6. **Компоненты для связей:**
   - EntityScorecardBlock — блок с чипами скоркарт (с ограничением maxItems)
   - Chip для связей с другими сущностями (кликабельные)
   - Блоки результатов симуляций (4 карточки с метриками)
   - Блоки финансовых эффектов (4 карточки с метриками)

7. **Inline формы:**
   - CreateSimulationFormInline (название, описание, режим)
   - CreatePilotFormInline (название, код, режим, измерение, даты, выбор скоркарт)
   - CreateChangeFormInline (название, описание, выбор скоркарт)
   - Кнопки "Сохранить" и "Отмена"

8. **Действия:**
   - Редактирование внедрения (открывает форму)
   - Удаление (только draft, с подтверждением)
   - Архивирование (с проверкой deployed изменений, с подтверждением)
   - Создание сущностей через inline формы
   - Выбор completed симуляций/пилотов
   - Создание пилота/изменения из выбранных

9. **Навигация:**
   - Клик на название сущности → переход к детальному просмотру
   - Клик на чип связи → переход к связанной сущности
   - Breadcrumbs: "Внедрения" → "DEP-XXX"

10. **Loading и Error состояния:**
    - Skeleton loader при загрузке
    - Error message при ошибке API
    - Empty state для каждой вкладки
    - Toast уведомления при действиях

11. **API интеграция:**
    - DeploymentService.getDetail(id)
    - DeploymentService.getSimulations(id)
    - DeploymentService.getPilots(id)
    - DeploymentService.getChanges(id)
    - DeploymentService.getScorecards(id)
    - DeploymentService.update(id, data)
    - DeploymentService.delete(id)
    - DeploymentService.archive(id)
    - Обработка ошибок (403, 404, 409, 500)

### Acceptance Criteria

- [ ] DeploymentDetailView компонент реализован
- [ ] Header отображает всю информацию корректно
- [ ] Статус с tooltip работает
- [ ] Кнопки действий работают (Редактировать, Удалить, Архивировать)
- [ ] Tabs навигация работает
- [ ] Вкладка "Симуляции" реализована
- [ ] Вкладка "Пилоты" реализована
- [ ] Вкладка "Изменения" реализована
- [ ] Вкладка "Скоркарты" реализована
- [ ] Карточки симуляций отображаются корректно
- [ ] Карточки пилотов отображаются корректно
- [ ] Карточки изменений отображаются корректно
- [ ] Карточки скоркарт отображаются корректно
- [ ] Checkbox работает (только для completed)
- [ ] Кнопки "Создать из выбранных" работают
- [ ] Inline формы работают
- [ ] EntityScorecardBlock компонент работает
- [ ] Чипы связей кликабельные и работают
- [ ] Блоки результатов симуляций отображаются
- [ ] Блоки финансовых эффектов отображаются
- [ ] Навигация к связанным сущностям работает
- [ ] Breadcrumbs отображается корректно
- [ ] Удаление работает (только draft, с подтверждением)
- [ ] Архивирование работает (с проверкой, с подтверждением)
- [ ] Loading состояние (skeleton) работает
- [ ] Error состояние отображается
- [ ] Empty state для каждой вкладки работает
- [ ] Responsive дизайн работает (desktop/tablet/mobile)
- [ ] API интеграция работает корректно
- [ ] Обработка ошибок реализована (403, 404, 409)
- [ ] Toast уведомления при действиях
- [ ] Unit тесты для компонентов (coverage > 70%)
- [ ] TypeScript типы определены

### Dependencies
- AN-DD1 (требуется UI спецификация)
- BE-DD1 (требуется готовый API)
- FE-D1 (требуется базовый DeploymentsView)
- FE-S1 (требуется SimulationService)
- FE-P1 (требуется PilotService)
- FE-C1 (требуется ChangeService)
- FE-1 (базовая структура проекта)
- FE-2 (UI Kit компоненты: Tabs, Chip, Checkbox, Tooltip)
- FE-3 (DeploymentService)
- FE-4 (AuthContext для проверки прав)

### Technical Notes

**Пример структуры компонента:**
```typescript
interface DeploymentDetailViewProps {
  deploymentId: string;
  onBack: () => void;
}

function DeploymentDetailView({ deploymentId, onBack }: DeploymentDetailViewProps) {
  const [deployment, setDeployment] = useState<Deployment | null>(null);
  const [activeTab, setActiveTab] = useState(0);
  const [simulations, setSimulations] = useState<Simulation[]>([]);
  const [pilots, setPilots] = useState<Pilot[]>([]);
  const [changes, setChanges] = useState<Change[]>([]);
  const [scorecards, setScorecards] = useState<Scorecard[]>([]);
  const [selectedSimulations, setSelectedSimulations] = useState<string[]>([]);
  const [selectedPilots, setSelectedPilots] = useState<string[]>([]);
  const [showCreateSimulation, setShowCreateSimulation] = useState(false);
  const [showCreatePilot, setShowCreatePilot] = useState(false);
  const [showCreateChange, setShowCreateChange] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDeploymentDetail();
  }, [deploymentId]);

  useEffect(() => {
    if (activeTab === 0) fetchSimulations();
    if (activeTab === 1) fetchPilots();
    if (activeTab === 2) fetchChanges();
    if (activeTab === 3) fetchScorecards();
  }, [activeTab]);

  const handleDelete = async () => {
    if (deployment.status !== 'draft') {
      showToast('Можно удалить только черновики', 'error');
      return;
    }

    const confirmed = await showConfirmDialog({
      title: 'Удалить внедрение?',
      message: 'Это действие нельзя отменить.',
      confirmText: 'Удалить',
      cancelText: 'Отмена'
    });

    if (confirmed) {
      try {
        await DeploymentService.delete(deploymentId);
        showToast('Внедрение удалено', 'success');
        onBack();
      } catch (error) {
        showToast('Ошибка при удалении', 'error');
      }
    }
  };

  const handleArchive = async () => {
    const confirmed = await showConfirmDialog({
      title: 'Архивировать внедрение?',
      message: 'Все связанные сущности также будут архивированы.',
      confirmText: 'Архивировать',
      cancelText: 'Отмена'
    });

    if (confirmed) {
      try {
        await DeploymentService.archive(deploymentId);
        showToast('Внедрение архивировано', 'success');
        fetchDeploymentDetail();
      } catch (error) {
        if (error.status === 409) {
          showToast('Нельзя архивировать внедрение с deployed изменениями', 'error');
        } else {
          showToast('Ошибка при архивировании', 'error');
        }
      }
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      {/* Header */}
      {/* Tabs */}
      {/* Tab content */}
    </Box>
  );
}
```

**EntityScorecardBlock компонент:**
```typescript
interface EntityScorecardBlockProps {
  entity: Simulation | Pilot | Change;
  maxItems?: number;
  onSelectScorecard: (scorecard: Scorecard) => void;
}

function EntityScorecardBlock({ entity, maxItems = 3, onSelectScorecard }: EntityScorecardBlockProps) {
  const scorecards = entity.scorecards || [];
  const displayScorecards = scorecards.slice(0, maxItems);
  const remaining = scorecards.length - maxItems;

  return (
    <Box sx={{ mt: 1 }}>
      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 0.5 }}>
        Скоркарты:
      </Typography>
      <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
        {displayScorecards.map(sc => (
          <Chip
            key={sc.id}
            label={`${sc.display_id}: ${sc.name}`}
            size="small"
            onClick={() => onSelectScorecard(sc)}
            sx={{
              bgcolor: '#f5f5f5',
              cursor: 'pointer',
              '&:hover': { bgcolor: '#e0e0e0' }
            }}
          />
        ))}
        {remaining > 0 && (
          <Chip
            label={`+${remaining} ещё`}
            size="small"
            sx={{ bgcolor: '#f5f5f5' }}
          />
        )}
      </Stack>
    </Box>
  );
}
```

---

## Итоговая зависимость задач

```
AN-DD1 (3 дня) ← зависит от AN-D1, AN-S1, AN-P1, AN-C1
  ↓
BE-DD1 (4 дня) ← зависит от BE-D1, BE-S1, BE-P1, BE-C1, BE-1, BE-4
  ↓
FE-DD1 (5 дней) ← зависит от FE-D1, FE-S1, FE-P1, FE-C1, FE-1, FE-2, FE-3, FE-4
```

**Общая длительность (критический путь):** 12 дней

**Параллельная работа:**
- BE-DD1 может начаться сразу после AN-DD1
- FE-DD1 может начаться только после готовности BE-DD1 (нужен работающий API)

---

## ✅ Ключевые особенности детальной страницы

1. **Удалена вкладка "Обзор":** Процесс согласования/утверждения будет реализован позже
2. **Четыре вкладки:** Симуляции, Пилоты, Изменения, Скоркарты
3. **Карточки вместо таблиц:** Более детальное представление с метаданными
4. **Inline формы:** Создание сущностей без перехода на другую страницу
5. **Выбор completed сущностей:** Для создания следующих в цепочке
6. **Связи между сущностями:** Чипы для навигации
7. **Результаты и эффекты:** Блоки с метриками для симуляций и скоркарт
8. **Автоматический статус:** С tooltip объяснением
9. **Валидация действий:** Удаление только draft, архивирование с проверкой
10. **Сложный UI:** Требует 5 дней на фронтенд (с запасом)
