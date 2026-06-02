# References

## Current change request sources

- `context/source-materials/change-requests/sberdocs-approvals/Цепочка_согласования_Сравнение_подходов.md`
- `context/source-materials/change-requests/sberdocs-approvals/сбердокс.yaml`
- `context/source-materials/change-requests/sberdocs-approvals/Бриф для утверждения.md`
- `context/source-materials/change-requests/sberdocs-approvals/StateMachine_внутреннего_документа.md`
- `context/source-materials/change-requests/sberdocs-approvals/Бриф_для_утверждения.md` — legacy-версия, заменена файлом `Бриф для утверждения.md`.
- `context/source-materials/change-requests/sberdocs-approvals/Маршруты_согласований.md`
- `context/source-materials/change-requests/sberdocs-approvals/Согласование_Релизов_Риск_параметров.md`
- `context/source-materials/change-requests/sberdocs-approvals/meeting.txt`

## Accepted direction

- АС КОДА готовит бриф, подписанта и получателей, но само согласование/утверждение и настройка согласующих выполняются в SberDocs. `GET /public/Gateway/health-check` используется отдельным фоновым мониторингом backend, а не как обязательный pre-call gate перед каждым запросом.
- АС КОДА хранит `ApprovalChain` с версиями брифа и участников отправки; после отправки версия read-only, SberDocs является источником статуса, а история читается по запросу из `approval-sheet`.
- Бриф хранится как JSON: в DOCX-документ для SberDocs входят только поля документа, а скоркарта и поле `Доп. эффекты` не входят в DOCX и используются только для HTML-письма подписанту и его предпросмотра.
- DOCX Renderer генерирует DOCX из документной части JSON, и DOCX передаётся в SberDocs как основной `documentFile`; краткое содержание передаётся в `DocumentJobRequest.summary`; `restrictions.actions`, `route.executorList` и `attachmentList` в MVP не передаются; К2 через API не устанавливается, его ставит пользователь в SberDocs.
- `author` = методолог, отправивший на согласование; `additionalAuthorList[]` = ПРМ-соавтор; отзыв/редактирование документа выполняется в интерфейсе SberDocs, не в АС КОДА MVP.
- Во время polling backend определяет переход к подписанию по `document/state.documentState = ON_APPROVAL`, затем подтверждает активную задачу через `approval-sheet.nodeList[].taskType = APPROVAL` и `taskState = IN_WORK`, формирует HTML-письмо из JSON + скоркарты + `Доп. эффекты` и отправляет email текущему подписанту. Актуальный DOCX после согласования скачивается из SberDocs через `document-files`.
- Успешный submit возвращает frontend `documentId`, `systemNumber`, ссылку на документ и новый mapped status, чтобы UI сразу перешёл в read-only режим без отдельного шага ожидания.
- Отдельная страница `Согласования`, package flow и собственные action endpoints для решений исключаются из MVP.

## Legacy sources kept for history

- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md`
- `context/source-materials/current-system/prototypes/raw/approvals_page.html`

Legacy sources describe the pre-SberDocs native approval model and are superseded for current MVP requirements by `DEC-2026-05-25-APPROVALS-SBERDOCS-001` and `DEC-2026-06-01-APPROVALS-NOTIFICATION-004`.
