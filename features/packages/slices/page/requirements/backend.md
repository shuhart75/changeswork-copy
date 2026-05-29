# Страница "Пакеты" (Backend)

Статус: **исключено из MVP**  
Область: MVP  
Дата обновления: 2026-05-25  
Decision ID: `DEC-2026-05-25-APPROVALS-SBERDOCS-001`

## Решение

Backend package flow не реализуется. Согласование/утверждение выполняется в SberDocs, а АС КОДА не создаёт локальные пакеты и не выполняет batch decisions.

## Superseded scope

Отменены:

- модель `Package` как группировка `ApprovalInstance`;
- `GET /api/v1/packages/queue`;
- `POST /api/v1/packages`;
- `GET /api/v1/packages/{id}`;
- `POST /api/v1/packages/{id}/action`;
- package brief;
- package history;
- пересчёт пакета при индивидуальных решениях.

## Новый backend источник

Backend должен использовать approvals SberDocs integration из `features/approvals/slices/core-process/requirements/backend.md`:

- draft маршрута/брифа;
- submit to SberDocs;
- SberDocs status/history snapshot.

## Критерии приемки отмены

- [ ] В OpenAPI MVP отсутствуют package endpoints.
- [ ] В БД MVP не требуется таблица package для approval/ratification.
- [ ] Нет статуса `awaiting_ratification` как очереди пакетирования.
- [ ] Package-related старые examples не используются в acceptance/API документах.
