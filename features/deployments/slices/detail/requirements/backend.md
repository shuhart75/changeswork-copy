# Детальная страница внедрения (Backend)

Статус: **draft**  
Feature: `deployments`  
Slice: `detail`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/backend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация BACKEND` для текущего slice.

## Назначение пакета

- Описать detail payload внедрения для host screen.
- Зафиксировать состав данных: общая информация, scorecards, related entities, artifacts, lineage.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `../requirements/frontend.md`

### Связанные planning stories

- `STORY-DEPLOYMENTS-004`

## Контекст и бизнес-смысл

### Цель

Detail screen должен получать один согласованный backend payload, достаточный для отображения полного состояния внедрения.

### Источник правды

- deployment aggregate;
- related scorecards;
- derived related entities;
- artifacts;
- `ApprovalInstance` status при наличии процесса.

## Бизнес-правила и системные ограничения

### BR-1. Единый detail payload
- detail screen не должен собираться из противоречащих друг другу источников;
- lineage simulation и required scorecard flags должны быть явно выражены в ответе.

### BR-2. Read/edit boundary
- detail payload пригоден и для read-mode, и как основа для перехода в edit-mode;
- недопустимые к изменению поля остаются source-of-truth на backend.

## Границы MVP

### Входит в MVP

- общая информация;
- связанные scorecards;
- related entities;
- artifacts;
- process status;
- lineage information для simulation-based deployment.

### Не входит в MVP

- отдельные расширенные аналитические view beyond current requirements.

## Пользовательские и системные сценарии

### Сценарий BE-1. Открытие detail screen
1. Клиент запрашивает deployment detail.
2. Backend собирает aggregate и связанные блоки.
3. Возвращает единый detail payload.

### Сценарий BE-2. Пустые связанные блоки
1. Для deployment отсутствуют related entities или artifacts.
2. Backend возвращает пустые коллекции, а не неоднозначные null-структуры.

## Функциональные требования

### BE-FR-1. Detail composition

**Описание:**
Detail endpoint возвращает composition данных для всех обязательных блоков экрана.

### BE-FR-2. Related entities derivation

**Описание:**
Связанные `Pilot` и `Simulation` вычисляются через связанные scorecards и lineage rules.

## Модель данных

### Основные сущности и поля

| Сущность / таблица | Поле | Тип | Обязательность | Описание |
|---|---|---|---|---|
| `deployment` | ключевые business fields | domain | да | общая информация |
| `scorecard` | binding fields | relation | нет | связанные scorecards |
| `artifact` | artifact fields | relation | нет | внешние ссылки |

## API-контракт

### Эндпоинты

| Метод и маршрут | Назначение | Кто вызывает | Примечание |
|---|---|---|---|
| `GET /api/v1/deployments/{id}` | detail payload | frontend detail screen | единый источник detail data |

## Ошибки и валидация

### Валидационные правила

- несуществующий deployment возвращает `404`;
- недоступный deployment возвращает `403`.

## Критерии приемки

### BE-AC-1. Detail payload
- [ ] Detail endpoint возвращает состав данных для всех обязательных блоков экрана

### BE-AC-2. Empty and derived blocks
- [ ] Пустые и вычисляемые блоки возвращаются в согласованном формате
