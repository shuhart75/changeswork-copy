# changeswork-copy

Это копия и раскладка legacy-проекта `changesWork` под новый workflow.

## Быстрый вход для работы с LLM

Смотри в первую очередь:

- `.workflow/command-cheatsheet.md` - готовые формулировки команд
- `.workflow/command-catalog.md` - как LLM должна их интерпретировать
- `.workflow/templates/intake/` - шаблон preflight для команды `новая фича`
- `.workflow/templates/requirements/` - шаблоны requirement packs

Базовые команды:

- `новая фича`
- `занимаемся планированием`
- `делаем требования`
- `делаем презентационный прототип`
- `делаем прототип для разработки`
- `обновляем прогресс`
- `финализируем релиз`

Пример:

```text
новая фича
Источник: `/home/reutov/Documents/AI/simulations_AI_agent`
Квартал: `2026-Q2`
```

```text
обновляем прогресс
RSCON-2445 завершена вчера.
Добавь milestone релиза на 2026-04-30 и обнови actual-progress.
```

## Что теперь есть в структуре
- `baseline/current/` — каноническое описание текущей системы
- `planning/` — квартальные планы и gantt
- `planning/intake/` — preflight-заметки до создания новой feature
- `features/` — рабочие дельты: требования, прототипы, execution tracking
- `releases/` — итоговые релизные пакеты перед промоушеном в baseline
- `context/source-materials/` — сырые импортированные материалы и evidence

## Что уже сделано
- raw snapshot legacy-репозитория перенесён полностью в `context/source-materials/legacy/changeswork-full/`
- полнота snapshot перепроверена сравнением с `/home/reutov/Documents/AI/changesWork`
- current-system requirements / diagrams / prototypes разложены в `context/source-materials/current-system/`
- основные feature и slice-контейнеры, включая `features/simulations/`, созданы в `features/`
- legacy planning-артефакты вынесены в `planning/2026-Q2/imported-source/`
- canonical baseline domain model разложена в `baseline/current/domain/`
- добавлены обзорные baseline summaries для `requirements`, `ui`, `api`, `data`, `decisions`
- release package skeleton добавлен для `releases/2026-Q2/rscon-2438/`

## Что ещё требует доработки
- дальнейшая детализация baseline/current на уровне full post-page contracts при необходимости
- promotion итоговых delivered требований из feature-level living docs в canonical baseline
- заполнение release package по фактическим delivered изменениям
