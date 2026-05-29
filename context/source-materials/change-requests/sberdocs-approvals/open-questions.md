# Открытые вопросы по интеграции SberDocs

Дата обновления: `2026-05-26`  
Источник: `meeting.txt` от 2026-05-25 является источником правды для снятых вопросов; `сбердокс.yaml` остаётся формальным API-контрактом.

## Уже принято после встречи

- Обязательный набор методов MVP:
  - `POST /public/Gateway/document-job` — создать задание на создание документа;
  - `GET /public/Gateway/document-job/{jobId}/state` — дождаться `COMPLETED` и получить `documentId`/`systemNumber`, либо получить `FAILED`/`VALIDATION_ERROR`;
  - `GET /public/Gateway/document/{documentId}/state` — получить текущий `documentState`, `stateName`, `systemNumber`, `approvalSheetId`;
  - `GET /public/Gateway/approval-sheet/{approvalSheetId}` — получить поимённую историю участников и комментарии;
  - `GET /public/Gateway/document/{documentId}/actual-info` — использовать при необходимости проверки `privacyList`/регистрационных атрибутов;
  - `GET /public/Gateway/document/{documentId}/document-files-archive` — использовать только для диагностики неизменности файла.
- Бриф формируется в АС КОДА как HTML snapshot, затем backend рендерит PDF и передаёт PDF как основной `documentFile.content = base64(PDF)`.
- HTML напрямую в SberDocs не отправляем: в YAML нет `HTML` в `FileExtension`, а SberDocs ожидает файл с корректным `extension`.
- В MVP не прикладываем внешние файлы: `attachmentList` не используем.
- Созданный SberDocs-документ не редактируем: `PUT /public/Gateway/document/{documentId}/document-header` в MVP не используем, потому что метод не рекомендован новым потребителям и будет пересматриваться.
- Повторное согласование после отзыва/отклонения создаёт новую локальную версию `ApprovalChain` и новый документ через `POST /public/Gateway/document-job`.
- Документ создаём с `restrictions.actions` из `headers.txt`, чтобы запретить редактирование основного документа, файлов/приложений и вида информации.
- Прямой API-способ установки `Коммерческая тайна (К2)` через `POST /public/Gateway/document-job` не подтверждён; ближайший рабочий вариант — отдельный вид/шаблон документа SberDocs с дефолтным видом информации К2 и последующая проверка через `actual-info`.
- `author` в SberDocs = автор внедрения.
- `senderList` = подписанты/утверждающие; подписанта не надо дублировать в `route.executorList`, SberDocs сам добавляет его в конец маршрута.
- `route.executorList` = согласующие; одинаковый `sortOrder` означает параллельное согласование, разные значения задают последовательность этапов.
- `recipientList` = получатели документа после регистрации/на исполнение; это не согласующие. Если отдельного получателя нет, допустимый fallback — автор документа.
- `externalDocumentId` задаёт АС КОДА; это наш внешний номер/ключ документа.
- `documentId` появляется после `document-job/{jobId}/state = COMPLETED`.
- URL SberDocs, как правило, не возвращается API; АС КОДА строит ссылку по конфигурируемому шаблону из `documentId`.
- При `jobState = FAILED` или `VALIDATION_ERROR` текущую job продолжить нельзя: нужно учесть ошибку, исправить данные и создать новую job.
- При отклонении/замечаниях основной источник комментариев — `ApprovalSheetResponse.nodeList[].comment`; специального статуса «согласовано с замечаниями» может не быть.
- `ApprovalSheetResponse.nodeList` формируется постепенно: будущие последовательные участники могут отсутствовать до создания их задач.
- Отзыв/приостановка в SberDocs может выполняться автором/соавтором/заместителем в UI SberDocs; отдельный public API отзыва в текущем YAML не найден.
- Страница `Согласования`, package flow и native approval actions в АС КОДА не входят в MVP.

## Оставшиеся вопросы / риски к подтверждению

| # | Сценарий использования | Метод SberDocs | Поле / часть контракта | Что нужно уточнить |
|---:|---|---|---|---|
| 1 | Создание документа с К2 | `POST /public/Gateway/document-job`, затем `GET /public/Gateway/document/{documentId}/actual-info` | request body `kind`; response body `privacyList` | Будет ли для АС КОДА создан отдельный вид/шаблон документа SberDocs с дефолтным `Коммерческая тайна (К2)`, какой `kind` передавать и можно ли проверять К2 через `actual-info.privacyList` на ИФТ. |
| 2 | Создание документа: регистрационные атрибуты | `POST /public/Gateway/document-job` | request body `registration` | Передаём ли `registration` в MVP. Если да — каким точным способом: через `registrarList` с табельным номером сотрудника в нужном подразделении или через другой атрибут SberDocs; риск — один регистратор может относиться к нескольким подразделениям. |
| 3 | Создание документа: вид документа | `POST /public/Gateway/document-job` | request body `kind` | Подтвердить итоговый вид документа: `DIVISION_ORDER` или отдельный вид/шаблон для АС КОДА, особенно если нужен дефолтный К2. |
| 4 | Создание документа: внешний ключ | `POST /public/Gateway/document-job` | request body `externalDocumentId` | Зафиксировать формат внешнего ключа: id версии внедрения, `approvalChainId + versionNumber` или другой устойчивый бизнес-ключ. |
| 5 | Синхронизация процесса | `GET /public/Gateway/document-job/{jobId}/state`, `GET /public/Gateway/document/{documentId}/state`, `GET /public/Gateway/approval-sheet/{approvalSheetId}` | polling policy backend АС КОДА | Интервал polling, timeout, число попыток, наличие ручной кнопки `Обновить статус`, stop condition после `REGISTERED`/`EXECUTION`/`EXECUTED`. |
| 6 | Отзыв из АС КОДА | Endpoint отзыва не найден в текущем YAML | remote recall contract | Если бизнес требует полноценный отзыв из АС КОДА при активном SberDocs-документе, нужен подтверждённый endpoint SberDocs. Иначе в MVP АС КОДА возвращает `409 Conflict` и просит выполнить отзыв в SberDocs. |
| 7 | Проверка неизменности PDF | `GET /public/Gateway/document/{documentId}/document-files-archive` | response body `archiveFile.content`, ZIP contents | Нужна ли в MVP автоматическая проверка SHA-256 PDF после создания/согласования или достаточно хранить хэш и использовать archive method только для диагностики. |
| 8 | Production-подключение | Организационный CR/анкета интеграции | список используемых методов, сертификаты, JWT/ТУЗ | Нужно оформить изменение интеграционной анкеты/архитектуры: добавить `document-job`, `document state`, `approval sheet`, possibly `actual-info`/`document-files-archive`, а также подтвердить ТУЗ/сертификаты/IFT-настройки. |
