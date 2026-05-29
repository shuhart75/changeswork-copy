# FEATURE-APPROVALS — Согласования через SberDocs

Статус: **в работе / scope updated**
Квартал: `2026-Q2`
Дата обновления: `2026-05-27`

## Цель

Минимизировать собственную разработку согласований в АС КОДА: хранить версии брифа и участников отправки, создавать DOCX-документ для SberDocs и дальше отображать read-only статус и on-demand историю из SberDocs.

## Контекст

Feature была импортирована из `changesWork` как native approval/ratification workflow. Новое решение `DEC-2026-05-25-APPROVALS-SBERDOCS-001` supersedes native модель: согласующие и подписант принимают решения в SberDocs, а АС КОДА остаётся контуром подготовки и мониторинга.

## Ideal scope

- подготовка JSON документа, поля `Доп. эффекты`, подписанта и получателей в АС КОДА с версионированием `ApprovalChain`;
- генерация DOCX через backend DOCX Renderer из документной части JSON без скоркарты и `Доп. эффекты`, передача DOCX как основного документа;
- предпросмотр и отправка HTML-письма на `av@av.ru` из JSON документа, скоркарты, `Доп. эффекты` и значимых участников из SberDocs approval sheet;
- создание документа в SberDocs: `summary`, `senderList`, `recipientList`, `author` = методолог-отправитель, `additionalAuthorList[]` = ПРМ-соавтор; согласующие настраиваются в SberDocs и локально не хранятся;
- синхронизация статуса документа и on-demand получение листа согласования из SberDocs;
- справочник значимых подписантов/согласовантов и включение в письмо всех участников из справочника, успевших согласовать к моменту отправки;
- ручная отправка уведомления методологом после submit с отключением последующей автоматической отправки;
- определение перехода к подписанию по `documentState = ON_APPROVAL`, подтверждение активной задачи `APPROVAL/IN_WORK` и автоматическая отправка HTML-письма на `av@av.ru`, если ручной отправки не было;
- получение актуального DOCX-документа из SberDocs после согласования;
- отображение `systemNumber`, ссылки, статуса и истории на host screens;
- аудит отправки и синхронизации.

## MVP scope

- локальный `ApprovalChain` с `new`-версией брифа и участников отправки до SberDocs;
- новая версия `ApprovalChain` при изменении брифа, подписанта, получателей до отправки или после ошибки создания SberDocs-документа без `documentId`; после создания SberDocs-документа raw `ON_DELETING`/`DELETED` переводит цепочку в `cancelled`, а не в `new`;
- health-check SberDocs перед submit/polling/on-demand history;
- email-уведомление поддержки АС[СТ, РСП, КОДА, СРО] при провале health-check SberDocs или unknown/unexpected SberDocs status;
- submit в SberDocs через backend;
- `restrictions.actions` не передаются, редактирование документа/маршрута остаётся штатной возможностью SberDocs;
- polling `document-job` и `document state`; approval sheet читается отдельным методом;
- HTML-письмо на `av@av.ru`: вручную по кнопке методолога после submit либо автоматически при `documentState = ON_APPROVAL` и активной задаче `APPROVAL/IN_WORK`, если ручной отправки не было;
- справочник значимых участников для включения в письмо по данным `approval-sheet`;
- получение актуального DOCX из SberDocs через backend после согласования;
- маппинг SberDocs statuses в статусы АС КОДА;
- read-only status и on-demand history на host screen;
- блокировка действий доменного элемента на всё время существования связанного `ApprovalChain`, кроме будущих явно описанных исключений;
- отзыв/редактирование документа выполняется в SberDocs автором/соавтором, кнопки отзыва в АС КОДА MVP нет.

## Что исключено из MVP

- отдельная страница `Согласования`;
- собственные действия `approve`, `reject`, `ratify`, `sign` в АС КОДА;
- локальный `ApprovalChain` как workflow engine;
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

- зависимость от SLA и доступности SberDocs; health-check должен вернуть `LIVING` перед критическими запросами, а при провале backend уведомляет поддержку АС[СТ, РСП, КОДА, СРО];
- нужны согласованные профили `type`, `kind`, `externalDocumentSource`;
- признак К2 не устанавливается через API; пользователь должен установить К2 в интерфейсе SberDocs после создания документа;
- нужно согласовать mapping неизвестных `documentState/taskState` значений;
- baseline, deployments wording, planning stories и прототипы синхронизируются отдельными задачами.

## Решение по кварталу

- [x] берём в квартал как SberDocs integration scope
- [ ] переносим
- [ ] дробим дополнительно
