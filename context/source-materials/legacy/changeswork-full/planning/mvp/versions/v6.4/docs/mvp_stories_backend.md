# Backend Stories - Детальные описания

## BE-1: Миграция БД - Базовые таблицы

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 1

### Описание
Создание/обновление базовых таблиц БД для MVP. Необходимо создать схему данных для основных сущностей системы: Deployment, Simulation, Pilot, Change, Scorecard, таблицы источников для Lineage, Package.

### Технические требования
- PostgreSQL 14+
- Использовать миграции (Alembic/Django migrations)
- Все таблицы должны иметь поля: id (UUID), created_at, updated_at
- Foreign keys с ON DELETE CASCADE/RESTRICT согласно бизнес-логике
- Индексы на часто используемые поля (product_id, status, deployment_id)

### Acceptance Criteria
- [ ] Таблица `deployment` создана с полями: id, name, description, product_id, status (enum: draft/active/deployed/archived), created_at, updated_at, created_by
- [ ] Таблица `simulation` обновлена: добавлено поле deployment_id (NOT NULL, FK)
- [ ] Таблица `pilot` обновлена: добавлено поле deployment_id (NOT NULL, FK)
- [ ] Таблица `change` создана с полями: id, name, description, deployment_id, status (enum), priority (enum: low/medium/high/critical), planned_deployment_date, deployed_at, rolled_back_at, created_at, updated_at, created_by
- [ ] Таблица `scorecard` создана с полями: id, name, description, version, product_id, configuration (JSONB), created_at, updated_at, created_by
- [ ] Таблица `scorecard_source` создана для отслеживания источников: id, scorecard_id, source_type (enum: simulation/pilot), source_id
- [ ] Таблица `pilot_scorecard` создана для связи многие-ко-многим
- [ ] Таблица `change_scorecard` создана для связи многие-ко-многим
- [ ] Таблица `simulation_source` создана для отслеживания источников Симуляций: id, simulation_id, source_type ('pilot'), source_id
- [ ] Таблица `pilot_source` создана для отслеживания источников Пилотов: id, pilot_id, source_type ('simulation'), source_id
- [ ] Таблица `change_source` создана для отслеживания источников Изменений: id, change_id, source_type ('pilot'/'simulation'), source_id
- [ ] Таблица `package` создана с полями: id, name, description, created_at, created_by (БЕЗ полей status, priority)
- [ ] Таблица `package_item` создана с полями: id, package_id, item_type (enum: pilot/change), item_id, status (enum: pending/ratified/ratification_rejected), created_at
- [ ] Триггер для автоматического расчета статуса Deployment создан
- [ ] Все Foreign keys настроены корректно
- [ ] Индексы созданы: deployment(product_id, status), simulation(deployment_id), pilot(deployment_id), change(deployment_id, status), simulation_source(simulation_id), pilot_source(pilot_id), change_source(change_id), package_item(package_id, status)
- [ ] Миграция применяется без ошибок на чистой БД
- [ ] Rollback миграции работает корректно
- [ ] Документация по схеме БД обновлена

### Зависимости
Нет

### Технические заметки
```sql
-- Пример триггера для расчета статуса Deployment
CREATE OR REPLACE FUNCTION calculate_deployment_status()
RETURNS TRIGGER AS $$
BEGIN
  -- Логика расчета статуса
  -- draft: пустое ИЛИ все вложенные в draft
  -- active: хотя бы одна вложенная сущность не в draft
  -- deployed: хотя бы одно Deployment в deployed
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## BE-2: Миграция БД - Таблицы согласования

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 2 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 2

### Описание
Создание таблиц для процесса двухэтапного согласования с маршрутами. Система должна поддерживать настраиваемые маршруты согласования с двумя обязательными этапами: approval и ratification.

### Технические требования
- Фиксированные 2 этапа (constraint на уровне БД)
- Последовательное прохождение этапов
- История всех решений

### Acceptance Criteria
- [ ] Таблица `approval_route` создана с полями: id, name, product_id, created_at, updated_at, created_by
- [ ] Таблица `approval_stage` создана с полями: id, approval_route_id, stage_type (enum: approval/ratification), stage_order (1 или 2), created_at
- [ ] Constraint: для каждого approval_route должно быть ровно 2 stage (1 approval, 1 ratification)
- [ ] Таблица `approval_assignment` создана с полями: id, approval_stage_id, user_id, created_at
- [ ] Таблица `approval_instance` создана с полями: id, package_id (UNIQUE), approval_route_id, current_stage_id, status (enum: pending/approved/rejected), created_at, updated_at
- [ ] Таблица `approval_decision` создана с полями: id, approval_instance_id, approval_stage_id, user_id, decision (enum: approved/rejected), comment (TEXT), decided_at
- [ ] Foreign keys настроены с правильными ON DELETE правилами
- [ ] Индексы созданы: approval_instance(package_id, status), approval_decision(approval_instance_id, user_id)
- [ ] Constraint: нельзя создать approval_instance для package, у которого уже есть активный instance
- [ ] Миграция применяется без ошибок
- [ ] Rollback работает корректно
- [ ] Документация обновлена

### Зависимости
BE-1 (нужна таблица package)

### Технические заметки
```sql
-- Constraint для 2 этапов
ALTER TABLE approval_route
ADD CONSTRAINT check_two_stages
CHECK (
  (SELECT COUNT(*) FROM approval_stage WHERE approval_route_id = id) = 2
);
```

---

## BE-3: Миграция БД - Артефакты и роли

**Тип:** Task
**Приоритет:** High
**Оценка:** 2 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 2

### Описание
Создание таблиц для управления артефактами (документами) и ролевой модели пользователей. Артефакты могут быть прикреплены к Deployment и Change. Роли определяют права доступа пользователей.

### Технические требования
- Артефакты хранятся как URL ссылки
- Типы артефактов: business_case, rov, other
- Роли: ПРМ (с product_id), Методолог, Approver, Ratifier, Админ (без product_id для глобальных ролей)

### Acceptance Criteria
- [ ] Таблица `artifact` создана с полями: id, entity_type (enum: deployment/simulation/pilot/change), entity_id (UUID), name, url, type (enum: business_case/rov/other), uploaded_by (user_id), uploaded_at
- [ ] Индекс создан: artifact(entity_type, entity_id)
- [ ] Constraint: url должен начинаться с http:// или https://
- [ ] Таблица `user_role` создана с полями: id, user_id, role (enum: prm/methodologist/approver/ratifier/admin), product_id (nullable), created_at, created_by
- [ ] Constraint: если role = 'prm', то product_id NOT NULL
- [ ] Constraint: если role IN ('methodologist', 'approver', 'ratifier', 'admin'), то product_id IS NULL
- [ ] Unique constraint: (user_id, role, product_id) - один пользователь не может иметь одну и ту же роль дважды
- [ ] Индекс создан: user_role(user_id, role)
- [ ] Обновлена таблица `user` при необходимости (добавлены недостающие поля)
- [ ] Миграция применяется без ошибок
- [ ] Rollback работает корректно
- [ ] Документация обновлена

### Зависимости
BE-1 (нужны таблицы deployment, change)

### Технические заметки
```sql
-- Constraint для ролей
ALTER TABLE user_role
ADD CONSTRAINT check_prm_product
CHECK (
  (role = 'prm' AND product_id IS NOT NULL) OR
  (role IN ('methodologist', 'approver', 'admin') AND product_id IS NULL)
);
```

---

## BE-4: Модели данных (ORM)

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 1

### Описание
Создание/обновление ORM моделей для всех сущностей системы. Модели должны включать связи, валидацию и методы для бизнес-логики.

### Технические требования
- Django ORM / SQLAlchemy
- Type hints для всех полей
- Docstrings для всех классов и методов
- Unit тесты для методов моделей

### Acceptance Criteria
- [ ] Модель `Deployment` создана с полями и связями (simulations, pilots, changes, artifacts)
- [ ] Метод `calculate_status()` реализован для Deployment
- [ ] Модель `Simulation` обновлена (добавлено поле deployment)
- [ ] Модель `Pilot` обновлена (добавлено поле deployment, связь scorecards многие-ко-многим)
- [ ] Валидация: Pilot должен иметь минимум 1 scorecard
- [ ] Модель `Change` создана с полями и связями (deployment, scorecards многие-ко-многим, artifacts)
- [ ] Валидация: Change должен иметь минимум 1 scorecard
- [ ] Модель `Scorecard` создана с полями и связями (product, pilots, changes, sources)
- [ ] Модели источников для Lineage созданы: `SimulationSource`, `PilotSource`, `ChangeSource`
- [ ] Модель `Package` создана с полями и связями (approval_route, approval_instance)
- [ ] Модель `PackageItem` создана с полями (package, entity_type, entity_id, status)
- [ ] Метод `calculate_priority()` реализован для Package (MAX от PackageItem)
- [ ] Модель `ApprovalRoute` создана с полями и связями (product, stages, assignments)
- [ ] Модель `ApprovalStage` создана
- [ ] Модель `ApprovalAssignment` создана
- [ ] Модель `ApprovalInstance` создана с полями и связями (package, approval_route, decisions)
- [ ] Модель `ApprovalDecision` создана
- [ ] Модель `Artifact` создана с полями и связями
- [ ] Модель `UserRole` создана с полями и валидацией
- [ ] Все связи настроены с правильными related_name
- [ ] Unit тесты написаны для всех методов моделей (coverage > 90%)
- [ ] Docstrings добавлены для всех классов и методов
- [ ] Type hints добавлены для всех полей и методов

### Зависимости
BE-1, BE-2, BE-3

### Технические заметки
```python
class Initiative(models.Model):
    """Инициатива - верхнеуровневая группировка работы."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('User', on_delete=models.PROTECT)

    def calculate_status(self) -> str:
        """Рассчитывает статус на основе вложенных сущностей."""
        # Логика расчета
        pass
```

---

## BE-5: API Deployment (CRUD)

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 1

### User Story
Как ПРМ, я хочу создавать и управлять Deployment для своего продукта, чтобы группировать связанную работу по внедрению риск-стратегий.

### Описание
REST API для управления Deployment. API должен поддерживать создание, просмотр, обновление и удаление Deployment с учетом прав доступа.

### Технические требования
- Django REST Framework / FastAPI
- Пагинация: 20 элементов на страницу
- Фильтрация по product_id, status
- Сортировка по created_at, updated_at
- Права доступа: ПРМ видит только свой продукт, Админ видит все

### Acceptance Criteria
- [ ] POST /api/deployments/ - создание Deployment
  - Поля: name, description, product_id
  - Валидация: все поля обязательны
  - Статус автоматически устанавливается в 'draft'
  - created_by = текущий пользователь
  - Права: только ПРМ своего продукта или Админ
- [ ] GET /api/deployments/ - список Deployment
  - Фильтрация: ?product_id=X&status=Y
  - Сортировка: ?ordering=-created_at
  - Пагинация: page_size=20
  - Права: ПРМ видит только свой продукт, Админ видит все
  - Response включает: id, name, description, product, status, created_at, updated_at, created_by
- [ ] GET /api/deployments/{id}/ - детальный просмотр
  - Response включает все поля + вложенные сущности (simulations, pilots, changes, artifacts)
  - Статус рассчитывается автоматически при GET
  - Права: ПРМ своего продукта или Админ
- [ ] PATCH /api/deployments/{id}/ - обновление
  - Можно обновить: name, description
  - Нельзя обновить: product_id, status (рассчитывается автоматически)
  - Права: ПРМ своего продукта или Админ
- [ ] DELETE /api/deployments/{id}/ - удаление
  - Можно удалить только если status = 'draft'
  - Каскадное удаление вложенных сущностей
  - Права: ПРМ своего продукта или Админ
- [ ] Валидация входных данных реализована
- [ ] Обработка ошибок: 400 (валидация), 403 (права), 404 (не найдено)
- [ ] Unit тесты написаны (coverage > 80%)
- [ ] Integration тесты написаны (CRUD операции, права доступа)
- [ ] API документация добавлена (OpenAPI/Swagger)

### Зависимости
BE-4

### API Examples
```bash
# Создание
POST /api/deployments/
{
  "name": "Новая стратегия кредитования",
  "description": "Внедрение обновленной скоринговой модели",
  "product_id": "uuid-here"
}

# Список с фильтрацией
GET /api/deployments/?product_id=uuid&status=active&ordering=-created_at

# Детальный просмотр
GET /api/deployments/uuid/
```

---

## BE-6: API Simulation (адаптация)

**Тип:** Task
**Приоритет:** High
**Оценка:** 2 дня
**Спринт:** 2
**Исполнитель:** Backend Dev 1

### Описание
Адаптация существующего API Simulation под новую модель данных. Необходимо добавить обязательное поле deployment_id и валидацию принадлежности к одному продукту.

### Технические требования
- Сохранить существующую функциональность
- Добавить новые поля и валидацию
- Обновить тесты

### Acceptance Criteria
- [ ] POST /api/simulations/ обновлен: deployment_id обязательное поле
- [ ] Валидация: Simulation и Deployment должны быть в одном продукте
- [ ] GET /api/simulations/ обновлен: добавлена фильтрация по deployment_id
- [ ] GET /api/simulations/{id}/ обновлен: response включает deployment
- [ ] PATCH /api/simulations/{id}/ обновлен: нельзя изменить deployment_id после создания
- [ ] Существующие тесты обновлены
- [ ] Новые тесты для валидации deployment_id
- [ ] API документация обновлена

### Зависимости
BE-4, BE-5

---

## BE-7: API Pilot (адаптация)

**Тип:** Task
**Приоритет:** High
**Оценка:** 3 дня
**Спринт:** 2
**Исполнитель:** Backend Dev 1

### Описание
Адаптация существующего API Pilot под новую модель данных. Необходимо добавить deployment_id и связь со Scorecard (многие-ко-многим, минимум 1).

### Технические требования
- Сохранить существующую функциональность
- Добавить связь со Scorecard
- Валидация: минимум 1 scorecard

### Acceptance Criteria
- [ ] POST /api/pilots/ обновлен: deployment_id и scorecard_ids обязательны
- [ ] Валидация: минимум 1 scorecard
- [ ] Валидация: Pilot, Deployment и Scorecard в одном продукте
- [ ] GET /api/pilots/ обновлен: фильтрация по deployment_id и scorecard_id
- [ ] GET /api/pilots/{id}/ обновлен: response включает deployment и scorecards
- [ ] PATCH /api/pilots/{id}/ обновлен: можно изменить scorecards
- [ ] Нельзя изменить deployment_id после создания
- [ ] Существующие тесты обновлены
- [ ] Новые тесты для валидации
- [ ] API документация обновлена

### Зависимости
BE-4, BE-5, BE-8

---

## BE-8: API Scorecard (CRUD)

**Тип:** Story
**Приоритет:** High
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Backend Dev 2

### User Story
Как Методолог, я хочу создавать и управлять Scorecard, чтобы определять конфигурации скоринговых моделей для использования в Pilot и Change.

### Описание
REST API для управления Scorecard. Методолог создает и редактирует Scorecard, ПРМ может только просматривать.

### Acceptance Criteria
- [ ] POST /api/scorecards/ - создание
  - Поля: name, description, version, product_id, configuration (JSON), source_type (optional), source_id (optional)
  - Права: только Методолог или Админ
- [ ] GET /api/scorecards/ - список с фильтрацией (product_id, source_type)
  - Права: все роли
- [ ] GET /api/scorecards/{id}/ - детальный просмотр
  - Response включает: pilots, changes, source
  - Права: все роли
- [ ] PATCH /api/scorecards/{id}/ - обновление
  - Права: только Методолог или Админ
- [ ] DELETE /api/scorecards/{id}/ - удаление
  - Валидация: нельзя удалить, если используется в Pilot или Change
  - Права: только Методолог или Админ
- [ ] Unit и integration тесты (coverage > 80%)
- [ ] API документация

### Зависимости
BE-4

---

## BE-9: API Change (CRUD)

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 4 дня
**Спринт:** 2
**Исполнитель:** Backend Dev 1

### User Story
Как ПРМ, я хочу создавать и управлять Change для внедрения изменений в продуктовую среду, чтобы реализовывать утвержденные риск-стратегии.

### Описание
REST API для управления Deployment. Deployment представляет продуктовое внедрение модификации стратегии и должен быть связан минимум с одной Скоркартой.

### Технические требования
- Связь со Scorecard (многие-ко-многим, минимум 1)
- State machine для статусов: draft → requires_approval → approved → deployed → rolled_back
- Артефакты могут быть прикреплены к Deployment

### Acceptance Criteria
- [ ] POST /api/changes/ - создание Change
  - Поля: name, description, deployment_id, scorecard_ids (array, минимум 1), priority (enum), planned_deployment_date
  - Валидация: минимум 1 scorecard
  - Валидация: Change, Deployment и Scorecard в одном продукте
  - Статус автоматически 'draft'
  - Права: ПРМ своего продукта или Админ
- [ ] GET /api/changes/ - список с фильтрацией
  - Фильтры: deployment_id, status, priority
  - Сортировка: priority, planned_deployment_date, created_at
  - Пагинация: 20 элементов
  - Права: ПРМ видит только свой продукт, Админ видит все
- [ ] GET /api/changes/{id}/ - детальный просмотр
  - Response включает: все поля, deployment, scorecards, artifacts, approval_history
  - Права: ПРМ своего продукта или Админ
- [ ] PATCH /api/changes/{id}/ - обновление
  - Можно обновить: name, description, scorecards, priority, planned_deployment_date
  - Нельзя изменить: deployment_id, status (меняется через actions)
  - Права: ПРМ своего продукта или Админ
- [ ] POST /api/changes/{id}/submit/ - отправка на согласование
  - Переход статуса: draft → requires_approval
  - Валидация: Change должен иметь минимум 1 scorecard
  - Валидация: все обязательные поля заполнены
  - Права: ПРМ своего продукта или Админ
- [ ] DELETE /api/changes/{id}/ - удаление
  - Можно удалить только если status = 'draft'
  - Права: ПРМ своего продукта или Админ
- [ ] Переходы статусов согласно state machine реализованы
- [ ] Unit и integration тесты (coverage > 80%)
- [ ] API документация

### Зависимости
BE-4, BE-5, BE-8

### API Examples
```bash
POST /api/changes/
{
  "name": "Внедрение новой скоринговой модели",
  "description": "Обновление порогов одобрения",
  "deployment_id": "uuid",
  "scorecard_ids": ["uuid1", "uuid2"],
  "priority": "high",
  "planned_deployment_date": "2026-04-01"
}
```

---

## BE-10: API Lineage (GET only - визуализация)

**Тип:** Story
**Приоритет:** High
**Оценка:** 2 дня
**Спринт:** 2
**Исполнитель:** Backend Dev 2

### User Story
Как ПРМ, я хочу видеть визуализацию Lineage (происхождения) для Deployment или Change, чтобы понимать полный путь внедрения стратегии через Simulation → Pilot → Change.

### Описание
REST API для визуализации Lineage. Lineage НЕ является CRUD-сущностью - это визуализация связей "создано из", которые отслеживаются через таблицы источников (simulation_source, pilot_source, change_source) и Scorecards.

### Технические требования
- Только GET endpoints (НЕТ POST/PATCH/DELETE)
- Данные читаются из таблиц simulation_source, pilot_source, change_source
- Граф связей строится через Scorecards (многие-ко-многим)
- Backend автоматически создаёт записи в таблицах источников при создании Pilot/Deployment с указанием Scorecards

### Acceptance Criteria
- [ ] GET /api/lineage/?initiative_id={id} - получение Lineage для Initiative
  - Response: граф связей всех Simulation/Pilot/Deployment в Initiative
  - Формат удобен для визуализации (узлы и рёбра)
  - Права: ПРМ своего продукта или Админ
- [ ] GET /api/lineage/?change_id={id} - получение Lineage для конкретного Change
  - Response: граф связей для конкретного Change (его предки)
  - Права: ПРМ своего продукта или Админ
- [ ] Граф строится корректно через таблицы источников и Scorecards
- [ ] Unit и integration тесты (coverage > 80%)
- [ ] API документация

### Зависимости
BE-4, BE-5, BE-6, BE-7, BE-9

---

## BE-12: API Package (CRUD + Submit)

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 4 дня
**Спринт:** 3
**Исполнитель:** Backend Dev 1

### User Story
Как ПРМ, я хочу создать Package для группировки Pilot/Deployment и отправить их на утверждение (Ratification) одновременно, чтобы ускорить процесс утверждения.

### Описание
REST API для управления Package. Package создаётся ТОЛЬКО при отправке на утверждение (Ratification). НЕТ draft состояния - создание и отправка происходят одновременно. Package группирует Pilot/Deployment (не Chain) для совместного утверждения.

### Технические требования
- Package создаётся и отправляется на утверждение одновременно (один API call)
- Package НЕ имеет статусов - статусы принадлежат PackageItem
- Критичность Package = MAX(pilot/change.priority) - вычисляется на лету
- Package хранится навсегда для истории утверждения (аудит)

### Acceptance Criteria
- [ ] POST /api/packages/ - создание Package и отправка на утверждение
  - Поля: name, description, items (array of {type: 'pilot'/'deployment', id: UUID}), ratifier_id
  - Валидация: минимум 1 item
  - Валидация: все Pilot/Deployment из одного продукта
  - Создаёт Package, PackageItem (status: pending) и ApprovalInstance одновременно
  - priority вычисляется на лету (MAX от items)
  - Права: ПРМ своего продукта или Админ
- [ ] GET /api/packages/ - список с фильтрацией
  - Фильтры: priority, product_id
  - Сортировка: priority, created_at
  - Пагинация: 20 элементов
  - Права: ПРМ видит только свой продукт, Админ видит все
- [ ] GET /api/packages/{id}/ - детальный просмотр
  - Response включает: все поля, package_items (с индивидуальными статусами), approval_instance
  - priority вычисляется на лету
  - Права: ПРМ своего продукта или Админ
- [ ] Unit и integration тесты (coverage > 80%)
- [ ] API документация

### Зависимости
BE-4, BE-10, BE-11

---

## BE-13: Бизнес-логика согласования

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 5 дней
**Спринт:** 3
**Исполнитель:** Backend Dev 1

### User Story
Как Approver или Ratifier, я хочу согласовывать или отклонять Package на назначенных мне этапах, чтобы контролировать внедрение изменений в продуктовую среду.

### Описание
Реализация процесса двухэтапного согласования. Процесс должен последовательно проходить этапы approval → ratification с валидацией прав доступа.

### Технические требования
- Последовательное прохождение этапов
- Все согласующие/утверждающие этапа должны одобрить для перехода на следующий этап
- Если хотя бы один отклонил → Package отклонен
- История всех решений сохраняется

### Acceptance Criteria
- [ ] POST /api/packages/{id}/submit/ создает ApprovalInstance
  - ApprovalInstance.status = 'pending'
  - ApprovalInstance.current_stage_id = первый этап (approval)
  - Уведомления отправляются Approver первого этапа
- [ ] POST /api/approval-instances/{id}/approve/ - согласование/утверждение
  - Поля: comment (optional)
  - Валидация: только назначенный Approver/Ratifier текущего этапа может согласовать
  - Валидация: пользователь еще не принял решение
  - Создание ApprovalDecision с decision='approved'
  - Если все на этапе одобрили:
    - Если это последний этап → ApprovalInstance.status = 'approved', все Change в Package → 'approved'
    - Если не последний → переход на следующий этап, уведомления следующим
  - Права: только назначенный Approver/Ratifier
- [ ] POST /api/approval-instances/{id}/reject/ - отклонение
  - Поля: comment (required)
  - Валидация: только назначенный Approver/Ratifier текущего этапа
  - Валидация: пользователь еще не принял решение
  - Создание ApprovalDecision с decision='rejected'
  - ApprovalInstance.status = 'rejected'
  - Все Change в Package → статус не меняется (остаются 'requires_approval')
  - Уведомление отправляется создателю Package
  - Права: только назначенный Approver/Ratifier
- [ ] GET /api/approval-instances/ - список для Approver/Ratifier
  - Фильтры: status, current_stage
  - Показывает только те ApprovalInstance, где пользователь назначен
  - Права: Approver/Ratifier видят свои, Админ видит все
- [ ] GET /api/approval-instances/{id}/ - детальный просмотр
  - Response включает: package, approval_route, current_stage, decisions (история)
  - Права: создатель Package, назначенные Approver/Ratifier, Админ
- [ ] GET /api/approval-instances/{id}/history/ - история согласований
  - Response: все ApprovalDecision с user, decision, comment, decided_at
  - Права: создатель Package, назначенные Approver/Ratifier, Админ
- [ ] Обновление статусов Change при завершении согласования реализовано
- [ ] Unit тесты для всех сценариев (coverage > 90%)
- [ ] Integration тесты для полного процесса (submit → approve → approve → approved)
- [ ] API документация

### Зависимости
BE-4, BE-9, BE-11, BE-12

### Сценарии тестирования
1. Happy path: submit → все одобрили на approval → все одобрили на ratification → approved
2. Отклонение на первом этапе: submit → один отклонил на approval → rejected
3. Отклонение на втором этапе: submit → все одобрили на approval → один отклонил на ratification → rejected
4. Попытка согласовать не своим пользователем → 403
5. Попытка согласовать дважды → 400

---

## BE-14: API Artifact Links (управление ссылками)

**Тип:** Story
**Приоритет:** Medium
**Оценка:** 3 дня
**Спринт:** 2
**Исполнитель:** Backend Dev 2

### User Story
Как ПРМ, я хочу добавлять ссылки на внешние документы к Deployment, Simulation, Pilot и Change, чтобы хранить связанную документацию в одном месте.

### Описание
REST API для управления артефактами (ссылки на внешние документы). Артефакты могут быть прикреплены к Deployment, Simulation, Pilot и Change.

### Технические требования
- Артефакты хранятся как URL ссылки (НЕ загрузка файлов)
- Валидация формата URL
- Типы артефактов: business_case, rov, other
- Права доступа: ПРМ для своих, Методолог для всех

### Acceptance Criteria
- [ ] POST /api/artifacts/ - создание ссылки на документ
  - Content-Type: application/json
  - Поля: entity_type (enum: deployment/simulation/pilot/change), entity_id, name, url, type (enum: business_case/rov/other)
  - Валидация: формат URL (начинается с http:// или https://)
  - Метаданные сохраняются в БД
  - uploaded_by = текущий пользователь
  - Права: ПРМ для своих сущностей, Методолог для всех, Админ
- [ ] GET /api/artifacts/ - список с фильтрацией
  - Фильтры: entity_type, entity_id
  - Response: id, name, url, type, uploaded_by, uploaded_at
  - Права: ПРМ видит артефакты своих сущностей, Методолог видит все
- [ ] PATCH /api/artifacts/{id}/ - обновление ссылки
  - Поля: name, url, type
  - Валидация: формат URL
  - Права: только uploaded_by или Методолог или Админ
- [ ] DELETE /api/artifacts/{id}/ - удаление
  - Метаданные удаляются из БД
  - Права: только uploaded_by или Методолог или Админ
- [ ] Обработка ошибок: 400 (невалидный URL), 403 (права), 404 (не найдено)
- [ ] Unit и integration тесты (coverage > 80%)
- [ ] API документация

### Зависимости
BE-4

### Технические заметки
```python
# Пример валидации URL
from urllib.parse import urlparse

def validate_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False
```

---

## BE-16: Middleware для проверки прав доступа

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 3
**Исполнитель:** Backend Dev 2

### Описание
Реализация middleware/decorators для проверки прав доступа согласно ролевой модели. Middleware должен проверять роль пользователя и его права на конкретное действие.

### Технические требования
- Декораторы для проверки ролей
- Проверка принадлежности к продукту (для ПРМ)
- Матрица прав из CLAUDE.md должна быть реализована полностью

### Acceptance Criteria
- [ ] Middleware для аутентификации реализован
- [ ] Декоратор @require_role(roles=['prm', 'admin']) реализован
- [ ] Декоратор @require_product_access реализован для ПРМ
- [ ] Декоратор @require_owner_or_role реализован (владелец или определенная роль)
- [ ] Матрица прав доступа реализована:
  - ПРМ: CRUD своих Initiative/Simulation/Pilot/Deployment/Package, просмотр всех Scorecard
  - Методолог: CRUD всех Scorecard, управление артефактами всех сущностей, просмотр всех сущностей
  - Approver: просмотр назначенных Package на этапе Approval, согласование/отклонение
  - Ratifier: просмотр назначенных Package на этапе Ratification, утверждение/отклонение
  - Админ: полный доступ ко всем сущностям, управление ролями
- [ ] Корректные HTTP коды возвращаются:
  - 401 Unauthorized (не аутентифицирован)
  - 403 Forbidden (нет прав)
  - 404 Not Found (сущность не найдена или нет прав на просмотр)
- [ ] Декораторы применены ко всем endpoints
- [ ] Unit тесты для всех сценариев проверки прав (coverage > 90%)
- [ ] Integration тесты для разных ролей
- [ ] Документация по использованию декораторов

### Зависимости
BE-5 - BE-13

### Технические заметки
```python
from functools import wraps
from rest_framework.exceptions import PermissionDenied

def require_role(roles):
    """Декоратор для проверки роли пользователя."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_roles = request.user.roles.values_list('role', flat=True)
            if not any(role in roles for role in user_roles):
                raise PermissionDenied("У вас нет прав для этого действия")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_product_access(view_func):
    """Декоратор для проверки доступа ПРМ к продукту."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Логика проверки
        pass
    return wrapper
```

---

## BE-17: Integration тесты end-to-end

**Тип:** Task
**Приоритет:** High
**Оценка:** 4 дня
**Спринт:** 3-4
**Исполнитель:** Backend Dev 1, Backend Dev 2

### Описание
Написание integration тестов для полного сценария работы системы от создания Deployment до завершения процесса согласования.

### Технические требования
- Pytest / Django TestCase
- Тестовая БД
- Фикстуры для тестовых данных
- Coverage > 80% для критичных модулей

### Acceptance Criteria
- [ ] Тест: Happy path - полный цикл
  - Создание Initiative
  - Создание Simulation (связь с Initiative)
  - Создание Scorecard из Simulation
  - Создание Pilot (связь с Initiative и Scorecard)
  - Создание Deployment (связь с Initiative и Scorecard)
  - Визуализация Lineage (проверка связей через Scorecards)
  - Создание Package (группировка Pilot/Deployment)
  - Отправка Package на согласование (создание и отправка одновременно)
  - Согласование на этапе approval (все Approver)
  - Переход на этап ratification
  - Утверждение на этапе ratification (все Ratifier)
  - Проверка: Deployment в статусе 'approved'
- [ ] Тест: Отклонение на первом этапе
  - Создание Package и отправка на согласование
  - Один Approver отклоняет на этапе approval
  - Проверка: Package в статусе 'rejected'
  - Проверка: Deployment остается в 'requires_approval'
- [ ] Тест: Отклонение на втором этапе
  - Прохождение первого этапа
  - Отклонение на этапе ratification
  - Проверка: Package в статусе 'rejected'
- [ ] Тест: Права доступа ПРМ
  - ПРМ создает Deployment своего продукта - успех
  - ПРМ пытается создать Deployment чужого продукта - 403
  - ПРМ видит только свои Deployment - проверка фильтрации
  - ПРМ пытается согласовать Package - 403 (если не назначен)
- [ ] Тест: Права доступа Методолога
  - Методолог создает Scorecard - успех
  - Методолог видит все Scorecard всех продуктов
  - Методолог управляет артефактами всех сущностей
  - ПРМ пытается создать Scorecard - 403
- [ ] Тест: Права доступа Approver/Ratifier
  - Approver видит только назначенные ему Package на этапе Approval
  - Approver согласовывает назначенный Package на этапе Approval - успех
  - Approver пытается согласовать Package на этапе Ratification - 403
  - Ratifier видит только назначенные ему Package на этапе Ratification
  - Ratifier утверждает назначенный Package на этапе Ratification - успех
  - Ratifier пытается согласовать Package на этапе Approval - 403
- [ ] Тест: Валидация бизнес-правил
  - Нельзя создать Package с Pilot/Deployment с разными ApprovalRoute - 400
  - Нельзя удалить Scorecard, используемую в Pilot - 400
  - Нельзя удалить ApprovalRoute, используемый в Package - 400
  - Pilot должен иметь минимум 1 Scorecard - 400
  - Deployment должен иметь минимум 1 Scorecard - 400
- [ ] Тест: Артефакты
  - Добавление ссылки на документ к Deployment - успех
  - Добавление ссылки с невалидным URL - 400
  - Обновление ссылки владельцем - успех
  - Удаление ссылки владельцем - успех
  - Удаление ссылки не владельцем - 403
  - ПРМ управляет артефактами своих сущностей - успех
  - Методолог управляет артефактами всех сущностей - успех
- [ ] Coverage отчет сгенерирован (coverage > 80%)
- [ ] Тесты запускаются автоматически в CI/CD
- [ ] Документация по запуску тестов

### Зависимости
BE-5 - BE-13

### Технические заметки
```python
# Пример integration теста
def test_full_approval_flow():
    # Setup
    prm_user = create_user_with_role('prm', product_id=product.id)
    approver1 = create_user_with_role('approver')
    ratifier1 = create_user_with_role('ratifier')

    # Create entities
    deployment = create_deployment(prm_user, product)
    simulation = create_simulation(prm_user, deployment)
    scorecard = create_scorecard_from_simulation(simulation)
    pilot = create_pilot(prm_user, deployment, [scorecard])
    change = create_change(prm_user, deployment, [scorecard])

    # Create approval route
    route = create_approval_route(product, [
        {'stage': 'approval', 'assignees': [approver1]},
        {'stage': 'ratification', 'assignees': [ratifier1]}
    ])

    # Create and submit package (одновременно)
    package = create_and_submit_package(prm_user, [pilot, change], route, ratifier1)

    # Approve on first stage
    approve_instance(approver1, package.approval_instance)

    # Ratify on second stage
    approve_instance(ratifier1, package.approval_instance)

    # Assert
    assert package.approval_instance.status == 'approved'
    assert change.status == 'approved'
```

---

## BE-18: API документация и Postman коллекция

**Тип:** Task
**Приоритет:** Medium
**Оценка:** 2 дня
**Спринт:** 4
**Исполнитель:** Backend Dev 1

### Описание
Финализация API документации и создание Postman коллекции с примерами запросов для всех endpoints.

### Технические требования
- OpenAPI 3.0 спецификация
- Swagger UI для интерактивной документации
- Postman коллекция с примерами
- README с описанием API

### Acceptance Criteria
- [ ] OpenAPI спецификация сгенерирована для всех endpoints
- [ ] Swagger UI доступен по адресу /api/docs/
- [ ] Все endpoints задокументированы с:
  - Описанием
  - Параметрами (path, query, body)
  - Примерами запросов
  - Примерами ответов (success и error)
  - Кодами ответов (200, 201, 400, 403, 404, 500)
- [ ] Postman коллекция создана с:
  - Папками по сущностям (Deployment, Simulation, Pilot, Change, etc.)
  - Примерами запросов для всех endpoints
  - Environment variables (baseUrl, authToken)
  - Pre-request scripts для аутентификации
  - Tests для проверки ответов
- [ ] Postman коллекция экспортирована в JSON
- [ ] README.md создан с:
  - Обзором API
  - Инструкцией по аутентификации
  - Примерами curl команд
  - Описанием ролевой модели
  - Ссылкой на Swagger UI
  - Инструкцией по импорту Postman коллекции
- [ ] Примеры curl команд для основных операций
- [ ] Документация актуальна и соответствует реализации

### Зависимости
BE-5 - BE-13

### Примеры документации

#### README.md структура
```markdown
# Risk Strategy Deployment System API

## Обзор
REST API для управления внедрениями риск-стратегий.

## Аутентификация
Bearer token в заголовке Authorization.

## Endpoints

### Deployments
- GET /api/deployments/ - список
- POST /api/deployments/ - создание
- GET /api/deployments/{id}/ - детальный просмотр
- PATCH /api/deployments/{id}/ - обновление
- DELETE /api/deployments/{id}/ - удаление

### Примеры curl
...

## Ролевая модель
...

## Swagger UI
http://localhost:8000/api/docs/

## Postman коллекция
Импортируйте файл `postman_collection.json`
```

---

## Итого Backend: 18 задач, 54 дня

**Критический путь:**
BE-1 → BE-4 → BE-5 → BE-9 → BE-10 → BE-12 → BE-13 → BE-17

**Ключевые задачи:**
- BE-1, BE-2, BE-3: Миграции БД (фундамент)
- BE-4: ORM модели (критично для всех API)
- BE-13: Бизнес-логика согласования (самая сложная часть)
- BE-16: Middleware прав доступа (безопасность)
- BE-17: Integration тесты (качество)

**Распределение:**
- Backend Dev 1: 27 дней (основной поток - сущности и согласование)
- Backend Dev 2: 27 дней (поддержка - артефакты, роли, тестирование)
