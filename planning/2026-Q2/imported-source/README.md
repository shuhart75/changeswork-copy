# Imported planning source — 2026-Q2

Это curated planning-layer, извлечённый из legacy `changesWork` для квартала `2026-Q2`.

## Что лежит рядом

- `gantt/` — legacy PlantUML gantt views, использовавшиеся как историческая база для нового quarter/commander/actual-progress.
- `tasks/` — summary-level planning docs, полезные для восстановления исходной квартальной декомпозиции.
- `notes/` — planning laws и поясняющие README из legacy.

## Что важно понимать

- Это не новый source of truth. Канонические рабочие gantt-файлы теперь лежат в `planning/2026-Q2/gantt/`.
- Imported source нужен для сверки, трассировки и восстановления утерянных planning-решений.
- Более подробные legacy task docs, включая simulation-related breakdown, лежат в `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/`.

## Нормализация по состоянию на сейчас

- `approvals`, `deployments`, `packages`, `scorecards` уже имеют feature lanes в новом формате;
- simulation-related baseline coverage подтверждён как existing system behavior, но отдельный planning-slice в harness не поднимался;
- альтернативные commander/current variants (`opt2/opt3/opt4`, aggressive actualization и т.п.) оставлены raw, без автоматической нормализации.
