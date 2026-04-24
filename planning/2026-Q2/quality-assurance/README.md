# Quality Assurance — 2026-Q2

Дата обновления: `2026-04-24`
Статус: **нормализовано из legacy planning**

## Зачем этот слой нужен

Здесь собраны не продуктовые требования, а квартальный QA-план из legacy `changesWork`:
- что именно тестировали по фазам;
- какие интеграционные сценарии считались обязательными;
- какие deliverables ожидались от QA;
- где в legacy лежит исходный детальный материал.

Это не current baseline системы и не replacement для feature-level requirements. Это planning/execution слой квартала `2026-Q2`.

## Что внутри

| Нормализованный файл | Legacy источник | Что фиксирует |
|---|---|---|
| `phase-1.md` | `mvp_tasks_qa_phase1.md` | вход в QA-фазу v6.15 и привязку к gantt / alignment |
| `phase-2.md` | `mvp_tasks_qa_phase2.md` | тестирование новых списков и форм |
| `phase-3.md` | `mvp_tasks_qa_phase3.md` | backend lifecycle, approval flow и notifications |
| `phase-4.md` | `mvp_tasks_qa_phase4.md` | detail/form screens для Changes и Scorecards |
| `phase-5.md` | `mvp_tasks_qa_phase5.md` | deprecated-статус отдельной фазы |
| `final-mvp.md` | `mvp_tasks_qa_final.md` | итоговое e2e-тестирование MVP |

## Практическое правило

- Для восстановления квартального QA-плана начинаем отсюда.
- Для исходных формулировок и полного хвоста идём в `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/`.
- Для delivered/current truth по конкретной фиче идём в `features/*` и `baseline/current/*`.
