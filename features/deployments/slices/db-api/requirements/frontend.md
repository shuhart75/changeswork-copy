# DB/API контракт внедрения (Frontend)

Статус: **draft**  
Feature: `deployments`  
Slice: `db-api`  
Область: `MVP`  
Дата обновления: `2026-04-27`  
Шаблон: `.workflow/templates/requirements/frontend.template.md`

## Связь с feature-level документом

- Главный контрольный документ: `../../requirements.md`
- Этот файл детализирует раздел `Реализация для FRONTEND` для текущего slice.

## Назначение пакета

- Зафиксировать ожидания frontend к deployment API и payload structure.
- Обеспечить единый контракт для list/form/detail/lifecycle screens.

## Источники и трассировка

### Основные источники

- `../slice.md`
- `../../requirements.md`
- `../../feature.md`
- `../../references.md`
- `requirements/backend.md`

### Связанные planning stories

- `STORY-DEPLOYMENTS-005`

## Контекст и бизнес-смысл

### Цель

Frontend должен опираться на стабильный API-контракт и не создавать собственные схемы данных для deployment scope.

### Бизнес-контекст

Этот slice не вводит отдельный UI-сценарий. Он обслуживает все остальные deployment screens.

## Границы MVP

### Входит в MVP

- согласованный shape deployment payload;
- правила чтения status, lineage, scorecards, related entities;
- единое ожидание по ошибкам и валидации.

### Не входит в MVP

- произвольные клиентские адаптеры, меняющие смысл contract fields.

## Пользовательские сценарии

### Сценарий FE-1. Чтение deployment payload
1. Frontend запрашивает deployment data.
2. Получает единый payload.
3. Использует его в list/detail/form screens.

### Сценарий FE-2. Отправка mutation payload
1. Frontend формирует запрос по contract.
2. Backend валидирует payload.
3. UI интерпретирует ответ и ошибки по согласованной схеме.

## Функциональные требования

### FE-FR-1. Stable payload contract

**Описание:**
Все deployment screens используют один согласованный shape данных.

### FE-FR-2. Error contract consistency

**Описание:**
Frontend ожидает и обрабатывает ошибки по единой схеме.

## Интеграция с Backend API

| Метод и маршрут | Где используется | Что отправляем/читаем | Условия вызова | Примечание |
|---|---|---|---|---|
| deployment endpoints | все deployment screens | list/detail/form/lifecycle payloads | по screen flow | см. backend pack |

## Валидация на frontend

### Правила

- payload строится только из согласованных полей;
- неизвестные поля не должны отправляться в mutation requests.

### Сообщения об ошибках

| Ситуация | Сообщение | Где показываем |
|---|---|---|
| невалидный ответ | `Не удалось обработать ответ сервера` | toast / error boundary |
| ошибка валидации | `Данные внедрения заполнены некорректно` | форма / inline |

## Критерии приемки

### FE-AC-1. Contract usage
- [ ] Все deployment screens используют единый API-контракт

### FE-AC-2. Error handling
- [ ] Ошибки API интерпретируются одинаково на связанных экранах
