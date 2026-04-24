# Улучшения API шаблонов скоркарт

## Дата: 2026-03-21

## Изменения в структуре API

### 1. Группировка индикаторов по секциям

**Было:**
```json
{
  "fields": {
    "indicators": [
      {
        "code": "launch_new_credit_product",
        "label": "...",
        "type": "boolean",
        "required": true
      }
    ]
  }
}
```

**Стало:**
```json
{
  "fields": {
    "indicator_sections": [
      {
        "section_id": "always_high",
        "title": "Критичные изменения",
        "description": "Любое значение «Да» автоматически устанавливает высокую критичность",
        "empty_text": "Во всём блоке значения только «Нет».",
        "fields": [
          {
            "code": "launch_new_credit_product",
            "label": "...",
            "type": "boolean"
          }
        ]
      }
    ]
  }
}
```

**Обоснование:**
- В прототипе (`prototypes/scorecards_detail.html`) индикаторы разбиты на смысловые блоки с заголовками
- Секции имеют разное поведение UI (например, "всегда высокая критичность" vs "зависимые поля")
- Поле `empty_text` нужно для отображения подсказки, когда все поля в секции = false

### 2. Удалено поле `required` из индикаторов

**Было:**
```json
{
  "code": "launch_new_credit_product",
  "type": "boolean",
  "required": true
}
```

**Стало:**
```json
{
  "code": "launch_new_credit_product",
  "type": "boolean"
}
```

**Обоснование:**
- Все boolean-индикаторы обязательны по умолчанию (всегда должны иметь значение true/false)
- Поле `required` избыточно и создаёт путаницу
- Для финансовых эффектов (number) поле `required` сохранено, так как там оно имеет смысл

### 3. Удалено поле `final_rule` из `criticality_thresholds`

**Было:**
```json
{
  "criticality_thresholds": {
    "boolean_indicators_high_if_true": [...],
    "effect_thresholds": {...},
    "final_rule": "high_if_any_indicator_or_effect_high_else_low"
  }
}
```

**Стало:**
```json
{
  "criticality_thresholds": {
    "boolean_indicators_high_if_true": [...],
    "effect_thresholds": {...}
  }
}
```

**Обоснование:**
- Правило расчёта критичности одно и то же для всех шаблонов в MVP
- Нет необходимости передавать его в каждом ответе API
- Алгоритм документирован в спецификации API

### 4. Добавлено описание алгоритма расчёта критичности

В спецификацию добавлен явный алгоритм:

```
Алгоритм расчёта критичности:
- Критичность = `high`, если выполнено хотя бы одно из условий:
  - любой индикатор из `boolean_indicators_high_if_true` имеет значение `true`
  - любой финансовый эффект превышает порог из `effect_thresholds` (для полей с `comparison: "abs_gte"`)
- Критичность = `low` во всех остальных случаях
- Поля с `comparison: "not_applicable"` не участвуют в расчёте
```

## Преимущества новой структуры

1. **Соответствие UI**: API напрямую отражает структуру формы из прототипа
2. **Меньше дублирования**: убраны избыточные поля (`required` для boolean, `final_rule`)
3. **Гибкость**: легко добавить новые секции с разным поведением
4. **Читаемость**: структура самодокументируемая через `title`, `description`, `empty_text`
5. **Разделение ответственности**:
   - `fields` — структура формы
   - `default_values` — данные по умолчанию
   - `criticality_thresholds` — бизнес-логика расчёта

## Обратная совместимость

Это breaking change для фронтенда, но так как MVP ещё не реализован, изменения безопасны.

## Файлы изменены

- `final-spec/REQ_scorecards_backend.md`:
  - Секция "ФТ-7. Технические API загрузки шаблона скоркарты"
  - OpenAPI схема `DefaultScorecardConfigResponse`
  - Примеры запросов/ответов
