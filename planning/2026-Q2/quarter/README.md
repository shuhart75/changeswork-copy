# 2026-Q2

## Notes

Этот квартал импортирован из legacy-проекта `changesWork`.
Raw planning-артефакты лежат в `../imported-source/`.
Рабочие gantt views лежат в `../gantt/`.
Нормализованные operational layers лежат в:
- `../quality-assurance/`
- `../retrospectives/`

## Scope Decisions

- legacy gantt и task docs скопированы без изменения оригинала;
- planning stories и implementation tasks разнесены по новому формату только частично;
- QA и retrospective контур вынесен из raw snapshot в отдельные planning-папки, чтобы он не терялся среди feature docs.

## Comparison Notes

Сверку legacy-плана и новой структуры лучше делать по feature lanes.
Отдельно проверяем:
- `gantt/` — что было запланировано и что фактически двигалось;
- `quality-assurance/` — что считалось обязательным тестовым охватом;
- `retrospectives/` — какие управленческие checkpoints были задуманы внутри квартала.
