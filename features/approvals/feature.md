# FEATURE-APPROVALS — Согласования через SberDocs

Статус: **в работе / scope updated**
Квартал: `2026-Q2`
Дата обновления: `2026-06-01`

## Цель

Минимизировать собственную разработку согласований в АС КОДА: хранить версии брифа и участников отправки, создавать DOCX-документ для SberDocs и дальше отображать read-only статус, историю и актуальный документ из SberDocs.

## Контекст

Feature была импортирована из `changesWork` как native approval/ratification workflow. Новое решение `DEC-2026-05-25-APPROVALS-SBERDOCS-001` supersedes native модель: согласующие и подписант принимают решения в SberDocs, а АС КОДА остаётся контуром подготовки, отправки и мониторинга.

## Ideal scope

- подготовка JSON документа, поля `Доп. эффекты`, подписанта и получателей в АС КОДА с версионированием `ApprovalChain`;
- генерация DOCX через backend DOCX Renderer из документной части JSON без скоркарты и `Доп. эффекты`;
- предпросмотр HTML-письма, совпадающего по составу с реальным письмом подписанту;
- создание документа в SberDocs через `document-job` с `summary`, `senderList`, `recipientList`, `author` и `additionalAuthorList[]`;
- синхронное получение `documentId`, `systemNumber` и ссылки на документ в ответ на успешный submit;
- дальнейший polling `document/state` и on-demand чтение `approval-sheet`;
- автоматическая отправка письма текущему подписанту, когда в `approval-sheet` появляется активная задача `APPROVAL` со статусом `IN_WORK`;
- получение актуального DOCX из SberDocs после согласования, потому что документ может быть изменён в SberDocs;
- отображение mapped status, истории и ссылки на SberDocs на host screen;
- аудит отправки, синхронизации, health-check и интеграционных ошибок.

## MVP scope

- локальный `ApprovalChain` с `new`-версией брифа и участников отправки до SberDocs;
- новая версия `ApprovalChain` при изменении брифа, подписанта или получателей до отправки; после отправки версия read-only;
- периодический health-check SberDocs в фоне; при сбое или деградации уходит уведомление на поддержку АС[СТ, РСП, КОДА, СРО];
- submit в SberDocs через backend без `route.executorList`, без `attachmentList` и без `restrictions.actions`;
- `author` = методолог-отправитель, `additionalAuthorList[]` = ПРМ-соавтор;
- К2 через API не ставится; пользователь устанавливает признак в интерфейсе SberDocs после создания документа;
- polling `document-job` в рамках submit до получения `documentId/systemNumber`, затем регулярный polling `document/state`;
- read-only статус, on-demand история, скачивание актуального DOCX и ссылка `Открыть в SberDocs` на host screen;
- автоматическое письмо подписанту без ручной отправки и без отдельного UI-статуса письма;
- блокировка действий доменного элемента на всё время существования связанного `ApprovalChain`, кроме будущих явно описанных исключений;
- отзыв/редактирование документа выполняется только в SberDocs автором/соавтором.

## Что исключено из MVP

- отдельная страница `Согласования`;
- собственные действия `approve`, `reject`, `ratify`, `sign` в АС КОДА;
- локальный `ApprovalChain` как workflow engine;
- передача списка согласующих из АС КОДА и локальное хранение этапов маршрута SberDocs;
- ручная отправка письма из интерфейса АС КОДА;
- редактирование уже созданного SberDocs-документа из интерфейса АС КОДА;
- package flow и массовые решения;
- собственная реализация ЭП/КЭП.

## Входные материалы

- `references.md`
- `requirements.md`
- `slices/core-process/requirements/frontend.md`
- `slices/core-process/requirements/backend.md`
- `context/source-materials/change-requests/sberdocs-approvals/`

## Planning stories

- `planning/stories/STORY-APPROVALS-001.md` — требует planning-синхронизации под SberDocs.
- `planning/stories/STORY-APPROVALS-002.md` — legacy page story, исключена из MVP и требует planning-синхронизации.

## Риски и зависимости

- зависимость от SLA и доступности SberDocs; backend отдельно мониторит `health-check`, но не блокирует каждый business-вызов предварительной проверкой;
- нужно согласовать значения `type`, `kind`, `externalDocumentSource` и формат `externalDocumentId` для `document-job`;
- DOCX в формате base64 не должен превышать лимит SberDocs `10 МБ`;
- признак К2 не устанавливается через API; пользователь должен поставить его вручную в SberDocs;
- если подписант будет заменён в SberDocs, backend должен определить актуального адресата письма по активной задаче `APPROVAL/IN_WORK`, а не по исходному `senderList`;
- baseline, deployments wording, planning stories и прототипы синхронизируются отдельными задачами.

## Решение по кварталу

- [x] берём в квартал как SberDocs integration scope
- [ ] переносим
- [ ] дробим дополнительно
