# Системные требования — Артефакты (core) для MVP

Статус: **для передачи команде**
Область: MVP
Дата обновления: 2026-03-15

## 1) Цель и границы задачи

### 1.1 Цель
Система должна предоставить **единый переиспользуемый механизм “Артефакты”** (БД + API + UI‑блоки), который позволяет прикреплять **ссылки на внешние документы** к ключевым сущностям MVP с единообразными:
- моделью данных
- правами доступа
- CRUD‑операциями
- отображением в UI

### 1.2 Входит в MVP
Артефакты могут быть прикреплены к:
- **Пилоту (Pilot)**
- **Симуляции (Simulation)**
- **Внедрению (Deployment)**

В MVP артефакты — это **только ссылки** (без загрузки файлов).

### 1.3 Не входит в MVP
- Хранение файлов внутри системы (upload/attachments)
- Парсинг/превью ссылок, сбор метаданных
- Версионирование документов
- Отдельные сложные workflow согласования артефактов (артефакты следуют ЖЦ родительской сущности)

---

## 2) Определения

### 2.1 Артефакт (Artifact)
**Артефакт** — запись, содержащая ссылку на внешний документ и прикреплённая ровно к одной родительской сущности.

Минимальные поля:
- `id` — уникальный идентификатор
- `entityType` — enum: `PILOT` | `SIMULATION` | `DEPLOYMENT`
- `entityId` — идентификатор родительской сущности
- `title` — короткое понятное название
- `url` — внешняя ссылка
- `type` — классификация (enum или строка; в MVP допустим небольшой enum + `OTHER`)
- `description` — опционально, краткое описание
- `createdAt`, `createdBy`
- `updatedAt`, `updatedBy`

Рекомендуемые (если дёшево):
- `order` — число для стабильной сортировки в UI


### 2.2 Инварианты
- `url` обязателен и должен быть валидным URL (базовая проверка формата)
- `title` обязателен
- артефакт принадлежит **ровно одной** сущности (`entityType`, `entityId`)

---

## 3) Контроль доступа (RBAC)

### 3.1 Наследование прав
Артефакты должны **наследовать права от родительской сущности**.

Правила:
- **Просмотр артефактов**: разрешён, если у пользователя есть право просмотра родительской сущности (Pilot/Simulation/Deployment).
- **Создание/изменение/удаление артефактов**: разрешено, если у пользователя есть право редактирования родительской сущности.

В MVP не вводим отдельную матрицу прав “на уровне артефакта”.

### 3.2 Аудит
Любое создание/изменение/удаление артефакта должно оставлять аудит‑след хотя бы через:
- `updatedAt/updatedBy`

---

## 4) Backend (БД + API)

### 4.1 Модель данных (для реализации задачи)

#### 4.1.1 Таблица `artifacts`

Минимальный состав колонок (SQL-ориентированно; типы можно адаптировать под выбранный стек):

| Поле | Тип | Обяз. | Описание |
|---|---|---:|---|
| `id` | UUID / BIGINT | да | PK |
| `entity_type` | VARCHAR(32) | да | Тип родителя: `PILOT` \| `SIMULATION` \| `DEPLOYMENT` |
| `entity_id` | UUID / BIGINT | да | ID родительской сущности |
| `title` | VARCHAR(200) | да | Название артефакта |
| `url` | VARCHAR(2048) | да | Ссылка на внешний документ |
| `type` | VARCHAR(32) | да | Классификация; по умолчанию `OTHER` |
| `description` | TEXT | нет | Краткое описание |
| `order` | INT | нет | Порядок отображения (сортировка) |
| `created_at` | TIMESTAMP | да | Дата/время создания |
| `created_by` | UUID / BIGINT | да | Кто создал |
| `updated_at` | TIMESTAMP | да | Дата/время последнего изменения |
| `updated_by` | UUID / BIGINT | да | Кто изменил |

Примечание по дефолтам:
- `type` default `OTHER`

Также допускается хранить `created_by/updated_by` как string (username) — если в проекте нет стабильных user id.

---

#### 4.1.2 Ограничения, индексы, FK

Ограничения:
- CHECK на `entity_type` ∈ {PILOT, SIMULATION, DEPLOYMENT}
- (опционально) UNIQUE `(entity_type, entity_id, order)` — если хотим запретить дубли `order`

Индексы:
- INDEX `(entity_type, entity_id)` — основной для списка по родителю
- (опционально) INDEX `(entity_type, entity_id, order, created_at)`

Примечание про FK:
- так как связь полиморфная (`entity_type` + `entity_id`), строгие внешние ключи на 3 таблицы не обязательны для MVP.
- доступ/существование родителя проверяются на уровне бизнес-логики (404/403).


---

#### 4.1.3 DTO (контрактные модели)

> Ниже — контрактные модели (DTO) в том виде, как они должны выглядеть в OpenAPI/контрактах.
> Реальные внутренние модели могут отличаться, но API должен соответствовать.

| Модель | Поле | Тип | Обяз. | Описание |
|---|---|---|---:|---|
| `Artifact` | `id` | string (uuid) | да | Идентификатор |
|  | `entityType` | `PILOT`\|`SIMULATION`\|`DEPLOYMENT` | да | Тип родителя |
|  | `entityId` | string (uuid) | да | ID родителя |
|  | `title` | string | да | Название |
|  | `url` | string | да | URL |
|  | `type` | string | да | Тип/категория |
|  | `description` | string | нет | Описание |
|  | `order` | integer | нет | Порядок |
|  | `createdAt` | string (date-time) | да | Создан |
|  | `createdBy` | string (uuid) | да | Кто создал |
|  | `updatedAt` | string (date-time) | да | Обновлён |
|  | `updatedBy` | string (uuid) | да | Кто обновил |
| `ArtifactCreateRequest` | `title` | string | да | Название |
|  | `url` | string | да | URL |
|  | `type` | string | нет | Тип/категория |
|  | `description` | string | нет | Описание |
|  | `order` | integer | нет | Порядок |
| `ArtifactUpdateRequest` | `title` | string | нет | Название |
|  | `url` | string | нет | URL |
|  | `type` | string | нет | Тип/категория |
|  | `description` | string | нет | Описание |
|  | `order` | integer | нет | Порядок |

Примечание по типам идентификаторов:
- В таблице допускаются UUID/BIGINT.
- В OpenAPI в примерах используется `uuid`. Если в проекте numeric id — заменить `format: uuid` на нужный формат.

---

#### 4.1.4 OpenAPI (встроенный источник контракта)

OpenAPI‑фрагмент приведён ниже в разделе 4.2.2.

---

### 4.2 API

#### 4.2.1 Endpoints
Entity‑scoped endpoints:

1) Получить список артефактов сущности
- `GET /api/{entityType}/{entityId}/artifacts`
- Ответ: массив артефактов, сортировка по `order`, затем `createdAt` (или только по `createdAt`)

2) Создать артефакт
- `POST /api/{entityType}/{entityId}/artifacts`
- Body: `title, url, type, description, order`
- Ответ: созданный артефакт

Глобальные endpoints:

3) Обновить артефакт
- `PATCH /api/artifacts/{artifactId}`
- Body: любые из `title, url, type, description, order`

4) Удалить артефакт
- `DELETE /api/artifacts/{artifactId}`

#### 4.2.2 OpenAPI (фрагмент контракта)
Ниже — минимальный OpenAPI 3.0 фрагмент.

```yaml
components:
  schemas:
    ArtifactEntityType:
      type: string
      enum: [PILOT, SIMULATION, DEPLOYMENT]

    Artifact:
      type: object
      required: [id, entityType, entityId, title, url, type, createdAt, createdBy, updatedAt, updatedBy]
      properties:
        id: { type: string, format: uuid }
        entityType: { $ref: '#/components/schemas/ArtifactEntityType' }
        entityId: { type: string, format: uuid }
        title: { type: string, maxLength: 200 }
        url: { type: string, maxLength: 2048 }
        type: { type: string, maxLength: 32 }
        description: { type: string }
        order: { type: integer }
        createdAt: { type: string, format: date-time }
        createdBy: { type: string, format: uuid }
        updatedAt: { type: string, format: date-time }
        updatedBy: { type: string, format: uuid }

    ArtifactCreateRequest:
      type: object
      required: [title, url]
      properties:
        title: { type: string, maxLength: 200 }
        url: { type: string, maxLength: 2048 }
        type: { type: string, maxLength: 32 }
        description: { type: string }
        order: { type: integer }

    ArtifactUpdateRequest:
      type: object
      properties:
        title: { type: string, maxLength: 200 }
        url: { type: string, maxLength: 2048 }
        type: { type: string, maxLength: 32 }
        description: { type: string }
        order: { type: integer }

paths:
  /api/{entityType}/{entityId}/artifacts:
    get:
      summary: Получить список артефактов родительской сущности
      description: |
        Возвращает список артефактов (ссылок на внешние документы), прикреплённых к сущности
        заданного типа (`entityType`) и идентификатора (`entityId`).

        Права доступа наследуются от родительской сущности.
        Сортировка: по `order` (если задан), затем по `createdAt`.
      parameters:
        - name: entityType
          in: path
          required: true
          schema: { $ref: '#/components/schemas/ArtifactEntityType' }
        - name: entityId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/Artifact' }
        '403': { description: Forbidden }
        '404': { description: Not Found }

    post:
      summary: Создать артефакт для родительской сущности
      description: |
        Создаёт новый артефакт (ссылку на внешний документ) и прикрепляет его к родительской сущности.
        Права доступа наследуются от родительской сущности.
      parameters:
        - name: entityType
          in: path
          required: true
          schema: { $ref: '#/components/schemas/ArtifactEntityType' }
        - name: entityId
          in: path
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ArtifactCreateRequest' }
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Artifact' }
        '403': { description: Forbidden }
        '404': { description: Not Found }
        '422': { description: Unprocessable Entity }

  /api/artifacts/{artifactId}:
    patch:
      summary: Обновить артефакт
      description: |
        Обновляет поля существующего артефакта по его `artifactId`.
        Права на обновление наследуются от родительской сущности.
      parameters:
        - name: artifactId
          in: path
          required: true
          schema: { type: string, format: uuid }
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/ArtifactUpdateRequest' }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/Artifact' }
        '403': { description: Forbidden }
        '404': { description: Not Found }
        '422': { description: Unprocessable Entity }

    delete:
      summary: Удалить артефакт
      description: |
        Удаляет артефакт по его `artifactId`.
        Права на удаление наследуются от родительской сущности.
      parameters:
        - name: artifactId
          in: path
          required: true
          schema: { type: string, format: uuid }
      responses:
        '204': { description: No Content }
        '403': { description: Forbidden }
        '404': { description: Not Found }
```

### 4.3 Валидация
- `url`:
  - обязателен, не пустой
  - ограничение длины (например ≤ 2048)
  - базовая серверная проверка формата URL
- `title`:
  - обязателен, не пустой
  - ограничение длины (например ≤ 250)

### 4.4 Ошибки
- `403` — нет доступа к родительской сущности
- `404` — родительская сущность / артефакт не найдены
- `422` — ошибка валидации

(Опционально) `201` для успешного создания, `204` для успешного удаления.

**Важно:** формат идентификаторов в OpenAPI указан как `uuid` для определённости. Если в проекте используются numeric id — заменить `format: uuid` на подходящий формат.
---

## 5) Frontend (UI)

### 5.0 Интерактивный макет

**Файл:** `../prototypes/artifacts_mockup.html`

Интерактивный HTML-макет демонстрирует:
- Вкладку "Документы" на детальной странице пилота
- Режим просмотра (пустое состояние и список документов)
- Режим редактирования (добавление/удаление документов)
- Форму добавления нового документа

Макет можно открыть в браузере без сборки.

### 5.1 Где показываем артефакты (MVP)
- Детальная страница Пилота: вкладка **Документы**/секция **Артефакты**
- Детальная страница Симуляции: вкладка **Документы** (создать, сейчас её нет)/секция **Артефакты**
- Детальная страница Внедрения: секция **Артефакты**

### 5.2 Поведение секции “Артефакты”
- Список/таблица:
  - `title` (как ссылка)
  - `type`
  - опционально: `description`
  - действия (edit/delete) только если пользователь может редактировать родительскую сущность
- Кнопка **Добавить артефакт** только если пользователь может редактировать родительскую сущность
- Открытие ссылок:
  - в новой вкладке/окне
  - безопасные атрибуты (`target=_blank`, `rel=noopener`)

### 5.3 Форма создания/редактирования
Поля:
- `title` (обязательное)
- `url` (обязательное)
- `type`
- `description` (опционально)

### 5.4 Состояния
- Пустое состояние: “Артефактов нет” + кнопка “Добавить” (если разрешено)
- Loading / Error — стандартные

---

## 6) QA / критерии приемки

### 6.1 Позитивные сценарии
Для каждого типа сущности (**Pilot**, **Simulation**, **Deployment**):
- Пользователь с правами редактирования может:
  - создать артефакт → он появляется в списке
  - изменить title/url/type/description → изменения сохраняются
  - удалить артефакт → он исчезает из списка
- Пользователь только с правами просмотра:
  - видит список артефактов
  - не видит кнопки Add/Edit/Delete

### 6.2 Негативные сценарии
- невалидный `url` → `422` + понятное сообщение в форме
- нет прав → `403`
- несуществующий `artifactId` → `404`

---

## 7) Нефункциональные требования
- Безопасность:
  - защита от XSS (экранирование/санитизация текстовых полей)
  - безопасное открытие внешних ссылок (`noopener`)
- Производительность:
  - получение списка артефактов должно быть быстрым; ожидается небольшой объём на сущность
- Совместимость:
  - ссылки могут вести на любые внешние домены; система не должна скачивать/парсить содержимое

---

## 8) Порядок реализации (чтобы не блокировать)
1) **Backend core (БД + API)** для entityType = PILOT/SIMULATION/DEPLOYMENT
2) FE‑блоки:
   - секция артефактов на Пилоте
   - секция артефактов на Симуляции
   - секция артефактов на Внедрении
3) QA smoke по всем 3 типам сущностей
