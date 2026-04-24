# Задачи для страницы "Цепочки" (Chains / Lineage)

**Источник правды:** [`spec/domain_model.md`](/home/reutov/Documents/AI/changesWork/spec/domain_model.md) (контекст Lineage, см. раздел 7)

## Обзор

**Страница:** "Цепочки"  
**Смысл:** UI-визуализация lineage (цепочки происхождения) через связи "создано из" (таблицы `*_source`).  
**Важно:** В рамках рескоупа MVP v6.3 **Инициативы не реализуются**. "Цепочка" строится вокруг `Deployment` и его источников.

## AN-D1: Аналитика "Цепочки"

**Тип:** Task  
**Оценка:** 5 дней (как в Gantt v6 для AN_D1)

### Что уточнить

- Какие варианты "цепочки" показываем:
  - только для `Deployment` (основной вариант)
  - дополнительно для `Pilot` и `Simulation` (как lineage-дерево)
- Требования к рекурсивности: 1 уровень (Deployment -> Pilots/Simulations) или полноценная рекурсия (как в spec).
- Нужна ли фильтрация по продукту/критичности, сортировки, полнотекстовый поиск.
- Нужна ли отдельная "деталка цепочки" или достаточно переходов в `Deployment` detail.

### Артефакты

- UI-mock соответствовать прототипу (ChainsView).
- Согласованный API-контракт для списка и детальной lineage.

## BE-D1: Backend для "Цепочки" (list)

**Тип:** Story  
**Оценка:** 3 дня (как в Gantt v6 для BE_D1)

### Scope

1. **GET /api/chains/** (виртуальная сущность, без CRUD):
   - Возвращает список `Deployment` + агрегаты по lineage:
     - counts: simulations / pilots
     - priority (например, MAX из deployment.priority или derived)
     - статусы ключевых сущностей
2. Фильтры/сортировка: минимально по `product_id`, `status`, `priority`, `search`.

### Acceptance Criteria

- [ ] Endpoint `GET /api/chains/` реализован и возвращает данные, достаточные для таблицы ChainsView.
- [ ] Данные не требуют таблиц `chain/*` (цепочка вычисляется по `DeploymentSource/PilotSource/SimulationSource`).

## BE-DD1: Backend для lineage (detail)

**Тип:** Task  
**Оценка:** 3 дня (как в Gantt v6 для BE_DD1)

### Scope

- `GET /api/lineage/?target_type=deployment&target_id={uuid}`
  - Возвращает граф lineage (узлы: Simulation/Pilot/Deployment/Scorecard; ребра: "created_from"/"uses")
  - Допускается упрощенная версия для MVP: только Deployment -> {Pilots, Simulations} + их Scorecards.

### Acceptance Criteria

- [ ] Endpoint возвращает стабильный формат (nodes/edges), пригодный для визуализации.
- [ ] Доступы: минимум чтение для ролей, у которых есть доступ к Deployment.

## BE-CD1: Создание источников lineage при создании сущностей

**Тип:** Task  
**Оценка:** 2 дня (как в Gantt v6 для BE_CD1)

### Scope

- При создании `Pilot` и `Deployment` на основе выбранных `Scorecard`:
  - backend определяет, какие `Simulation`/`Pilot` являются источниками скоркарт
  - записывает `PilotSource` / `DeploymentSource` автоматически (как в spec).

### Acceptance Criteria

- [ ] `PilotSource` / `DeploymentSource` создаются автоматически на create/update (минимум на create).
- [ ] Lineage корректно отражает источники для пилота и внедрения.

## FE-D1: Frontend "Цепочки" (list)

**Тип:** Story  
**Оценка:** 3 дня (как в Gantt v6 для FE_D1)

### Scope

- Страница "Цепочки" (ChainsView):
  - таблица: ID, Deployment, counts Simulations/Pilots, priority, status, created_at
  - фильтры по продукту/приоритету/статусу
  - переход в `Deployment` detail по клику

### Acceptance Criteria

- [ ] Страница отображает данные из `GET /api/chains/`.
- [ ] Переход в деталку `Deployment` работает.

## FE-DD1: Визуализация lineage (detail widget)

**Тип:** Task  
**Оценка:** 10 дней (как в Gantt v6 для FE_DD1)

### Scope

- Компонент для отображения lineage-графа/списков:
  - используется в `DeploymentDetail` и (опционально) в ChainsView
  - подгружает `GET /api/lineage?...`

### Acceptance Criteria

- [ ] На странице `DeploymentDetail` отображается lineage (минимум списком источников).

## FE-CD1: Интеграция lineage в формы (UX)

**Тип:** Task  
**Оценка:** 3 дня (как в Gantt v6 для FE_CD1)

### Scope

- В формах `Pilot` и `Deployment`:
  - пользователь выбирает `Scorecard` (как и раньше)
  - UI показывает "источники" выбранных скоркарт (preview lineage), если возможно

### Acceptance Criteria

- [ ] Preview источников не блокирует сохранение (может быть best-effort).

