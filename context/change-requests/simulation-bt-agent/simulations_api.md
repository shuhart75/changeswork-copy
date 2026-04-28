# Вкладка "Основная информация"

**Страница:** https://confluence.delta.sbrf.ru/pages/viewpage.action?pageId=17649736393  
**Пространство:** CPCRM  
**Версия:** 24  
**Статус:** incomplete

---

## Бизнес-требования

Я, как пользователь системы, хочу иметь возможность посмотреть детали любой симуляции.

### Критерии приемки

8-18 - **не выполнены** (статус incomplete)

---

## Функциональные требования

### FE:

1. Необходимо реализовать новую форму просмотра симуляции разбив ее на вкладки.

### BE:

1. Реализовать новые API и логику работы с ними.

---

## Реализация для Frontend

### Описание UI

| Экран | Детали |
| --- | --- |
| image-2026-3-5_15-50-1.png | * В новом статусе нет статус бара * Отображается в вкладка "Основная информация" |
| image-2026-3-5_15-54-8.png | * В статусе "В работе" отображается статус бар процесса выполнения симуляции |

### Jira SberWorks: RSCON-2205

#### 1) Вкладки просмотра симуляции

Необходимо на форме просмотра симуляции реализовать возможность открытия нескольких вкладок:

* Основная информация
* Итоги симуляции

**Примечание:** В рамках данного требования будет идти речь про вкладку "Основная информация". Результаты в рамках других требований описаны.

#### 2) Вызов ручек при открытии режима просмотра симуляции

При открытии детальной формы симуляции необходимо вызывать ручку:

* **GET /api/v1/simulation/{number}** — Просмотр атрибутов симуляции

передавая на вход в параметрах номер симуляции.

#### 3) Выполнение симуляции

Необходимо добавить строку - динамический показатель стадии выполнения симуляции, значения которого будет меняться в зависимости от полученного статуса выполнения симуляции.

**Логика отрисовки статусной строки:**

```json
{
  "stages": [
    {
      "stepName": "Загрузка данных",
      "createDateTime": "2025-04-01T08:30:00Z",
      "updateDatetime": "2025-04-01T09:30:00Z"
    }
  ]
```

| Название атрибута | Использование на UI | Правила |
| --- | --- | --- |
| stepName | Отрисовываем полученное название шага | - |
| createDateTime | Отрисовавыем дату начала выполнения шага | Если даты нет, значит данный шаг еще не запускался |
| closeDatetime | Отрисовываем даты завершения выполнения шага | Если даты нет, значит данный шаг в процессе выполнения |

#### 4) Поля на форме просмотра симуляции

На форме просмотра отображаем те же поля, что и в режиме редактирования/создания, только в данном режиме ничего не доступно для редактирования.

| Имя поля | Наименование поля в API (JSON Path) | Пояснение |
| --- | --- | --- |
| **Основная форма** | | |
| Пространство симуляции | `$.spaces[:].description` | |
| Название симуляции | `$.name` | |
| Описание симуляции | `$.description` | |
| Версия сборки стратегии | `$.strategyVersion` | |
| Режим симуляции | `$.mode` | |
| **Фильтрация выборки** | | |
| **Период данных** | | |
| Дата начала | `$.startDate` | |
| Дата завершения | `$.endDate` | |
| Количество отбираемых записей | `$.maxRec` | |
| | `$.filters[:].name` | **Верхнеуровнево:** отображаем наименование, полученное в данном атрибуте. |
| | `$.filters[:].values` | под названием перечисляем все значения, как выбранные, полученные в массиве values[] |
| **Изменение риск-параметра**: необходимо динамически настраивать, для разного продукта разные столбцы | | |
| Риск-параметр | `$.riskParameters[:].name` | |
| Текущее значение(низ) | `$.riskParameters[:].originHigherValue` | |
| Новое значение(низ) | `$.riskParameters[:].userLowerValue` | |
| Текущее значение(верх) | `$.riskParameters[:].originHigherValue` | если значения не получены, то не отрисовываем столбцы. Данные значения только для пространства ПК используются, поэтому так |
| Новое значение(верх) | `$.riskParameters[:].userHigherValue` | |
| Дата активации | `$.riskParameters[:].activationDate` | |

---

## Реализация для Backend

| Сервис | ПКАП1200 АС КОДА |
| --- | --- |
| ИФТ URL | https://ci07642362-eiftgen1dm-rscon-iamproxy.apps.ift-gen1-dm.delta.sbrf.ru |
| База данных | [Структура данных](https://confluence.delta.sbrf.ru/pages/viewpage.action?pageId=12828906632) |
| Методы | https://apistudio-iamosh.sigma.sbrf.ru/#/projects/41304/specs/swagger/115250/165132/editor |

### Jira SberWorks: RSCON-2206

#### 5) БД

К таблице **SIMULATIONS** добавить новое поле:

| Column | Type | Size | Nulls | Источник | Comments |
| --- | --- | --- | --- | --- | --- |
| ADDITIONAL_PROPERTIES | JSONB | | Yes | ФП Симуляция | Параметры симуляции |
| STATUS_DESCRIPTION | VARCHAR | 2000 CHAR | Yes | ФП Симуляция | Дополнительная информация по статусу |

#### 6) API

Необходимо реализовать новую ручку:

| | |
| --- | --- |
| **Сервис просмотра симуляции** | |
| **GET** | /api/v1/simulation/{number} |
| **Parameters** | number |
| **path** | /api/v1/simulation/{id}?spaceCode={spaceCode} |

```json
{
  "id": "string",
  "number": "SIM-CC-117",
  "name": "string",
  "mode": "risk_params_change",
  "status": "NEW",
  "statusDescription": "string",
  "author": "string",
  "createDateTime": "2026-03-05T12:56:01.281Z",
  "updateDateTime": "2026-03-05T12:56:01.281Z",
  "space": {
    "id": "string",
    "status": "ACTUAL",
    "code": "CC",
    "departmentCode": "ДРРБ",
    "version": 2,
    "baselineSize": 1.25,
    "description": "Кредитные карты",
    "sticky": true
  },
  "externalId": "string",
  "description": "string",
  "strategyVersion": "string",
  "startDate": "2026-03-05",
  "endDate": "2026-03-05",
  "maxRec": 10,
  "btLink": "string",
  "releaseEffects": "string",
  "releaseDescription": "string",
  "releaseStartDate": "2026-03-05",
  "filters": [
    {
      "name": "Канал продаж",
      "code": "sales_channel",
      "values": ["DSA", "ВСП"]
    }
  ],
  "riskParameters": {
    "releaseVersion": "string",
    "snapshotId": "string",
    "riskParameters": [
      {
        "userLowerValue": 0,
        "userHigherValue": 0,
        "activationDate": "2026-03-05",
        "name": "string",
        "originLowerValue": 0,
        "originHigherValue": 0
      }
    ]
  },
  "availableActions": ["edit", "delete"],
  "stages": [
    {
      "stepName": "Загрузка данных",
      "createDateTime": "2025-04-01T08:30:00Z",
      "updateDatetime": "2025-04-01T09:30:00Z"
    }
  ]
}
```

##### 6.1. Аудит

Необходимо реализовать отправку информации в аудит по факту вызовов новых ручек.

#### 7) Логика работы с API и БД

Необходимо реализовать логику получения и передачи детальной информации симуляции, при вызове метода GET /api/v1/simulation/{number} на фронт.

**Sequence diagram:**
```
Frontend -> Backend: GET /api/v1/simulation/{number}
Backend -> DB: Селект симуляции
DB --> Backend: OK
Backend --> Frontend: Ответ
```

#### 8) Интеграция с ФП Симуляция: получение деталки

Реализовать вызовы новой ручки ФП Симуляция и логику работы с ней:

| Возможные действия со симуляцией | Вызываемый метод | Триггер |
| --- | --- | --- |
| Получение детальной формы симуляции | GET /api/v1/simulations/{simulation_id} | * Вызов фронтом метода GET /api/v1/simulation/{number} для симуляции в статусе IN_PROGRESS и DEPLOYING_PROGRESS * Выполнение периодической задачи обновления детальной формы симуляции в статусе IN_PROGRESS и DEPLOYING_PROGRESS |

### Jira SberWorks: RSCON-2207

Необходимо реализовать логику получения детальной формы симуляции для симуляций в статусах = **IN_PROGRESS, IN_PROGRESS_TO_CANCELLED, DEPLOYING**

**Успешный ответ:**

**Маппинг:**

| Элемент | Маппинг с БД | Маппинг с наш API | Описание элемента | Тип | Кратность | Примечание |
| --- | --- | --- | --- | --- | --- | --- |
| configSimulation.id | - | - | ID симуляции | String format: uuid | [1] | Уникальный идентификатор симуляции |
| configSimulation.product | SIMULATIONS.SPACE_CODE | code | Продукт | String maxLength: 255 | [1] | cc - кредитные карты |
| configSimulation.type | SIMULATIONS.SIMULATION_MODE | mode | Режим запуска | String maxLength: 255 | [1] | risk_params_change |
| configSimulation.strategy | SIMULATIONS.STRATEGY_VERSION | strategyVersion | Версия стратегии | String maxLength: 255 | [1] | actual |
| configSimulation.name | SIMULATIONS.NAME | name | Наименование | String maxLength: 255 | [1] | |
| configSimulation.description | SIMULATIONS.DESCRIPTION | description | Описание | String maxLength: 3000 | [0..1] | |
| configSimulation.employeeNumber | SIMULATIONS.EMPLOYEE_NUMBER | employeeNumber | ID пользователя | String maxLength: 255 | [0..1] | |
| configSimulation.status | SIMULATIONS.STATUS | Статус | String | [0..1] | in_progress, error, cancelled, completed, deployed |
| configSimulation.createDatetime | SIMULATIONS.CREATE_DATETIME | - | дата и время создания | String format: date-time | [0..1] | |
| configSimulation.updateDatetime | SIMULATIONS.UPDATE_DATETIME | - | дата и время обновления | String format: date-time | [0..1] | |
| configSimulation.statusBar | **Сохраняем всю информацию в формате json в SIMULATIONS.ADDITIONAL_PROPERTIES** | | Набор шагов | | [0..N] | |
| filtersStatic | - | - | Фильтрация выборки | | | |
| riskParamsChange | **Сохраняем всю информацию в формате json** | | Изменение риск параметров | | [0..1] | |
| results | - | - | Результаты симуляции | | [0..1] | |

**Пример ответа:**
```json
{
  "configSimulation": {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "product": "cc",
    "type": "risk_params_change",
    "strategy": "actual",
    "name": "Тестовая симуляция",
    "description": "Тестовая симуляция (детальное описание)",
    "employeeNumber": "1321234",
    "status": "in_progress",
    "createDatetime": "2024-01-15T09:35:00.000+03:00",
    "updateDatetime": "2024-01-15T09:35:00.000+03:00",
    "statusBar": [
      {
        "orderNum": 0,
        "step": "прогон стратегии as_is",
        "createDatetime": "2024-01-15T09:30:00.000+03:00",
        "closeDatetime": "2024-01-15T09:35:00.000+03:00"
      }
    ]
  },
  "filtersStatic": {
    "salesChannel": "8",
    "clientGroup": "A",
    "searchStart": "2018-01-01",
    "searchEnd": "2018-01-02",
    "maxRec": 0
  },
  "riskParamsChange": [
    {
      "name": "pti_cap",
      "lowerCurrentValue": "0.01",
      "lowerNewValue": "0.02",
      "hightCurrentValue": "1.01",
      "hightNewValue": "1.02",
      "activationDate": "2018-01-02"
    }
  ],
  "results": {
    "raw": "Симуляция завершена успешно. Показатель ХХХ = 100.3."
  }
}
```

**Ответ с ошибкой:**

| Элемент | Описание | Тип | Кратность | Примечание | Маппинг |
| --- | --- | --- | --- | --- | --- |
| errorCode | Код ошибки | String maxLength: 255 | [0..1] | 1 - Записи не найдены | Код ошибки |
| errorMessage | Описание ошибки | String maxLength: 255 | [0..1] | | |
| errorDescription | Дополнительная информация | String maxLength: 2000 | [0..1] | | |

```json
{
  "errorCode": "1",
  "errorMessage": "Записи не найдены",
  "errorDescription": "ErrorDescription"
}
```

##### Периодическая задача

Необходимо реализовать периодическую задачу, которая будет раз в 10 минут интегрировать с ФП Симуляция вызывая метод получения детальной формы симуляции в статусах IN_PROGRESS, IN_PROGRESS_TO_CANCELLED, DEPLOYING

**Сценарий взаимодействия:**
```
Backend -> DB: Получаем все EXTERNAL_ID для симуляций в нужном статусе
DB --> Backend: EXTERNAL_ID
Backend --> FP: Запрашиваем по всем EXTERNAL_ID деталку GET /simulation/{id}
FP --> Backend: Responses
Backend -> DB: Обновляем данные
DB --> Backend: ОК
```

**Логика обновления данных:**

1. В таблице **SIMULATIONS** находим все записи с `is_last=true` и `status = IN_PROGRESS, IN_PROGRESS_TO_CANCELLED, DEPLOYING`
2. У полученных записей извлекаем `EXTERNAL_ID`
3. Выполняем запросы в ФП Симуляция по каждому полученному `EXTERNAL_ID`
4. По каждому полученному ответу проверяем поменялся ли статус симуляции:
   - Если статус не поменялся — обновляем текущую запись
   - Иначе создаем новую запись с `is_last=true`, предыдущей указываем `is_last=false`

### Jira SberWorks: RSCON-2210

#### 9) Уведомление

Необходимо реализовать отправку уведомления о завершении выполнения симуляции автору.

| Тип уведомления | Триггер | Получатели | Шаблон письма |
| --- | --- | --- | --- |
| Оповещение о завершении выполнения симуляции | Переход статуса симуляции с **IN_PROGRESS** на **ERROR** или **COMPLETED** | Получаем почтовый адрес пользователя SIMULATIONS.EMPLOYEE_NUMBER | **Заголовок:** Оповещение о завершении выполнения симуляции в АС КОДА<br>**Текст:** Уважаемый пользователь, сообщаем, что выполнение симуляции ${simulationNumber} завершено. |

**HTML код:**
```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8"/>
  <title>Оповещение о завершении выполнения симуляции в АС КОДА</title>
</head>
<body style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; background-color: #fafafa; padding: 20px;">
  <p>Уважаемый пользователь,<br> сообщаем, что выполнение симуляции <strong>${simulationNumber}</strong> завершено.</p>
</body>
</html>
```