# Domain Impact — approvals

Дата обновления: `2026-05-27`
Baseline target: `baseline/current/domain/`

## Decision registry

| Decision ID | Summary | Status | Consistency level | Source | Supersedes | Reverted by |
|---|---|---|---|---|---|---|
| DEC-2026-04-23-APPROVALS-001 | Approval route создаётся динамически: 0..* approval stages + 1 ratification stage, recall допустим на любом этапе | superseded | domain-wide | `features/approvals/slices/core-process/requirements/backend.md` |  |  |
| DEC-2026-05-25-APPROVALS-SBERDOCS-001 | Approval/ratification workflow выносится в SberDocs; АС КОДА хранит `new`-версию до отправки, integration snapshot и read-only status; историю читает on demand | accepted | domain-wide | `features/approvals/requirements.md` | DEC-2026-04-23-APPROVALS-001, DEC-2026-04-23-PACKAGES-001 |  |
| DEC-2026-05-27-APPROVALS-SBERDOCS-DOCX-002 | SberDocs document создаётся как DOCX без `restrictions` и без `route.executorList`; скоркарта и `Доп. эффекты` не входят в DOCX и используются для HTML-письма; backend ловит переход к подписанию по `documentState = ON_APPROVAL`, подтверждает `APPROVAL/IN_WORK` в approval sheet и скачивает актуальный DOCX из SberDocs | accepted | local | `features/approvals/requirements.md` | частично уточняет DEC-2026-05-25-APPROVALS-SBERDOCS-001 |  |
| DEC-2026-05-29-APPROVALS-AV-NOTIFICATION-003 | HTML-уведомление отправляется на фиксированный адрес `av@av.ru`; методолог может отправить его вручную после submit, автоматическая отправка выполняется только если ручной не было, а в письмо включаются значимые участники из справочника по данным approval sheet | accepted | local | `features/approvals/requirements.md` | уточняет DEC-2026-05-27-APPROVALS-SBERDOCS-DOCX-002 |  |

## Changed bounded contexts

- `Approval`
- `Integration / SberDocs`
- `Research and Execution` host entities that show approval status

## New or changed aggregates

- `ApprovalChain` — локальный агрегат версий брифа, участников отправки и SberDocs integration snapshot; не является собственным workflow engine.
- `ApprovalChainVersion` — неизменяемый snapshot JSON документа, поля `Доп. эффекты`, подписанта, получателей, автора/соавтора и отправки в SberDocs; изменение этих данных создаёт новую версию.
- `sberdocs_snapshot` внутри версии — integration snapshot: `jobId`, `documentId`, `systemNumber`, `approvalSheetId`, mapped status, last sync; URL строится по конфигурируемому шаблону.
- `significant_signer_dictionary` — справочник значимых подписантов/согласовантов для включения в AV-уведомление; не является маршрутом согласования.
- `Package` как workflow/grouping aggregate отменён для MVP.

## Business rules and invariants

- JSON документа является центральной частью `ApprovalChain`; изменение документа, `Доп. эффекты`, подписанта или получателей создаёт новую локальную версию до отправки.
- Отправленная версия read-only в АС КОДА; документ и маршрут могут штатно меняться в SberDocs.
- Пока существует связка доменного элемента и `ApprovalChain`, действия с доменным элементом в АС КОДА запрещены; пользователь выполняет правки/решения в SberDocs по ссылке.
- Raw `REJECTED` не возвращает локальную цепочку в `new`: он маппится в `on_approval`, а повторная отправка выполняется в SberDocs.
- Raw `ON_DELETING` и `DELETED` переводят локальную цепочку в terminal status `cancelled`; возврат в `new` после создания SberDocs-документа в MVP не выполняется.
- Raw `CANCELLED` после `approved` не понижает локальный статус: АС КОДА сохраняет raw snapshot/audit, но оставляет результат согласованным.
- Бриф хранится как JSON; DOCX Renderer генерирует DOCX только из документной части JSON, без скоркарты и без `Доп. эффекты`, и DOCX передаётся как `documentFile.content = base64(DOCX)`.
- Скоркарта и `Доп. эффекты` используются для предпросмотра и итогового HTML-письма на `av@av.ru`, но не для документа SberDocs.
- Документ создаётся без `restrictions.actions`; АС КОДА не запрещает редактирование документа/маршрута в SberDocs.
- АС КОДА не устанавливает признак `Коммерческая тайна (К2)` через API; документ создаётся как есть, пользователь устанавливает К2 в SberDocs, submit из-за К2 не блокируется.
- `route.executorList` в SberDocs не передаётся; backend передаёт только `senderList`, `recipientList`, `author`, `additionalAuthorList[]` и `summary`.
- Backend ведёт справочник значимых участников и при отправке AV-уведомления включает всех участников из справочника, которые уже приняли участие в согласовании по данным SberDocs approval sheet.
- Методолог может вручную отправить HTML-уведомление на `av@av.ru` после submit; после ручной отправки автоматическая отправка по этой версии не выполняется.
- Если ручной отправки не было, backend во время polling ловит `documentState = ON_APPROVAL`, затем читает `approval-sheet`: `taskType = AGREEMENT` игнорирует как триггер email, а активную задачу подписания определяет по `taskType = APPROVAL` + `taskState = IN_WORK` и отправляет HTML-письмо один раз на `av@av.ru`.
- Актуальный DOCX после согласования получается из SberDocs через `document-files`, локальная копия файла не хранится.
- После успешной отправки SberDocs является источником статусов и решений; история и комментарии читаются on demand из approval sheet без локального хранения.
- АС КОДА не предоставляет действия `approve`, `reject`, `ratify`, `sign`; пользователь выполняет их в SberDocs.
- Отзыв/редактирование уже созданного документа выполняется в интерфейсе SberDocs методологом-автором или ПРМ-соавтором; АС КОДА не показывает кнопку отзыва в MVP.
- АС КОДА маппит статусы SberDocs на локальные read-only статусы и статусы host entity.
- Перед критическими запросами к SberDocs backend выполняет `health-check`; только `LIVING` допускает submit, polling и on-demand чтение истории.
- При провале health-check SberDocs или неизвестном/unexpected SberDocs status backend отправляет дедуплицированное email-уведомление на поддержку АС[СТ, РСП, КОДА, СРО].
- Отдельная страница `Согласования` и пакетные сценарии не входят в MVP.

## State transitions

- `new` -> `sending_to_sberdocs` -> `on_approval` -> `approved`.
- Raw `REJECTED` остаётся в `on_approval`; raw `ON_DELETING` / `DELETED` переводят в `cancelled`; raw `CANCELLED` после `approved` не меняет local lifecycle.
- Альтернативные terminal states: `cancelled`, `sberdocs_create_error`, `sberdocs_unknown`.
- Для host entity локальный `ON_APPROVAL` сохраняется как отображение mapped status, а не как собственный workflow state machine.

## API and integration impact

- Внешние SberDocs методы: `GET /public/Gateway/health-check`, `POST /public/Gateway/document-job`, `GET /public/Gateway/document-job/{jobId}/state`, `GET /public/Gateway/document/{documentId}/state`, `GET /public/Gateway/approval-sheet/{approvalSheetId}`, `GET /public/Gateway/document/{documentId}/document-files`; при необходимости отображения фактического К2 или диагностики также `GET /public/Gateway/document/{documentId}/actual-info` и `GET /public/Gateway/document/{documentId}/document-files-archive`.
- Основной документ создаётся как DOCX без `restrictions`, скоркарты и `Доп. эффекты`; `summary` = краткое содержание, `senderList` = подписант, `recipientList` = получатели, `author` = методолог-отправитель, `additionalAuthorList[]` = ПРМ-соавтор.
- Требуется внутренний API АС КОДА для сохранения `new`-версии, submit to SberDocs, ручной отправки AV-уведомления, status snapshot, sync и on-demand approval sheet; recall в АС КОДА не входит в MVP; resubmit из raw `REJECTED`, `ON_DELETING` и `DELETED` запрещён.
- Старые внутренние endpoints `POST /api/v1/approval-chains`, `POST /api/v1/approval-chains/{id}/action`, `POST /api/v1/packages`, `POST /api/v1/packages/{id}/action` не входят в MVP.

## Affected requirements

| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/requirements.md` | root feature scope switched to SberDocs integration | propagated |
| `features/approvals/slices/core-process/requirements/backend.md` | native workflow replaced by SberDocs DOCX integration, signer notification, actual document download and status mapping | propagated |
| `features/approvals/slices/core-process/requirements/frontend.md` | UI switched to new-version/submit/read-only monitoring/on-demand history, signer notification marker and actual DOCX download; recall only via SberDocs UI | propagated |
| `features/approvals/slices/page/requirements/frontend.md` | separate approvals page cancelled | propagated |
| `features/approvals/slices/page/requirements/backend.md` | page API cancelled | propagated |
| `features/packages/requirements.md` | package feature cancelled for MVP | propagated |
| `features/packages/slices/page/requirements/frontend.md` | package UI cancelled | propagated |
| `features/packages/slices/page/requirements/backend.md` | package API cancelled | propagated |
| `features/deployments/requirements.md` | host lifecycle/status wording should reference SberDocs mapped status | open |

## Affected baseline artifacts

| Path | Impact | Sync status |
|---|---|---|
| `baseline/current/domain/contexts/approval.md` | native approval aggregate and package rules are superseded | open |
| `baseline/current/domain/business-rules.md` | approval owner/status source changes to SberDocs | open |
| `baseline/current/api/README.md` | old approval/package endpoints should be removed from target MVP API | open |
| `baseline/current/ui/README.md` | approvals page navigation should be removed/deprecated | open |

## Affected prototypes

### Scope prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/planning/scope-prototype/prototype.html` | should show SberDocs submit/monitoring instead of native approval page | defer-ok |
| `features/packages/planning/scope-prototype/prototype.html` | package prototype is obsolete for MVP | obsolete |

### Delivery prototypes
| Path | Impact | Sync status |
|---|---|---|
| `features/approvals/slices/core-process/delivery-prototype/prototype.html` | should show brief/signing participants submit and read-only SberDocs state | defer-ok |
| `features/approvals/slices/page/delivery-prototype/prototype.html` | separate approvals page obsolete | obsolete |
| `features/packages/slices/page/delivery-prototype/prototype.html` | package page obsolete | obsolete |

## Required consistency actions

- [x] local feature requirements updated
- [x] neighboring package requirements updated
- [x] domain impact reviewed by main agent
- [ ] baseline impact updated or backlog item created
- [x] affected prototypes listed
- [ ] planning stories/estimates updated in planning mode
- [ ] release package updated when applicable

## Rollback notes

- До релиза: можно вернуть native approval/package model, отменив `DEC-2026-05-25-APPROVALS-SBERDOCS-001` и восстановив `DEC-2026-04-23-APPROVALS-001` / `DEC-2026-04-23-PACKAGES-001`.
- После релиза: откат возможен только новым change/release item с миграцией SberDocs links/status snapshots.

## Promotion targets

- `baseline/current/domain/contexts/approval.md`
- `baseline/current/domain/business-rules.md`
- `baseline/current/api/README.md`
- `baseline/current/ui/README.md`
