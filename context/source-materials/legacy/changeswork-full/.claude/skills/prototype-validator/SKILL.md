---
name: prototype-validator
description: Валидация и отладка HTML прототипов с React и Material-UI
version: 1.0
---

# Prototype Validator - Валидация HTML прототипов

Инструмент для проверки корректности HTML прототипов с React 18 и Material-UI v5.

## Использование

```bash
python3 scripts/validate_prototype.py prototypes/current.html
```

## Типичные проблемы

### 1. Пустая страница - отсутствуют emotion библиотеки

**Симптомы:** Пустая страница, нет ошибок в консоли

**Причина:** Material-UI v5 требует @emotion/react и @emotion/styled

**Решение:**
```html
<script crossorigin src="https://unpkg.com/@emotion/react@11/dist/emotion-react.umd.min.js"></script>
<script crossorigin src="https://unpkg.com/@emotion/styled@11/dist/emotion-styled.umd.min.js"></script>
```

### 2. Дублирование переменных

**Симптомы:** `Uncaught SyntaxError: Identifier 'X' has already been declared`

**Решение:**
```bash
# Найти дубликаты
grep -n "^        const " file.html | awk '{print $2}' | sort | uniq -c | awk '$1 > 1'
```

### 3. Устаревший React API

**Симптомы:** Warning в консоли

**Решение:**
```javascript
// React 18 API
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

## Правильный порядок зависимостей

```html
<script src="react@18"></script>
<script src="react-dom@18"></script>
<script src="@emotion/react@11"></script>
<script src="@emotion/styled@11"></script>
<script src="@mui/material@5"></script>
<script src="@babel/standalone"></script>
```

## Минимальный рабочий пример

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/@emotion/react@11/dist/emotion-react.umd.min.js"></script>
    <script crossorigin src="https://unpkg.com/@emotion/styled@11/dist/emotion-styled.umd.min.js"></script>
    <script src="https://unpkg.com/@mui/material@5.14.20/umd/material-ui.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const { Box, Typography } = MaterialUI;
        function App() {
            return <Box sx={{ p: 3 }}><Typography>Works!</Typography></Box>;
        }
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
```

## Отладка

1. Открыть консоль браузера (F12)
2. Проверить Network tab - все ли скрипты загрузились
3. Проверить Console tab - есть ли ошибки
4. Использовать минимальный пример для изоляции проблемы

## Best Practices

- Всегда проверяйте прототип валидатором перед коммитом
- Используйте локальный сервер: `python3 -m http.server 8000`
- Проверяйте консоль браузера при отладке
- Следуйте правильному порядку загрузки зависимостей
