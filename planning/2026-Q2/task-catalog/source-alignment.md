# Source alignment — 2026-Q2 MVP scope

Дата обновления: `2026-04-24`
Источник: `planning/2026-Q2/imported-source/tasks/mvp_tasks_projectlibre_alignment.md`

## Роль документа

Это главный summary-документ imported planning layer.
Он связывает ProjectLibre-декомпозицию, аналитические задачи, dev-задачи и QA в одном месте.

## Что он фиксирует
- состав команды и ресурсы (`A1`, `A2`, `B1..B3`, `F1`, `F2`, `Q1`);
- полный список MVP-задач;
- scope каждой задачи, а не только её id и оценку;
- добавленные поверх `Q2.pod` элементы: аналитика, QA, внедрения.

## Главные streams
- roles;
- artifacts;
- approvals / ratification / packages;
- deployments;
- scorecards;
- notifications;
- trace;
- QA.

## Важные выводы
- `Deployments` были добавлены в MVP поверх исходного `Q2.pod` как обязательный слой.
- `Notifications` и `Trace` были самостоятельными квартальными stream'ами, а не просто сносками в требованиях других фич.
- Этот документ остаётся лучшей отправной точкой, когда LLM нужно восстановить квартальный scope без чтения всего raw gantt.
