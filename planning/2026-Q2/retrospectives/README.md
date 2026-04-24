# Retrospectives — 2026-Q2

Дата обновления: `2026-04-24`
Статус: **нормализовано из legacy planning**
Источник: `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_retrospectives.md`

## Зачем этот слой нужен

Legacy `changesWork` содержал отдельный operational plan по ретроспективам для фаз квартала.
Это не продуктовые требования и не execution tasks, а управленческий контур обратной связи по ходу квартала.

## Общая модель ретроспективы

Для каждой фазы использовался один и тот же базовый каркас:
- команда: аналитики, backend, frontend, QA; заказчик опционально;
- формат: `Start-Stop-Continue` или `Mad-Sad-Glad`;
- длительность: `2-3 часа`;
- обязательный выход: action items, ответственные, метрики, корректировка следующей фазы.

## Фазы

| Фаза | Legacy id | Основной фокус |
|---|---|---|
| 1 | `RETRO-1` | базовые списки и detail pages |
| 2 | `RETRO-2` | новые списки, формы, Excel export |
| 3 | `RETRO-3` | lifecycle, approval flow, notifications |
| 4 | `RETRO-4` | detail/form экраны `Change` и `Scorecard` |
| 5 | `RETRO-5` | страницы `Packages` и `Approvals`, batch-логика |

## Важные акценты legacy

- Для `RETRO-3` и `RETRO-5` отдельно подчёркивался критический путь квартала.
- Во всех фазах нужно было собирать план/факт, количество багов, velocity и отклонение от оценок.
- Ретроспектива должна была влиять на дальнейшее квартальное планирование, а не существовать отдельно от него.

## Как использовать сейчас

- Если нужно восстановить operational context квартала, смотрим сюда и в raw legacy файл.
- Если нужно зафиксировать lessons learned в новом цикле, лучше писать их уже в новом planning layer текущего квартала, а этот слой оставлять как historical reference.
