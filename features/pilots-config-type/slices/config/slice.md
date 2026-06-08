# Slice — Конфигурация процесса

Статус: **draft**  
Feature: `features/pilots-config-type/feature.md`  
Slice slug: `config`  
Порядок в feature requirements: `01`  
Дата обновления: `2026-06-08`

## Производность от общего требования

- Этот slice не является самостоятельным источником требований.
- Он выделяется из соответствующего раздела `../../requirements.md`.
- Если здесь обнаруживается новый scope или противоречие, сначала обновляется `../../requirements.md`, затем этот slice.

## Назначение

Выделить дельту по полю `processType`: UI-выбор, хранение в `experiments.process_type`, API-возврат и миграция существующих записей.

## Что входит

- select типа процесса в форме пилота;
- read-only отображение типа процесса;
- backend enum и миграция;
- обновление experiment API-схем.

## Что не входит

- новая ролевая модель;
- изменение lifecycle пилотов;
- planning/execution/prototype импорт из входящей папки;
- изменение `/api/v2/config`; фильтрация закреплена только за `/api/v3/config`.

## Связанные planning stories

- `STORY-PILOTS-CONFIG-001` — есть во входящей папке, не импортирован в режиме `requirements`.

## Источники

- `../../references.md`
- `../../requirements.md`
- `/home/reutov/Downloads/coda_docs/`

## Шаблоны requirement packs

- `.workflow/templates/requirements/feature-requirements.template.md`
- `.workflow/templates/requirements/frontend.template.md`
- `.workflow/templates/requirements/backend.template.md`

## Пакеты требований

- `../../requirements.md`
- `requirements/frontend.md`
- `requirements/backend.md`

## Связанные прототипы

- `features/pilots/slices/workspace/delivery-prototype/prototype.html`
- `delivery-prototype/prototype.html` во входящей папке не импортирован в режиме `requirements`.

## Связанные execution-артефакты

- `execution/tasks.md` во входящей папке не импортирован в режиме `requirements`.

## Consistency touchpoints

- Затрагивает соседние features: `features/pilots/`.
- Затрагивает baseline/current: domain/data/api descriptions.
- Нужна запись в `../../domain-impact.md`: да.
