# Срез — Матрица доступа к endpoint

Статус: **draft**
Фича: `features/roles-industrialization/feature.md`
Порядок в требованиях фичи: `02`
Дата обновления: `2026-06-01`
Формат: **новый лёгкий**
Шаблон: `.workflow/templates/requirements/slice.readable.template.md`

## Назначение

Зафиксировать единый mapping ролей на backend operations и способ, которым FE и BE используют эту матрицу.

## Главное

- Главный источник бизнес-правил: `../../requirements.md`.
- Срез описывает endpoint matrix как Q3 source of truth, а не как пересказ Q2 control-layer.
- Если появится новая endpoint group, сначала обновить `../../requirements.md`, затем синхронизировать этот срез.

## Границы среза

| Входит | Не входит |
|---|---|
| endpoint groups из источника | release-promotion в baseline/current |
| allow / allow_in_space / deny semantics | фактическая переработка всех соседних feature packs в этом же проходе |
| единые правила для FE visibility и backend authorization | перепланирование Q2 задач |

## Схема среза

```plantuml
@startuml
left to right direction
rectangle "Role matrix" as A
rectangle "Endpoint operation" as B
rectangle "Access decision" as C
rectangle "FE/BE enforcement" as D
A --> B
B --> C
C --> D
@enduml
```

## Связанные плановые истории

- `STORY-ROLES-IND-002`

## Пакеты требований

- `../../requirements.md`
- `requirements/frontend.md`
- `requirements/backend.md`

## Связанные прототипы

- `—`

## Фокус тестирования среза

- [ ] Проверить основной успешный сценарий.
- [ ] Проверить пустые состояния.
- [ ] Проверить ошибки API и недоступные действия.
- [ ] Проверить права ролей.
- [ ] Проверить отсутствие старых терминов/маршрутов/статусов, если срез заменяет прежнюю логику.

## Связанные артефакты исполнения

- `execution/tasks.md`
