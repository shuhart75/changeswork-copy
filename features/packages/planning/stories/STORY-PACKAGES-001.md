# STORY-PACKAGES-001

Feature: `features/packages/feature.md`  
Статус: **импортировано из legacy-плана**  
Дата обновления: `2026-04-23`

## Summary
Страница Пакеты и пакетирование awaiting ratification

## Description
Собрать пользовательский сценарий пакетирования: очередь элементов в `awaiting_ratification`, локальный множественный выбор, brief пакета, отправка пакета, блок `Мои пакеты` и read-only просмотр состава пакета.

## Ideal scope
Единый workspace для пакетного ratification-потока, включая queue, текущие активные пакеты, rejected/history bucket и переходы в связанные доменные сущности.

## MVP scope
- queue элементов для пакетирования;
- локальный выбор 2+ элементов;
- brief пакета;
- создание пакета без backend draft;
- `Мои пакеты`;
- read-only деталка пакета.

## Analyst anchor estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Team estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Agreed estimate
- AN: 2 человеко-дней
- FE: 10 человеко-дней
- BE: 0 человеко-дней
- QA: 0 человеко-дней
- Total: 12 человеко-дней

## Actualization state
- `virtual`

## Mapping mode
- `explicit`

## Replaced by implementation tasks
- none yet

## Residual virtual tasks on actual-progress
- none

## Dependencies and assumptions
- зависит от approval core и страницы `Согласования`;
- backend API для пакетов и queue уже зафиксирован в requirement packs;
- execution-перенос в реальные Jira-задачи ещё не выполнен.

## Notes for quarter planning
Planning story агрегирует текущий HLE-срез `packages` без дробления по ролям; execution-слой под story пока отражён virtual tasks `AN_PKG_BE`, `AN_PKG_FE`, `FE_PKG_PAGE`.
