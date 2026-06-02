# Slice — Интеграция согласования со SberDocs

Статус: **в работе**
Feature: `features/approvals/feature.md`
Порядок в feature requirements: `01`
Дата обновления: `2026-06-01`

## Назначение

Описать минимальный MVP-процесс: АС КОДА хранит `ApprovalChain` с версиями JSON документа, поля `Доп. эффекты` и участников отправки, передаёт в DOCX Renderer только документную часть без скоркарты и `Доп. эффекты`, создаёт новый документ SberDocs без запрета редактирования и без передачи согласующих, получает `documentId` и `systemNumber` в submit, дальше отображает read-only статус из SberDocs API, по запросу получает историю и актуальный DOCX, автоматически отправляет письмо текущему подписанту по активной задаче `APPROVAL/IN_WORK`, маппит `ON_DELETING`/`DELETED` в `cancelled` и уведомляет поддержку при сбое фонового health-check или unknown status.

## Связанные planning stories

- `STORY-APPROVALS-001` — требует отдельной planning-синхронизации под SberDocs.

## Источники

- `../../references.md`
- `../../requirements.md`
- `context/source-materials/change-requests/sberdocs-approvals/`

## Пакеты требований

- `../../requirements.md`
- `requirements/frontend.md`
- `requirements/backend.md`

## Связанные прототипы

- `delivery-prototype/prototype.html` — требует актуализации под read-only статус и отсутствие ручной отправки письма.

## Связанные execution-артефакты

- `execution/tasks.md` — требует отдельной execution/planning-синхронизации после пересмотра scope.
