# Slice — Интеграция согласования со SberDocs

Статус: **в работе**
Feature: `features/approvals/feature.md`
Порядок в feature requirements: `01`
Дата обновления: `2026-05-27`

## Назначение

Описать минимальный MVP-процесс: АС КОДА хранит `ApprovalChain` с версиями JSON документа, поля `Доп. эффекты` и участников отправки, передаёт в DOCX Renderer только документную часть без скоркарты и `Доп. эффекты`, создаёт новый документ SberDocs без запрета редактирования и без передачи согласующих, дальше отображает read-only статус из SberDocs API, ведёт справочник значимых участников, отправляет HTML-уведомление на `av@av.ru` вручную по кнопке методолога либо автоматически при `documentState = ON_APPROVAL` + `APPROVAL/IN_WORK`, включает в письмо значимых участников из approval sheet, маппит `ON_DELETING`/`DELETED` в `cancelled`, уведомляет поддержку при health-check failure/unknown status и по запросу получает историю/актуальный DOCX из SberDocs.

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

- `delivery-prototype/prototype.html` — требует актуализации, текущее requirements-решение уже изменено.

## Связанные execution-артефакты

- `execution/tasks.md` — требует отдельной execution/planning-синхронизации после пересмотра scope.
