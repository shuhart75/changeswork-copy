# changeswork-copy

Это копия и частичная раскладка legacy-проекта `changesWork` под новый workflow.

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
- raw requirements, diagrams и prototypes скопированы в `context/source-materials/current-system/`
- полный полезный snapshot legacy-репозитория сохранён в `context/source-materials/legacy/changeswork-full/`
- основные feature и slice-контейнеры созданы в `features/`
- legacy planning-артефакты скопированы в `planning/2026-Q2/imported-source/`
- canonical baseline domain model разложена в `baseline/current/domain/`
- добавлен release package skeleton для `releases/2026-Q2/rscon-2438/`

## Что ещё требует доработки
- промоушен итоговых требований из feature-level living docs в canonical baseline
- детальная раскладка current-state API/UI/data baseline
- заполнение release package по фактическим delivered изменениям
