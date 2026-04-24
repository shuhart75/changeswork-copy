# Source materials

Это слой сырых доказательств и исторического контекста. Он не является source of truth сам по себе.

## Канонические подкаталоги

- `current-system/` — curated raw-копии документов, диаграмм и прототипов, которые использовались для нормализации baseline.
- `legacy/changeswork-full/` — полная копия legacy-репозитория `changesWork` без `.git/`, `.claude/worktrees/` и `__pycache__/`.
- `change-requests/` — входящие новые запросы на изменение для следующих итераций.

## Что уже подтверждено

- Полнота `legacy/changeswork-full/` перепроверена сравнением с оригиналом `/home/reutov/Documents/AI/changesWork`.
- Текущая каноническая точка входа для raw current-state материалов — `context/source-materials/current-system/`.
- Исторический дубль `context/current-system/` оставлен как legacy-import mirror и не должен считаться каноническим сырьевым каталогом.

## Как использовать

- Нужен полный исторический контекст — начинай с `legacy/changeswork-full/`.
- Нужны материалы для baseline normalization — начинай с `current-system/`.
- Нужна карта соответствий old -> new — смотри `legacy/changeswork-map.md`.
