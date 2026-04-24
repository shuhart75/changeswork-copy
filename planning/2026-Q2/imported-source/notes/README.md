# Система управления внедрениями риск-стратегий

**Версия:** 3.1  
**Статус:** В разработке

---

## Структура проекта

```
changesWork/
├── spec/                      # Актуальная спецификация
│   ├── domain_model.md       # Модель домена
│   ├── data_model.puml       # ER-диаграмма БД
│   ├── state_machine.puml    # Диаграммы состояний
│   ├── GUIDE.md              # Руководство для разработки
│   └── versions/             # Архив версий
│       ├── v3.0/
│       └── v3.1/
│
├── prototypes/                # HTML прототипы
│   ├── current.html          # Текущий прототип (MVP) -> mvp/prototype.html
│   ├── mvp/
│   │   └── prototype.html
│   └── archive/
│
├── Prototipes/                # Совместимость: старое имя папки (symlink -> prototypes/)
│
├── docs/                      # Документация
│   ├── executive_summary.md
│   ├── glossary.md
│   ├── faq_stakeholders.md
│   └── use_cases.md
│
├── planning/                  # Планирование разработки
│   └── mvp/
│       ├── current/          # Актуальная версия (symlink -> versions/*)
│       ├── tasks/            # Совместимость: symlink -> current/tasks
│       ├── gantt/            # Совместимость: symlink -> current/gantt
│       └── versions/         # Зафиксированные версии (v6.0/v6.1/v6.2)
│
├── notes/                     # Рабочие заметки
│   ├── TODO.md
│   └── DECISION_POINT.md
│
├── scripts/                   # Утилиты
│   ├── validate_prototype.py
│   └── reorganize_project.sh
│
├── final-spec/                # Пакет для передачи команде/демо (копии ключевых артефактов)
│   ├── README.md
│   └── prototype.html
│
├── .claude/                   # Claude Code конфигурация
│   └── skills/
│       ├── spec-sync/        # Синхронизация спецификации
│       └── project-consistency-manager/
│
└── archive/                   # Старые рабочие материалы
```

---

## Быстрый старт

### Для команды разработки

1. **Начните со спецификации:**
   ```bash
   # Прочитайте главные документы
   cat spec/domain_model.md
   cat spec/GUIDE.md
   ```

2. **Посмотрите диаграммы:**
   ```bash
   # Откройте PlantUML диаграммы
   plantuml spec/data_model.puml
   plantuml spec/state_machine.puml
   ```

3. **Изучите прототип:**
   ```bash
   # Откройте в браузере
   open prototypes/current.html
   ```

### Для работы над спецификацией

1. **Проверка синхронизации:**
   ```bash
   python3 .claude/skills/spec-sync/check_sync.py
   ```

2. **Валидация прототипа:**
   ```bash
   python3 scripts/validate_prototype.py prototypes/current.html
   ```

---

## Ключевые документы

### Спецификация (spec/)
- `domain_model.md` - Полная модель домена с бизнес-правилами
- `data_model.puml` - ER-диаграмма базы данных
- `state_machine.puml` - Диаграммы состояний всех сущностей
- `GUIDE.md` - Руководство для разработки

### Правила работы (для агентов/Claude Code)
- `CLAUDE.md` - соглашения по структуре, версионированию и git workflow

### Прототип (prototypes/)
- `current.html` - Интерактивный HTML прототип (React + Material-UI). Это часть MVP и основной артефакт для демо/передачи команде.

### Документация (docs/)
- `executive_summary.md` - Executive summary для руководства
- `glossary.md` - Глоссарий терминов
- `faq_stakeholders.md` - FAQ для стейкхолдеров
- `use_cases.md` - Сценарии использования

---

## Технологический стек

**Backend:**
- Django 4.2+ / Django REST Framework
- PostgreSQL 14+
- Celery + Redis

**Frontend:**
- React 18+ / TypeScript
- Material-UI v5
- React Router v6

**Инфраструктура:**
- Docker + Docker Compose
- Nginx
- Gunicorn

---

## Оценка разработки

**Длительность:** 12 недель (3 месяца)

**Фазы:**
1. Инфраструктура и базовые сущности (2 недели)
2. Скоркарты и связи (2 недели)
3. Пилоты и процесс согласования (3 недели)
4. Внедрения и пакеты (3 недели)
5. Визуализация и артефакты (1 неделя)
6. Уведомления и финализация (1 неделя)

---

## Skills и утилиты

### spec-sync
Автоматическая синхронизация изменений между документами спецификации.

```bash
# Проверка несоответствий
python3 .claude/skills/spec-sync/check_sync.py
```

### validate_prototype
Проверка HTML прототипов на корректность.

```bash
# Валидация прототипа
python3 scripts/validate_prototype.py prototypes/current.html
```

---

## Контакты

**Вопросы по спецификации:**
- Проверьте `spec/domain_model.md`
- Посмотрите PlantUML диаграммы
- Откройте `prototypes/current.html`

**Вопросы по разработке:**
- Изучите `spec/GUIDE.md`
- Проверьте `planning/mvp/current/`

---

**Версия документа:** 1.0  
**Дата обновления:** 2026-03-11
