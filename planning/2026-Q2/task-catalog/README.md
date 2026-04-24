# Task catalog — 2026-Q2

Дата обновления: `2026-04-24`
Статус: **нормализовано из imported planning summaries**

## Зачем этот слой нужен

`planning/2026-Q2/imported-source/tasks/` хранит полезные, но legacy-shaped summary docs.
Чтобы ими было удобно пользоваться в новом workflow, здесь собран нормализованный вход в эти материалы:
- что считать главным source alignment документом;
- где смотреть execution order;
- где лежит короткий task inventory;
- какие вне-MVP дорожки были обозначены в плане.

## Что внутри

| Файл | Назначение | Legacy источник |
|---|---|---|
| `source-alignment.md` | главный summary по scope, ролям и task ids | `mvp_tasks_projectlibre_alignment.md` |
| `execution-order.md` | краткий порядок запуска потоков | `mvp_tasks_execution_order.md` |
| `inventory.md` | список задач без аналитики | `mvp_tasks_list_no_analytics.md` |
| `summary.md` | high-level заметки по плану v6.15/v6.16 | `mvp_tasks_summary.md` |
| `artifacts-core.md` | отдельный note по artifacts core | `mvp_tasks_artifacts_core.md` |

## Как использовать

- Для восстановления квартального planning scope начинаем с `source-alignment.md`.
- Для быстрой оценки очередности задач смотрим `execution-order.md`.
- Для быстрого списка исполненческих задач без аналитики — `inventory.md`.
- Для точных legacy формулировок остаётся `planning/2026-Q2/imported-source/tasks/`.
