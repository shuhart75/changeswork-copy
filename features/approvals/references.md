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

- АС КОДА готовит бриф, подписанта и получателей, но само согласование/утверждение и настройка согласующих выполняются в SberDocs. Перед критическими запросами backend проверяет `GET /public/Gateway/health-check`; продолжать можно только при `status = LIVING`.
- АС КОДА хранит `ApprovalChain` с версиями брифа и участников отправки; после отправки версия read-only, SberDocs является источником статуса, а история читается по запросу из approval sheet.
- Бриф хранится как JSON: в DOCX-документ для SberDocs входят только поля документа, а скоркарта и поле `Доп. эффекты` не входят в DOCX и используются только для HTML-письма подписанту.
- DOCX Renderer генерирует DOCX из документной части JSON, и DOCX передаётся в SberDocs как основной `documentFile`; краткое содержание передаётся в `DocumentJobRequest.summary`; `restrictions.actions` не передаются; К2 через API не устанавливается, его ставит пользователь в SberDocs.
- `author` = методолог, отправивший на согласование; `additionalAuthorList[]` = ПРМ-соавтор; отзыв/редактирование документа выполняется в интерфейсе SberDocs, не в АС КОДА MVP.
- Во время polling backend определяет переход к подписанту по `document/state.documentState = ON_APPROVAL`; затем подтверждает активную задачу через `approval-sheet.nodeList[].taskType = APPROVAL` и `taskState = IN_WORK`, формирует HTML-письмо из JSON + скоркарты + `Доп. эффекты` и отправляет email. Актуальный DOCX после согласования скачивается из SberDocs через `document-files`.
- Отдельная страница `Согласования`, package flow и собственные action endpoints для решений исключаются из MVP.

## Legacy sources kept for history

- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approval_core.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_frontend.md`
- `context/source-materials/current-system/requirements/raw/final-spec/REQ_approvals_page_backend.md`
- `context/source-materials/current-system/prototypes/raw/approvals_page.html`

Legacy sources describe the pre-SberDocs native approval model and are superseded for current MVP requirements by `DEC-2026-05-25-APPROVALS-SBERDOCS-001`.
