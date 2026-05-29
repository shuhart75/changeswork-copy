# Страница "Согласования" (Backend)

Статус: **исключено из MVP**  
Область: MVP  
Дата обновления: 2026-05-27  
Decision ID: `DEC-2026-05-25-APPROVALS-SBERDOCS-001`

## Решение

Backend API отдельной страницы `Согласования` не реализуется. Источник назначений, решений и статусов — SberDocs. АС КОДА хранит `ApprovalChain` с версиями брифа, участников отправки и integration snapshot; approval sheet читает по запросу без локального хранения.

## Superseded scope

Следующий прежний scope отменён:

- `GET /api/v1/approval-chains` для списков назначений;
- `GET /api/v1/approval-chains/{id}` для собственной деталки процесса;
- `POST /api/v1/approval-chains/{id}/action`;
- `POST /api/v1/approval-chains/bulk-action`;
- package-related карточки на странице `Согласования`;
- собственное хранение решений как workflow source of truth.

## Новый backend scope

Актуальный backend scope находится в `../core-process/requirements/backend.md` и включает:

- `approval_chain` / `approval_chain_version`;
- `sberdocs_snapshot` внутри версии;
- отправку `DocumentJobRequest` в SberDocs;
- синхронизацию `DocumentJobStateResponse`, `DocumentStateResponse` и on-demand чтение `ApprovalSheetResponse`;
- status mapping и audit.

## Критерии приемки отмены

- [ ] В MVP OpenAPI АС КОДА нет endpoints для списка назначений согласующего.
- [ ] В MVP OpenAPI АС КОДА нет endpoints для `approve/reject/ratify`.
- [ ] Старые `ApprovalChain` response examples не используются в новых требованиях.
- [ ] История, показанная в АС КОДА, загружается из SberDocs approval sheet отдельным методом и не хранится локально.

## Консистентность

Если downstream-компоненту нужен статус согласования, он должен читать snapshot по target entity, а не обращаться к page API страницы `Согласования`.
