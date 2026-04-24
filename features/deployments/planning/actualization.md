# Actualization map

Feature: `features/deployments/feature.md`  
Quarter: `2026-Q2`  
Baseline: `commander-plan`

## Правила
- `materialized` используем, когда planning story уже живёт в actual-progress как набор реальных Jira-задач.
- `mixed` используем, когда часть story уже заменена real tasks, а часть ещё видна как virtual residual.
- Для imported legacy-кейса mapping зафиксирован явно, чтобы actual-progress был читаемым и отвечал на вопрос "успеваем или нет".

## Mapping

| Story ID | Summary | Baseline Start | Baseline Duration (дн) | Actualization State | Mapping Mode | Replaced By | Residual Virtual Tasks | Depends On |
|---|---|---|---:|---|---|---|---|---|
| STORY-DEPLOYMENTS-001 | Backend foundation для внедрений | 2026-04-14 | 8 | materialized | explicit | RSCON-2349, RSCON-2445 |  |  |
| STORY-DEPLOYMENTS-002 | Жизненный цикл внедрений | 2026-04-15 | 8 | materialized | explicit | RSCON-2410 |  |  |
| STORY-DEPLOYMENTS-003 | Список внедрений | 2026-04-20 | 8 | materialized | explicit | RSCON-2346 |  |  |
| STORY-DEPLOYMENTS-004 | Форма создания и редактирования | 2026-04-20 | 15 | materialized | explicit | RSCON-2348, RSCON-2445 |  |  |
| STORY-DEPLOYMENTS-005 | Детальная страница и связанные блоки | 2026-04-21 | 20 | mixed | inferred | RSCON-2347 | AN-CHD1, BE-CHD1 |  |
