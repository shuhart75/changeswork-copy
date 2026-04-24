# Системные требования — Роли и RBAC (MVP)

Статус: **для передачи команде**
Область: MVP
Дата обновления: 2026-03-15

## 1) Цель и границы задачи

### 1.1 Цель
Система должна реализовать **минимально достаточную ролевую модель (RBAC)** для MVP, обеспечивающую:
- корректную **видимость** сущностей (кто что видит)
- корректные **права действий** (кто что может делать)
- поддержку **product-scoped** роли ПРМ (PRM) и **глобальных** ролей
- поддержку **множественных ролей** пользователя

### 1.2 Входит в MVP
- Роли: `prm`, `methodologist`, `approver`, `ratifier`, `admin`
- Привязка ролей к пользователям
- Для роли `prm`: обязательная привязка к `productId`
- Базовые правила видимости и прав (см. раздел 3)
- Проверки ролей при:
  - CRUD ключевых сущностей (Simulation/Pilot/Deployment/Scorecard и др. в рамках MVP)
  - операциях согласования/утверждения (Approval/Ratification)
  - CRUD артефактов (наследование прав от родителя)

### 1.3 Не входит в MVP
- Иерархические роли, ABAC, policy engine
- UI для администрирования пользователей/ролей (если отсутствует) — допускается seed/ручное администрирование
- История изменений ролей (event sourcing)

---

## 2) Определения

### 2.1 Роль пользователя (UserRole)
Запись о назначении роли пользователю.

### 2.2 Product-scoped роль
Роль, действие которой ограничено конкретным продуктом. В MVP это **только `prm`**.

---

## 3) Роли и правила доступа (MVP)

Источник: `spec/domain_model.md` и `final-spec/CLAUDE.md`.

### 3.1 Роли
- **PRM (`prm`)** — Product Risk Manager. Управляет инициативами и сущностями своего продукта.
- **Methodologist (`methodologist`)** — методолог. Управляет скоркартами и документами.
- **Approver (`approver`)** — согласующий на этапах Approval.
- **Ratifier (`ratifier`)** — утверждающий на этапе Ratification.
- **Admin (`admin`)** — полный доступ.

### 3.2 Множественные роли
- Пользователь может иметь **несколько ролей одновременно**.
- Совмещение:
  - PRM и Methodologist **могут быть** назначены Approver и/или Ratifier.
  - (Уточнение из spec): запрещено совмещать PRM + Methodologist в одном аккаунте.

### 3.3 Product scoping
- Для ролей `prm` и `methodologist`: `productId` обязателен (product-scoped роли).
- Для ролей `approver|ratifier|admin`: `productId` = `NULL` (глобальные роли).

### 3.4 Матрица прав (концептуально, MVP)

| Действие | PRM | Methodologist | Approver | Ratifier | Admin |
|---|---:|---:|---:|---:|---:|
| Просмотр Simulation/Pilot/Deployment | ✓ (все продукты) | ✓ (все продукты) | ✓ | ✓ | ✓ |
| Создание/редактирование Simulation/Pilot/Deployment | ✓ (свой продукт) | ✗ | ✗ | ✗ | ✓ |
| Просмотр Scorecard | ✓ (все продукты) | ✓ (все продукты) | ✓ | ✓ | ✓ |
| CRUD Scorecard | ✓ (свой продукт) | ✓ (свой продукт) | ✗ | ✗ | ✓ |
| Просмотр/CRUD артефактов | ✓ (своих сущностей) | ✓ (своих сущностей) | ✗ | ✗ | ✓ |
| Работа в разделе «Отправка на утверждение» | ✓ (свой продукт) | ✓ (свой продукт) | ✗ | ✗ | ✓ |
| Просмотр раздела «Согласования» | ✓ (свои/назначенные) | ✓ (свои/назначенные) | ✓ (назначенные) | ✓ (назначенные) | ✓ (все) |
| Решение на этапах Approval | ✓ (если назначен) | ✓ (если назначен) | ✓ | ✗ | ✓ |
| Решение на этапе Ratification | ✓ (если назначен) | ✓ (если назначен) | ✗ | ✓ | ✓ |

**Пояснения:**
- **PRM**: видит сущности (Simulation/Pilot/Deployment/Scorecard) по всем продуктам, но создавать/редактировать может только в своём продукте
- **Methodologist**: видит сущности (Simulation/Pilot/Deployment/Scorecard) по всем продуктам, но создавать/редактировать Scorecard может только в своём продукте
- **Approver/Ratifier**: видят все сущности (включая Scorecard), но не имеют прав на CRUD
- **Раздел «Отправка на утверждение»**: место для формирования Package (групповое утверждение). Доступ:
  - PRM: может работать только с элементами своего продукта
  - Methodologist: может работать только с элементами своего продукта
  - Approver/Ratifier: нет доступа к формированию Package (только к принятию решений в разделе «Согласования»)

### 3.5 Инварианты и правила
- Пользователь **не может назначить самого себя** в approvers/ratifier при отправке на согласование.
- При отправке на согласование:
  - approver’ами можно выбрать только пользователей, имеющих роль `approver`
  - ratifier’ом можно выбрать только пользователя, имеющего роль `ratifier`
- Право на CRUD артефактов наследуется от родительской сущности.

---

## 4) Backend (БД + API)

> **ВАЖНО:** В системе уже существует модуль управления ролями `rscon-sudir` с готовым API.
> В MVP мы **только читаем** информацию о пользователях и их ролях. Управление ролями (создание, назначение) выполняется backend-командой через внутренние инструменты.

### 4.1 Интеграция с существующим API rscon-sudir

Система уже имеет:
- Таблицы: `users`, `roles`, `user_roles` (many-to-many), `role_space_mapping` (роль → продукт), `incompatible_roles` (несовместимые роли)
- Endpoint `GET /api/v1/user?employeeNumber=X` для получения информации о пользователе
- Endpoint `GET /api/v1/access` для проверки прав
- Поле `access_type` в таблице `roles` с существующими значениями: ADMIN, EDITOR, METODOLOG, VIEWER, AUDITOR
- Механизм предотвращения несовместимых комбинаций ролей через таблицу `incompatible_roles`

**Как работает product scoping в sudir:**
- Таблица `role_space_mapping` связывает `role_id` с `space_code` (код продукта)
- Одна роль может быть привязана к нескольким продуктам (many-to-many)
- В API ответе `permittedSpaces[]` — это агрегация всех `space_code` из `role_space_mapping` для всех ролей пользователя

**Как работают несовместимые роли:**
- Таблица `incompatible_roles` содержит пары несовместимых ролей: `(role_a, role_b)`
- При попытке назначить пользователю роль, система проверяет, нет ли у него уже несовместимой роли
- Это предотвращает нарушение принципа разделения обязанностей (например, PRM + Methodologist)

### 4.2 Маппинг ролей MVP на существующий API

| Роль MVP | access_type (существующий) | Product scoping | Примечание |
|---|---|---|---|
| `prm` | `EDITOR` | Да (через role_space_mapping) | Уже существует |
| `methodologist` | `METODOLOG` | Да (через role_space_mapping) | Уже существует; product-scoped роль |
| `approver` | `APPROVER` | Нет | **НОВАЯ** — добавить в access_type |
| `ratifier` | `RATIFIER` | Нет | **НОВАЯ** — добавить в access_type |
| `admin` | `ADMIN` | Нет | Уже существует |

**Как работает product scoping:**
- Для ролей с `access_type=EDITOR` (prm) и `access_type=METODOLOG` (methodologist): в таблице `role_space_mapping` создаются записи `(role_id, space_code)`
- Одна роль может быть привязана к нескольким продуктам через несколько записей в `role_space_mapping`
- В API ответе `permittedSpaces[]` — это агрегация всех `space_code` для всех ролей пользователя

### 4.3 Минимальные изменения в rscon-sudir

**Что нужно сделать backend-команде rscon-sudir:**

1. **Добавить новые значения в поле `access_type` таблицы `roles`:**
   - `APPROVER`
   - `RATIFIER`

   (Если `access_type` реализован как enum на уровне БД — расширить enum; если varchar с проверкой — обновить constraint)

2. **Создать записи в таблице `roles`** (через миграции/SQL):
   ```sql
   INSERT INTO roles (id, role_name, access_type, archive)
   VALUES
     ('approver', 'Согласующий', 'APPROVER', false),
     ('ratifier', 'Утверждающий', 'RATIFIER', false);
   ```

3. **Настроить несовместимые роли в таблице `incompatible_roles`:**

   Согласно требованиям MVP, роли PRM (EDITOR) и Methodologist (METODOLOG) несовместимы.

   ```sql
   -- Для каждой роли EDITOR (prm) добавить несовместимость с metodolog
   INSERT INTO incompatible_roles (role_a, role_b)
   SELECT r.id, 'metodolog'
   FROM roles r
   WHERE r.access_type = 'EDITOR';

   -- Обратная связь (metodolog несовместим с EDITOR)
   INSERT INTO incompatible_roles (role_a, role_b)
   SELECT 'metodolog', r.id
   FROM roles r
   WHERE r.access_type = 'EDITOR';
   ```

   **Примечание:** Если в системе уже есть механизм автоматической проверки несовместимости (симметричная проверка), достаточно одной записи на пару ролей.

4. **НЕ создавать записи в `role_space_mapping`** для новых ролей (они глобальные)

5. **Назначить роли пользователям** через таблицу `user_roles`:
   ```sql
   INSERT INTO user_roles (user_id, role_id)
   VALUES
     (<user_id>, 'approver'),
     (<user_id>, 'ratifier');
   ```

**Важно:**
- Для ролей `approver`, `ratifier` и `admin` таблица `role_space_mapping` должна быть **пустой** (глобальные роли)
- Для ролей с `access_type=EDITOR` (prm) и `access_type=METODOLOG` (methodologist) в `role_space_mapping` должны быть записи с `space_code` продуктов
- Система должна предотвращать назначение несовместимых ролей через проверку таблицы `incompatible_roles` при операциях INSERT в `user_roles`

### 4.4 Использование API в нашем приложении

#### 4.4.1 Получение информации о текущем пользователе

**Endpoint:** `GET /api/v1/user?employeeNumber={currentUserEmployeeNumber}`

**Ответ (существующий формат):**
```json
{
  "lastname": "Иванов",
  "firstname": "Иван",
  "middlename": "Иванович",
  "roles": [
    {
      "id": "experiment_editor_AUTO",
      "role_name": "ПРМ продукта. Автокредитование"
    },
    {
      "id": "approver",
      "role_name": "Согласующий"
    }
  ],
  "permittedSpaces": ["AUTO"]
}
```

**Как определить access_type роли:**

Вариант 1 (если backend добавит поле `access_type` в ответ — рекомендуется):
```json
{
  "roles": [
    {
      "id": "experiment_editor_AUTO",
      "role_name": "ПРМ продукта. Автокредитование",
      "access_type": "EDITOR"
    }
  ]
}
```

Вариант 2 (парсинг на клиенте, если поле не добавлено):
- Парсить `roles[].id`:
  - `experiment_editor_*` → EDITOR (prm)
  - `metodolog` → METODOLOG (methodologist)
  - `approver` → APPROVER
  - `ratifier` → RATIFIER
  - `experiment_admin` → ADMIN

**Интерпретация `permittedSpaces`:**
- Это агрегация всех `space_code` из таблицы `role_space_mapping` для всех ролей пользователя
- Для ролей EDITOR (prm) и METODOLOG (methodologist): `permittedSpaces` содержит коды продуктов, к которым привязана роль
- Для глобальных ролей (APPROVER, RATIFIER, ADMIN): `permittedSpaces` может быть пустым или содержать все продукты (зависит от реализации)

#### 4.4.2 Проверка прав

**Endpoint:** `GET /api/v1/access?employeeNumber=X&accessType=APPROVER`

Возвращает `boolean` — есть ли у пользователя указанный тип доступа.

**Использование:**
- Проверка перед назначением пользователя approver/ratifier
- Проверка прав на операции (если нужно)

**Примечание:** Параметр `spaceCode` опционален. Для глобальных ролей (APPROVER, RATIFIER) его можно не передавать.

**Важно:** Endpoint `/api/v1/access` уже существует в rscon-sudir API. Для работы с новыми ролями нужно только добавить `APPROVER` и `RATIFIER` в enum `accessType` (см. раздел 5).

---

## 5) Изменения, которые нужно внести (чек-лист для backend-команды rscon-sudir)

**Обязательные изменения в БД:**

1. **Расширить допустимые значения поля `access_type` в таблице `roles`:**
   - Добавить `APPROVER`
   - Добавить `RATIFIER`

   Если `access_type` реализован как enum — выполнить ALTER TYPE:
   ```sql
   ALTER TYPE access_type_enum ADD VALUE 'APPROVER';
   ALTER TYPE access_type_enum ADD VALUE 'RATIFIER';
   ```

   Если varchar с constraint — обновить constraint.

2. **Создать записи в таблице `roles`:**
   ```sql
   INSERT INTO roles (id, role_name, access_type, archive)
   VALUES
     ('approver', 'Согласующий', 'APPROVER', false),
     ('ratifier', 'Утверждающий', 'RATIFIER', false);
   ```

3. **Настроить несовместимые роли в таблице `incompatible_roles`:**

   Согласно требованиям MVP, роли PRM (EDITOR) и Methodologist (METODOLOG) несовместимы.

   ```sql
   -- Для каждой роли EDITOR (prm) добавить несовместимость с metodolog
   INSERT INTO incompatible_roles (role_a, role_b)
   SELECT r.id, 'metodolog'
   FROM roles r
   WHERE r.access_type = 'EDITOR';

   -- Обратная связь (metodolog несовместим с EDITOR)
   INSERT INTO incompatible_roles (role_a, role_b)
   SELECT 'metodolog', r.id
   FROM roles r
   WHERE r.access_type = 'EDITOR';
   ```

   **Примечание:** Если в системе уже есть механизм автоматической проверки несовместимости (симметричная проверка), достаточно одной записи на пару ролей.

4. **Назначить роли пользователям через таблицу `user_roles`:**
   ```sql
   -- Пример для конкретного пользователя
   INSERT INTO user_roles (user_id, role_id)
   SELECT u.id, 'approver'
   FROM users u
   WHERE u.employee_number = '<employee_number>';
   ```

   При назначении система должна автоматически проверять таблицу `incompatible_roles` и отклонять попытки назначить несовместимые роли.

5. **Настроить `role_space_mapping` для ролей methodologist:**
   ```sql
   -- Пример: привязать роль методолога к продукту AUTO
   INSERT INTO role_space_mapping (role_id, space_code)
   VALUES ('<methodologist_role_id>', 'AUTO');
   ```

6. **НЕ создавать записи в `role_space_mapping`** для ролей approver/ratifier/admin (они глобальные)

**Опциональные улучшения (не блокируют MVP):**

6. **Добавить поле `access_type` в ответ `GET /api/v1/user`:**
   ```json
   "roles": [
     {
       "id": "approver",
       "role_name": "Согласующий",
       "access_type": "APPROVER"  // НОВОЕ ПОЛЕ
     }
   ]
   ```
   Это упростит клиентский код (не придётся парсить role_id для определения типа роли).

---

## 6) QA / критерии приемки

**Интеграция с rscon-sudir (БД):**
- Таблица `roles` содержит записи с `access_type` = `APPROVER` и `RATIFIER`.
- Для ролей approver/ratifier/admin в таблице `role_space_mapping` нет записей (глобальные роли).
- Для ролей с `access_type=EDITOR` (prm) и `access_type=METODOLOG` (methodologist) в таблице `role_space_mapping` есть записи с соответствующими `space_code`.

**Интеграция с rscon-sudir (API):**
- `GET /api/v1/user?employeeNumber=X` возвращает все роли пользователя, включая новые (approver, ratifier).
- `GET /api/v1/access?employeeNumber=X&accessType=APPROVER` корректно проверяет наличие роли approver.
- `GET /api/v1/access?employeeNumber=X&accessType=RATIFIER` корректно проверяет наличие роли ratifier.

**Множественные роли:**
- Пользователь может иметь несколько ролей одновременно (например, EDITOR + APPROVER).
- Таблица `user_roles` содержит несколько записей для одного `user_id` с разными `role_id`.

**Несовместимые роли:**
- В таблице `incompatible_roles` настроены записи, предотвращающие назначение EDITOR и METODOLOG одному пользователю.
- Система предотвращает назначение несовместимых ролей через проверку таблицы `incompatible_roles` при операциях INSERT в `user_roles`.
- Попытка назначить пользователю роль EDITOR, если у него уже есть METODOLOG (или наоборот) → отклонено.

**Product scoping:**
- Для пользователей с ролями EDITOR (prm) и METODOLOG (methodologist) в ответе `GET /api/v1/user` поле `permittedSpaces` содержит коды продуктов из `role_space_mapping`.
- Для пользователей с глобальными ролями (APPROVER, RATIFIER, ADMIN) поле `permittedSpaces` пустое или содержит все продукты (зависит от реализации).

**Клиентское приложение:**
- Клиент корректно парсит `roles[].id` для определения access_type (или использует поле `access_type`, если оно добавлено в API).
- Клиент использует `GET /api/v1/access` для проверки прав перед назначением approvers/ratifiers.
- Permission checks в backend корректно работают для всех ролей MVP.

---

## 7) Порядок реализации (чтобы не блокировать)

**Фаза 1: Расширение rscon-sudir (критичный путь, делает backend-команда rscon-sudir)**

1. **Миграция БД:**
   - Расширить допустимые значения `access_type` (ALTER TYPE или UPDATE constraint)
   - Создать записи в таблице `roles` для approver и ratifier
   - Настроить несовместимые роли в таблице `incompatible_roles` (EDITOR ↔ METODOLOG)
   - Назначить роли тестовым пользователям через `user_roles`

2. **Проверка:**
   - Убедиться, что `GET /api/v1/user` возвращает новые роли
   - Убедиться, что `GET /api/v1/access?accessType=APPROVER` работает корректно

**Фаза 2: Интеграция в основное приложение (делает наша команда)**

3. **Клиентский код:**
   - Реализовать маппинг `roles[].id` → access_type (парсинг на клиенте)
   - Использовать `GET /api/v1/user` для получения ролей текущего пользователя
   - Использовать `GET /api/v1/access` для проверки прав перед назначением approvers/ratifiers

4. **Backend permission checks:**
   - Реализовать проверки ролей при CRUD операциях (Simulation/Pilot/Deployment/Scorecard)
   - Реализовать проверки ролей при операциях согласования/утверждения
   - Интегрировать с rscon-sudir API для получения информации о пользователях

**Фаза 3: Улучшения (опционально, не блокирует MVP, делает backend-команда rscon-sudir)**

5. **Добавить поле `access_type` в ответ `GET /api/v1/user`** — упростит клиентский код (не придётся парсить role_id)
