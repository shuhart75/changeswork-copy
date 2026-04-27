# Создание и редактирование внедрения (Backend)

Статус: **draft**  
Feature: `deployments`  
Slice: `form-editing`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Описать create/update contracts для deployment form.
- Зафиксировать ограничения по типу внедрения, lineage и составу scorecards.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `../requirements/frontend.md`

### Связанные planning stories

- `STORY-DEPLOYMENTS-003`

## Контекст и бизнес-смысл

### Цель

Backend должен принимать и валидировать форму внедрения так, чтобы create/edit flow не нарушал доменные правила deployment.

### Источник правды

- deployment aggregate;
- lineage rules;
- scorecard bindings;
- approval/lifecycle restrictions.

## Бизнес-правила и системные ограничения

### BR-1. Deployment type immutability
- после первичной фиксации `deployment_type` не меняется через обычное редактирование;
- для `simulation_based` внедрения lineage simulation фиксируется как источник результата.

### BR-2. Scorecard and lineage consistency
- обязательная lineage-скоркарта и lineage simulation должны быть согласованы;
- изменение состава связанных scorecards проходит серверную проверку.

## Границы MVP

### Входит в MVP

- `POST`/`PUT` контракты внедрения;
- проверка допустимых редактируемых полей;
- валидация lineage и scorecards.

### Не входит в MVP

- произвольное изменение уже зафиксированного deployment type;
- обход lifecycle/status guards через form endpoints.

## Пользовательские и системные сценарии

### Сценарий BE-1. Создание внедрения
1. Клиент отправляет create payload.
2. Backend создаёт deployment в допустимом стартовом состоянии.
3. Возвращает созданную сущность для дальнейшего flow.

### Сценарий BE-2. Редактирование внедрения
1. Клиент отправляет update payload.
2. Backend проверяет статус, редактируемые поля и lineage constraints.
3. При успехе сохраняет изменения и возвращает обновлённую сущность.

## Функциональные требования

### BE-FR-1. Create contract

**Описание:**
Create endpoint принимает согласованный набор полей для нового deployment.

### BE-FR-2. Update restrictions

**Описание:**
Update endpoint не допускает изменение недопустимых полей и несогласованных scorecard/lineage комбинаций.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `deployment` | business fields | domain | да | создаваемое/редактируемое внедрение |
| `deployment_scorecard` | binding fields | relation | нет | связанные scorecards |

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `POST /api/v1/deployments` | создание внедрения | frontend form | стартовый create flow |
| `PUT /api/v1/deployments/{id}` | редактирование внедрения | frontend form | учитывает status guards |

## Ошибки и валидация

### Валидационные правила

- недопустимое изменение `deployment_type` отклоняется;
- невалидная комбинация scorecards и lineage отклоняется;
- update невозможен в запрещённых status states.

### Ошибки API

| Код/сценарий | Условие | Ответ |
|---|---|---|
| `400` | невалидный payload | сообщение о нарушении правил формы |
| `409` | конфликт status/state | сообщение о недопустимом изменении |

## Критерии приемки

### BE-AC-1. Create and update guards
- [ ] Backend enforce-ит правила create/edit flow

### BE-AC-2. Lineage consistency
- [ ] Lineage и scorecards валидируются на backend
