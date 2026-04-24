# Prototype Fix - Duplicate Variable Declaration

**Дата:** 2026-03-11

---

## Проблема

После добавления emotion библиотек прототип всё ещё не открывался.

**Ошибка в консоли:**
```
Uncaught SyntaxError: Identifier 'mockDeployments' has already been declared. (865:14)
```

---

## Причина

В файле было **две декларации** переменной `mockDeployments`:
- Строка 474: `const mockDeployments = [...]` - содержала данные **инициатив**
- Строка 976: `const mockDeployments = [...]` - содержала данные **внедрений**

Первая декларация была ошибочной - переменная должна была называться `mockInitiatives`, так как содержала данные инициатив (Initiative), а не внедрений (Deployment).

**Доказательство:**
```javascript
// Строка 474 - данные инициатив
const mockDeployments = [  // ← НЕПРАВИЛЬНОЕ ИМЯ
    {
        id: 1,
        name: 'Оптимизация риск-стратегии Premium карт',
        status: 'deployed',
        author: 'Иванов И.И.',
        statusCalculated: true,
        statusReason: 'Внедрение #1 в статусе deployed',
        // Это поля Initiative, не Deployment!
    }
]

// Строка 976 - данные внедрений
const mockDeployments = [  // ← ПРАВИЛЬНОЕ ИМЯ
    {
        id: 1,
        name: 'Внедрение новой скоркарты Premium',
        deployedAt: null,
        deploymentConfig: { rollout_percentage: 100 },
        rollbackPlan: 'Автоматический откат...',
        // Это поля Deployment
    }
]
```

---

## Решение

Переименована первая декларация в `mockInitiatives`:

```javascript
// Строка 474
const mockInitiatives = [  // ← ИСПРАВЛЕНО
    {
        id: 1,
        name: 'Оптимизация риск-стратегии Premium карт',
        // ...
    }
]
```

---

## Проверка

### 1. Валидация прототипа

```bash
python3 scripts/validate_prototype.py prototypes/current.html
```

**Результат:**
```
✓ Все зависимости подключены
✓ Все CDN ссылки доступны
✓ Ошибок не найдено
```

### 2. Проверка дубликатов

```bash
grep -n "^        const mock" prototypes/current.html
```

**Результат:**
```
371:        const mockUsers = [
379:        const mockUserRoles = [
474:        const mockInitiatives = [      ← Исправлено
529:        const mockSimulations = [
609:        const mockScorecards = [
829:        const mockPilots = [
976:        const mockDeployments = [      ← Оригинал
1217:        const mockChains = [
1246:        const mockPackages = [
```

Все переменные уникальны ✓

### 3. Использование в коде

Переменная `mockInitiatives` уже использовалась в коде:
- Строка 466: `mockInitiatives.find(d => d.id === entity.initiativeId)`
- Строка 4087: `mockInitiatives.find(d => d.id === simulation.initiativeId)`
- Строка 4335: `mockInitiatives.find(d => d.id === pilot.initiativeId)`
- Строка 4567: `mockInitiatives.find(d => d.id === deployment.initiativeId)`
- И т.д.

Это подтверждает, что переменная должна была называться `mockInitiatives` с самого начала.

---

## Итоговые исправления прототипа

### Исправление 1: Добавлены emotion библиотеки

```html
<script crossorigin src="https://unpkg.com/@emotion/react@11/dist/emotion-react.umd.min.js"></script>
<script crossorigin src="https://unpkg.com/@emotion/styled@11/dist/emotion-styled.umd.min.js"></script>
```

**Причина:** Material-UI v5 требует emotion как peer dependency

### Исправление 2: Переименована переменная

```javascript
const mockDeployments = [  // Было
const mockInitiatives = [  // Стало
```

**Причина:** Дублирование имени переменной

---

## Статус

**Прототип исправлен и готов к использованию.**

Все синтаксические ошибки устранены:
- ✓ Emotion библиотеки добавлены
- ✓ Дубликаты переменных устранены
- ✓ Валидация проходит успешно

---

**Работа завершена:** 2026-03-11
