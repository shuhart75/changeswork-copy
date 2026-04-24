# Prototype Validator - Создан и применён

**Дата:** 2026-03-11

---

## Проблема

Прототип `prototypes/current.html` не открывался в браузере (пустая страница).

---

## Диагностика

Использован Explore агент для анализа проблемы:

**Найденная причина:**
Material-UI v5 требует **@emotion/react** и **@emotion/styled** как peer dependencies. Без них Material-UI не может инициализироваться, что приводит к пустой странице.

**Технические детали:**
1. Прототип загружал React 18, ReactDOM 18, Material-UI v5.14.20, Babel
2. НО отсутствовали @emotion/react и @emotion/styled
3. При попытке деструктурировать компоненты: `const { Box, Container, ... } = MaterialUI;`
4. Material-UI v5 UMD bundle внутренне зависит от emotion
5. Без emotion объект MaterialUI пустой или выбрасывает ошибки
6. React не может отрендерить App компонент
7. Результат: пустая страница без видимых ошибок

---

## Решение

### 1. Исправлен prototypes/current.html

Добавлены CDN ссылки на emotion библиотеки **перед** Material-UI:

```html
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<!-- Добавлены эти две строки -->
<script crossorigin src="https://unpkg.com/@emotion/react@11/dist/emotion-react.umd.min.js"></script>
<script crossorigin src="https://unpkg.com/@emotion/styled@11/dist/emotion-styled.umd.min.js"></script>
<!-- Затем Material-UI -->
<script src="https://unpkg.com/@mui/material@5.14.20/umd/material-ui.production.min.js"></script>
```

### 2. Обновлён scripts/validate_prototype.py

Добавлена проверка emotion зависимостей:

```python
# Проверка emotion (требуется для Material-UI v5)
if '@emotion/react' in content:
    print("✓ @emotion/react подключен")
else:
    print("✗ @emotion/react не найден (требуется для Material-UI v5)")

if '@emotion/styled' in content:
    print("✓ @emotion/styled подключен")
else:
    print("✗ @emotion/styled не найден (требуется для Material-UI v5)")
```

### 3. Создан prototype-validator skill

**Расположение:** `.claude/skills/prototype-validator/`

**Документация включает:**
- Типичные проблемы и решения
- Чеклист для создания новых прототипов
- Правильный порядок загрузки зависимостей
- Инструкции по отладке
- Best practices

---

## Проверка

### Валидация после исправления:

```bash
python3 scripts/validate_prototype.py prototypes/current.html
```

**Результат:**
```
=== Проверка зависимостей ===
✓ React 18 подключен
✓ Babel standalone подключен
✓ Material-UI подключен
✓ @emotion/react подключен          ← Теперь присутствует
✓ @emotion/styled подключен         ← Теперь присутствует
✓ Babel script присутствует

=== Проверка CDN ссылок ===
✓ https://unpkg.com/@emotion/react@11/dist/emotion-react.umd.min.js
✓ https://unpkg.com/@emotion/styled@11/dist/emotion-styled.umd.min.js
✓ Все остальные CDN ссылки

=== Итоги валидации ===
✓ Ошибок не найдено
```

---

## Критичный порядок загрузки

**ВАЖНО:** Зависимости должны загружаться в правильном порядке:

```
1. React
2. ReactDOM
3. @emotion/react    ← Требуется для Material-UI v5
4. @emotion/styled   ← Требуется для Material-UI v5
5. Material-UI
6. Babel
7. Ваш код (type="text/babel")
```

Неправильный порядок приведёт к ошибкам!

---

## Итоговый набор skills

После создания prototype-validator проект имеет **6 skills**:

1. **spec-sync v1.2** - Проверка синхронизации спецификации
2. **version-manager v1.0** - Управление версиями спецификации
3. **diagram-updater v1.0** - Проверка синхронизации PlantUML диаграмм
4. **task-generator v1.0** - Генерация задач разработки
5. **prototype-validator v1.0** - Валидация HTML прототипов
6. **project-consistency-manager** - Управление консистентностью проекта

---

## Использование prototype-validator

### Перед коммитом прототипа:

```bash
python3 scripts/validate_prototype.py prototypes/current.html
```

### При создании нового прототипа:

1. Использовать шаблон из `.claude/skills/prototype-validator/SKILL.md`
2. Проверить валидатором
3. Открыть в браузере и проверить консоль (F12)

### При проблемах с прототипом:

1. Запустить валидатор
2. Проверить типичные проблемы (см. SKILL.md)
3. Создать минимальный тест для изоляции проблемы

---

**Работа завершена:** 2026-03-11

**Результат:** Прототип исправлен и теперь корректно открывается. Создан skill для предотвращения подобных проблем в будущем.
