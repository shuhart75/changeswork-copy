# Cross-cutting stream — Notifications

Дата обновления: `2026-04-24`
Источники:
- `context/source-materials/legacy/changeswork-full/planning/mvp/current/tasks/legacy/mvp_tasks_notifications.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_projectlibre_alignment.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_execution_order.md`
- `planning/2026-Q2/imported-source/tasks/mvp_tasks_list_no_analytics.md`

## Почему это отдельный stream

В legacy-плане `notifications` были выделены в самостоятельную дорожку:
- `AN_NOT` — аналитика событий, шаблонов и получателей;
- `BE_NOT` — backend-реализация уведомлений.

Это не отдельная бизнес-фича для пользователя и не отдельный экран. Это сквозная инфраструктура вокруг жизненных циклов и approval flow.

## Legacy scope

### Аналитика (`AN_NOT`)
- перечень событий, которые должны триггерить уведомления;
- шаблоны писем;
- список получателей по каждому сценарию.

### Backend (`BE_NOT`)
- email-уведомления по approval / ratification / package-related событиям;
- уведомления о переходах `Pilot` и `Deployment`;
- HTML-шаблоны писем;
- история уведомлений в БД;
- API получения списка уведомлений и отметки прочитанности.

## Типовые события из legacy
- отправка на согласование;
- согласование / утверждение;
- отклонение с причиной;
- отзыв с согласования;
- активация пилота;
- внедрение deployment;
- rollback deployment.

## Где этот stream проявляется в новой структуре

Нормализованный контейнер не поднимался как отдельная `feature/`, потому что фактическое поведение размазано по нескольким областям:
- `features/approvals/`
- `features/packages/`
- `features/pilots/`
- `features/deployments/`
- `planning/2026-Q2/quality-assurance/phase-3.md`
- `planning/2026-Q2/quality-assurance/final-mvp.md`

## Граница нормализации

На текущем этапе в standalone project фиксируем именно planning-layer смысл:
- это отдельный квартальный stream;
- он зависим от approval/package/lifecycle контуров;
- он не является самостоятельной feature-папкой с own prototype.

Если позже понадобится canonical delivered scope по уведомлениям, логично будет поднимать уже отдельный cross-cutting workspace, а не притворяться, что это локальная часть только одной фичи.
