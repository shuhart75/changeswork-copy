# Migration Notes — tabular-risk-parameters

Дата: `2026-05-04`

## Что перенесено
- legacy-блок `Табличные риск-параметры (за рамками MVP)` выделен в отдельную feature;
- generic planning-контур `BE_RISK_TABLE` / `FE_RISK_TABLE` нормализован в planning stories;
- actualized backlog `RSCON-2429`, `RSCON-2430`, `RSCON-2431`, `RSCON-2432` признан каноническим execution-слоем для этой feature;
- follow-up `RSCON-2452` включён в тот же feature-поток как продолжение backend-контура.

## Почему сейчас
- контур уже живёт реальными Jira-задачами;
- без отдельной feature он терялся между legacy gantt и текущими execution-обновлениями;
- пользователь явно попросил вытащить его в актуальные планы и features.

## Принятое упрощение
- на первом шаге feature фиксируется с одним core slice для execution-трекинга;
- requirement packs и delivery prototype будут подниматься отдельно, когда пользователь переведёт работу в соответствующие режимы.
