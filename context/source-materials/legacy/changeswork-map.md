# changesWork -> harness map

Дата обновления: `2026-04-24`
Источник: `/home/reutov/Documents/AI/changesWork`

## Что уже перенесено полностью

- Полный raw snapshot лежит в `context/source-materials/legacy/changeswork-full/`.
- Planning raw-артефакты квартала вынесены в `planning/2026-Q2/imported-source/`.
- Основные requirements/prototypes/diagrams продублированы в `context/source-materials/current-system/`.
- Нормализованные feature-контейнеры созданы в `features/approvals`, `features/artifacts`, `features/deployments`, `features/packages`, `features/pilots`, `features/roles`, `features/scorecards`, `features/simulations`.
- Доменный baseline разложен в `baseline/current/domain/`.
- QA, retrospective, cross-cutting и task-catalog planning-контур вынесен в `planning/2026-Q2/quality-assurance/`, `planning/2026-Q2/retrospectives/`, `planning/2026-Q2/cross-cutting/`, `planning/2026-Q2/task-catalog/`.

## Карта верхнего уровня

| Legacy bucket | Что это было в changesWork | Где смотреть в standalone project |
|---|---|---|
| `final-spec/` | handoff bundle: requirements, доменная модель, gantt, прототип | `context/source-materials/current-system/requirements/raw/final-spec/`, `context/source-materials/current-system/diagrams/raw/`, `features/*`, `baseline/current/*` |
| `spec/` | ранние доменные и диаграммные спецификации | `context/source-materials/current-system/requirements/raw/spec/`, `context/source-materials/current-system/diagrams/raw/` |
| `docs/` | stakeholder/presentation/use-case материалы | `context/source-materials/current-system/requirements/raw/docs/` |
| `planning/mvp/current/gantt/` | legacy gantt views | `planning/2026-Q2/imported-source/gantt/` |
| `planning/mvp/current/tasks/` | legacy task docs и декомпозиция | `planning/2026-Q2/imported-source/tasks/`, а нормализованный вход — `planning/2026-Q2/task-catalog/` |
| `planning/mvp/current/tasks/legacy/` | старые подробные story/task breakdown | `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/`, а нормализованные части — в `features/`, `planning/2026-Q2/quality-assurance/`, `planning/2026-Q2/retrospectives/`, `planning/2026-Q2/cross-cutting/`, `baseline/current/ui/navigation.md`, `baseline/current/domain/contexts/lineage.md` |
| `prototypes/` | интерактивные html-макеты и архив вариантов | `context/source-materials/current-system/prototypes/raw/` и raw snapshot |
| `notes/` | ad-hoc решения, отчёты, эксперименты, служебные записи | `context/source-materials/legacy/changeswork-full/notes/` |
| `scripts/` | legacy automation и validators | `context/source-materials/legacy/changeswork-full/scripts/` |
| `archive/` | старые отчёты и исторические материалы | `context/source-materials/legacy/changeswork-full/archive/` |
| `memory/` | рабочая память старого проекта | `context/source-materials/legacy/changeswork-full/memory/` |
| `local-skills-marketplace/` | legacy marketplace/plugins для агентов | `context/source-materials/legacy/changeswork-full/local-skills-marketplace/` |
| `.claude/skills/` | локальные skills старого workflow | `context/source-materials/legacy/changeswork-full/.claude/skills/` |

## Что нормализовано не полностью

| Область | Что уже сделано | Что ещё остаётся |
|---|---|---|
| Current-state baseline | домен разложен по bounded contexts и aggregates | API/UI/data/requirements summary доведены до обзорного канона, но не до полной постраничной спецификации |
| Simulations | baseline признаёт `Simulation` как existing coverage и есть dedicated feature `features/simulations/` | simulation contracts всё ещё partly legacy-shaped и могут потребовать отдельной canonical URI/data normalization |
| Navigation + lineage auxiliary scope | sidebar baseline и lineage boundary вынесены в `baseline/current/ui/navigation.md` и `baseline/current/domain/contexts/lineage.md` | route-catalog и source-preview contracts можно ещё точнее свести при необходимости |
| QA / retrospectives | квартальный operational слой вынесен из raw legacy в отдельные planning-папки | если понадобится поминутный ход квартала, придётся идти в raw docs и gantt |
| Cross-cutting streams | `notifications` и `trace` вынесены в `planning/2026-Q2/cross-cutting/` как самостоятельные квартальные потоки | при желании можно дополнительно поднимать canonical delivered workspaces для этих потоков |
| Imported planning summaries | summary/task-order/alignment docs получили нормализованный вход через `planning/2026-Q2/task-catalog/` | raw imported docs всё равно остаются первичным историческим evidence |
| Release fixation | есть каркас release package | финальные delivered baseline-promotions нужно собирать по фактическим релизам |

## Практическое правило

Если не уверен, где искать правду:
1. для текущего deployed состояния — `baseline/current/`;
2. для рабочей дельты — `features/`;
3. для квартального planning/ops слоя — `planning/2026-Q2/`;
4. для исходных доказательств — `context/source-materials/current-system/`;
5. для полного исторического хвоста — `context/source-materials/legacy/changeswork-full/`.
