# changeswork-copy

Рабочий проект, использующий `analyst-harness` для планирования, требований, прототипов, актуализации факта и релизной фиксации.

## Как работать с обвязкой

Начинать с `AGENTS.md` и `.workflow/llm-contract.md`. Активный режим хранится в `.workflow/active-mode.md`; режим является границей допустимых правок.

Основные пользовательские команды:

- `новая фича`
- `занимаемся планированием`
- `делаем требования`
- `делаем презентационный прототип`
- `делаем прототип для разработки`
- `обновляем прогресс`
- `финализируем релиз`

Дополнительные команды по ролям:

- `спланируй фичу`
- `возьми срез в разработку`
- `разбери срез по коду`
- `предложи план реализации`
- `подготовь проверки по срезу`
- `собери негативные сценарии`
- `сверь проверки с требованиями`

Полный список фраз: `.workflow/command-catalog.md` и `.workflow/command-cheatsheet.md`.

## Работа с малым контекстным окном

Пользователь не должен вручную просить LLM собрать контекст, обновить чекпойнт или исследовать срез. Обвязка делает это автоматически под предметные команды.

Основные вспомогательные артефакты:

- `features/<feature>/context-summary.md`
- `features/<feature>/artifact-map.md`
- `features/<feature>/planning/planning-context.md`
- `features/<feature>/slices/<slice>/context-summary.md`
- `features/<feature>/slices/<slice>/.research/summary.md`
- `features/<feature>/slices/<slice>/implementation-handoff.md`
- `features/<feature>/slices/<slice>/execution/implementation-plan.md`
- `features/<feature>/slices/<slice>/testing/test-plan.md`

Эти файлы помогают LLM продолжать работу на больших требованиях, но не заменяют источник истины. Принятые решения должны переноситься в требования, планирование, прототипы, задачи, релизный пакет или baseline.

## Проверки

```bash
python .workflow/tools/validate-structure.py .
python .workflow/tools/validate-links.py .
python .workflow/tools/validate-context.py .
```

После изменений gantt:

```bash
python .workflow/tools/sync-quarter-gantt.py planning/2026-Q2/gantt
```
