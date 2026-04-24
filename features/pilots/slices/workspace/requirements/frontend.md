# Страница "Пилоты" (Frontend)

Статус: **для передачи команде**
Область: MVP
Дата обновления: 2026-03-18

## Оглавление
1. [Стора с фичей (ссылка на Jira)](#стора-с-фичей-ссылка-на-jira)
2. [Бизнес-требования](#бизнес-требования)
3. [Пользовательские требования к АС КОДА](#пользовательские-требования-к-ас-кода)
4. [Критерии приемки](#критерии-приемки)
5. [Функциональные требования](#функциональные-требования)
6. [Реализация для FRONTEND](#реализация-для-frontend)
7. [Интеграция с Backend API](#интеграция-с-backend-api)
8. [Обработка ошибок](#обработка-ошибок)
9. [Валидация](#валидация)
10. [BUGS](#bugs)
11. [Доп. пояснения](#доп-пояснения)

## Стора с фичей (ссылка на Jira)

- TBD

## Бизнес-требования

### Цель

Реализовать Frontend для страницы `Пилоты`, которая позволяет пользователям:
- просматривать список всех пилотов с фильтрацией и поиском;
- создавать новые пилоты с привязкой к инициативе и скоркартам;
- редактировать черновики пилотов;
- просматривать детальную информацию о пилоте;
- управлять жизненным циклом пилота (отправка на согласование, активация, завершение, корректировка);
- просматривать результаты и метрики активных пилотов;
- просматривать историю версий и изменений.

### Контекст

Страница `Пилоты` является инструментом для управления контролируемыми экспериментами с реальными клиентами. Пилот проходит через несколько этапов: черновик → согласование → утверждение → активация → завершение/корректировка.

## Пользовательские требования к АС КОДА

### ПТ-1. Список пилотов

**Описание:** Пользователь должен видеть список всех пилотов с возможностью фильтрации и поиска.

**Детали:**
- Табличное представление с ключевыми полями
- Фильтрация по статусу, продукту, критичности, инициативе
- Поиск по названию
- Сортировка по дате создания, статусу, критичности
- Пагинация для больших списков
- Цветовая индикация статусов и критичности
- Отображение активных пилотов с прогресс-баром

### ПТ-2. Создание пилота

**Описание:** Пользователь должен иметь возможность создать новый пилот.

**Детали:**
- Выбор инициативы (обязательно)
- Название и описание пилота
- Выбор скоркарт (минимум одна)
- Выбор подпродуктов (опционально, наследуется от скоркарт)
- Указание критичности (critical/high/medium/low)
- Указание параметров эксперимента (размер выборки, длительность)
- Указание целевых метрик
- Валидация всех полей перед сохранением

### ПТ-3. Редактирование пилота

**Описание:** Пользователь должен иметь возможность редактировать пилот в статусе draft или requires_correction.

**Детали:**
- Редактирование всех полей, кроме инициативы
- Изменение связанных скоркарт
- Изменение параметров эксперимента
- Сохранение изменений с валидацией
- Невозможность редактирования после отправки на согласование (кроме requires_correction)

### ПТ-4. Детальный просмотр

**Описание:** Пользователь должен видеть полную информацию о пилоте.

**Детали:**
- Модальное окно или отдельная страница с детальной информацией
- Вкладки: "Общая информация", "Скоркарты", "Результаты и метрики", "История версий", "Артефакты"
- Отображение текущего статуса и этапа процесса
- Для активных пилотов - отображение прогресса и текущих метрик
- Кнопки действий в зависимости от статуса и прав пользователя

### ПТ-5. Управление жизненным циклом

**Описание:** Пользователь должен иметь возможность управлять статусом пилота.

**Детали:**
- Отправка на согласование (draft → requires_activation)
- Активация пилота (ratified → active)
- Завершение пилота (active → completed)
- Отправка на корректировку (active → requires_correction)
- Повторная отправка после корректировки (requires_correction → requires_activation)
- Подтверждение перед критичными действиями
- Отображение текущего этапа процесса согласования

### ПТ-6. Просмотр результатов и метрик

**Описание:** Пользователь должен видеть результаты активного или завершенного пилота.

**Детали:**
- Отображение целевых метрик и их текущих значений
- Сравнение с плановыми показателями
- Визуализация динамики метрик (графики)
- Финансовые эффекты (плановые и фактические)
- Статистика по выборке (размер, охват)

## Критерии приемки

### КП-1. Отображение списка

- [ ] Список показывает все пилоты с корректными данными
- [ ] Фильтры работают корректно и применяются мгновенно
- [ ] Поиск работает по названию пилота
- [ ] Сортировка работает по всем доступным полям
- [ ] Пагинация работает корректно
- [ ] Цветовая индикация статусов и критичности соответствует спецификации
- [ ] Активные пилоты отображаются с прогресс-баром

### КП-2. Создание пилота

- [ ] Форма создания открывается корректно
- [ ] Все обязательные поля валидируются
- [ ] Нельзя создать пилот без инициативы
- [ ] Нельзя создать пилот без скоркарт
- [ ] После создания пилот появляется в списке
- [ ] Пилот создается в статусе draft

### КП-3. Редактирование пилота

- [ ] Форма редактирования открывается для draft и requires_correction
- [ ] Все поля, кроме инициативы, можно редактировать
- [ ] Изменения сохраняются корректно
- [ ] Валидация работает при редактировании
- [ ] После отправки на согласование редактирование недоступно (кроме requires_correction)

### КП-4. Детальный просмотр

- [ ] Модальное окно открывается при клике на пилот
- [ ] Все вкладки отображают корректные данные
- [ ] История версий показывает все изменения
- [ ] Связанные скоркарты отображаются с корректными данными
- [ ] Результаты и метрики отображаются для active и completed пилотов
- [ ] Артефакты отображаются и доступны для скачивания

### КП-5. Управление жизненным циклом

- [ ] Кнопка "Отправить на согласование" доступна только для draft
- [ ] Кнопка "Активировать" доступна только для ratified
- [ ] Кнопка "Завершить" доступна только для active
- [ ] Кнопка "Требует корректировки" доступна только для active
- [ ] Подтверждение запрашивается перед критичными действиями
- [ ] Статус обновляется после выполнения действия

### КП-6. Просмотр результатов

- [ ] Метрики отображаются для active и completed пилотов
- [ ] Графики динамики метрик работают корректно
- [ ] Сравнение с плановыми показателями отображается
- [ ] Финансовые эффекты рассчитываются корректно

### КП-7. Обработка ошибок

- [ ] Ошибки API отображаются пользователю в понятном виде
- [ ] При ошибке сети показывается соответствующее сообщение
- [ ] Ошибки валидации отображаются рядом с полями
- [ ] Критические ошибки не ломают интерфейс

## Функциональные требования

### ФТ-1. Архитектура компонентов

**Описание:** Страница должна быть построена на основе React компонентов с использованием Material-UI.

**Компоненты:**

#### PilotsPage (корневой компонент)
- Управляет состоянием страницы
- Координирует загрузку данных
- Обрабатывает глобальные ошибки

#### PilotsList (список пилотов)
- Отображает таблицу с пилотами
- Управляет фильтрами и поиском
- Обрабатывает пагинацию
- Открывает детальное окно при клике

#### PilotFilters (панель фильтров)
- Отображает все доступные фильтры
- Управляет состоянием фильтров
- Передает изменения родительскому компоненту

#### CreatePilotDialog (диалог создания)
- Форма создания нового пилота
- Валидация полей
- Выбор инициативы, скоркарт, подпродуктов
- Указание параметров эксперимента
- Отправка данных на сервер

#### EditPilotDialog (диалог редактирования)
- Форма редактирования пилота
- Аналогична CreatePilotDialog, но с предзаполненными данными
- Доступна для draft и requires_correction

#### PilotDetailDialog (детальное окно)
- Отображает детальную информацию о пилоте
- Содержит вкладки с разными аспектами
- Предоставляет кнопки для управления жизненным циклом

#### PilotMetricsView (просмотр метрик)
- Отображает целевые метрики и их значения
- Графики динамики метрик
- Сравнение с плановыми показателями
- Финансовые эффекты

#### PilotActionsMenu (меню действий)
- Контекстное меню с доступными действиями
- Действия зависят от статуса и прав пользователя
- Подтверждение перед критичными действиями

### ФТ-2. Управление состоянием

**Описание:** Состояние приложения должно управляться через React hooks.

**Состояния:**

#### Глобальное состояние (PilotsPage)
```typescript
interface PilotsPageState {
  user: User;
  loading: boolean;
  error: string | null;
}
```

#### Состояние списка (PilotsList)
```typescript
interface PilotsListState {
  pilots: Pilot[];
  filters: PilotFilters;
  sortBy: 'createdAt' | 'status' | 'priority';
  sortOrder: 'asc' | 'desc';
  page: number;
  pageSize: number;
  totalCount: number;
  loading: boolean;
  error: string | null;
  detailDialogOpen: boolean;
  detailDialogPilotId: string | null;
  createDialogOpen: boolean;
  editDialogOpen: boolean;
  editDialogPilotId: string | null;
}
```

### ФТ-3. Типы данных

**Описание:** Все данные должны быть типизированы с использованием TypeScript.

**Основные типы:**

```typescript
// Пилот в списке
interface Pilot {
  id: string;
  name: string;
  description: string;
  initiativeId: string;
  initiativeName: string;
  productName: string;
  currentVersion: PilotVersion;
  createdAt: string;
  createdBy: string;
}

// Версия пилота
interface PilotVersion {
  id: string;
  version: number;
  status: PilotStatus;
  priority: 'critical' | 'high' | 'medium' | 'low';
  experimentParams: ExperimentParams;
  targetMetrics: TargetMetric[];
  scorecards: ScorecardRef[];
  subproducts: SubproductRef[];
  createdAt: string;
  createdBy: string;
}

// Статусы пилота
type PilotStatus =
  | 'draft'
  | 'requires_activation'
  | 'in_approval'
  | 'approved'
  | 'in_ratification'
  | 'ratified'
  | 'active'
  | 'requires_correction'
  | 'completed';

// Параметры эксперимента
interface ExperimentParams {
  sampleSize: number;
  duration: number; // в днях
  startDate: string | null;
  endDate: string | null;
}

// Целевая метрика
interface TargetMetric {
  name: string;
  targetValue: number;
  currentValue: number | null;
  unit: string;
}

// Ссылка на скоркарту
interface ScorecardRef {
  id: string;
  name: string;
  version: number;
}

// Ссылка на подпродукт
interface SubproductRef {
  id: string;
  name: string;
}

// Детальная информация о пилоте
interface PilotDetail {
  id: string;
  name: string;
  description: string;
  initiative: InitiativeRef;
  versions: PilotVersion[];
  currentVersion: PilotVersion;
  metrics: PilotMetrics | null;
  artifacts: Artifact[];
  createdAt: string;
  createdBy: string;
  updatedAt: string;
  updatedBy: string;
}

// Метрики пилота
interface PilotMetrics {
  targetMetrics: TargetMetric[];
  financialEffects: FinancialEffects;
  sampleStatistics: SampleStatistics;
  timeline: MetricTimeline[];
}

// Финансовые эффекты
interface FinancialEffects {
  npv: number;
  irr: number;
  paybackPeriod: number;
  expectedEffectByYear: { year: number; effect: number }[];
  actualEffectByYear: { year: number; effect: number }[];
}

// Статистика выборки
interface SampleStatistics {
  totalSize: number;
  currentSize: number;
  coverage: number; // процент
}

// Временная шкала метрик
interface MetricTimeline {
  date: string;
  metrics: { name: string; value: number }[];
}

// Фильтры
interface PilotFilters {
  search: string;
  status: PilotStatus | 'all';
  productId: string | null;
  priority: 'all' | 'critical' | 'high' | 'medium' | 'low';
  initiativeId: string | null;
}

// Данные для создания пилота
interface CreatePilotData {
  name: string;
  description: string;
  initiativeId: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  experimentParams: ExperimentParams;
  targetMetrics: TargetMetric[];
  scorecardIds: string[];
  subproductIds: string[];
}
```

### ФТ-4. UI компоненты и их спецификация

**Описание:** Детальная спецификация UI компонентов с использованием Material-UI.

#### Таблица пилотов (PilotsList)

**Колонки:**
- Название пилота (кликабельная ссылка)
- Инициатива
- Продукт
- Статус (цветной бадж)
- Критичность (цветной бадж)
- Прогресс (для active - прогресс-бар)
- Версия
- Дата создания
- Действия (меню с иконкой)

**Поведение:**
- Сортировка по умолчанию: по дате создания (новые сверху)
- Клик по строке открывает детальное окно
- Hover эффект на строках
- Пагинация: 20 элементов на страницу
- Контекстное меню с действиями
- Для активных пилотов - прогресс-бар показывает процент выполнения

#### Панель фильтров (PilotFilters)

**Элементы:**
- Поле поиска (TextField с иконкой поиска)
- Выпадающий список "Статус" (All/Draft/Active/Completed/etc.)
- Выпадающий список "Продукт" (загружается с сервера)
- Выпадающий список "Критичность" (All/Critical/High/Medium/Low)
- Выпадающий список "Инициатива" (загружается с сервера)
- Кнопка "Очистить фильтры"

**Поведение:**
- Фильтры применяются с debounce 300ms для поиска
- Выпадающие списки применяются немедленно
- Кнопка "Очистить" сбрасывает все фильтры

#### Диалог создания/редактирования (CreatePilotDialog / EditPilotDialog)

**Структура:**
- Заголовок: "Создать пилот" / "Редактировать пилот"
- Форма с полями:
  - Инициатива (Autocomplete, обязательное, только для создания)
  - Название (TextField, обязательное)
  - Описание (TextField multiline, обязательное)
  - Критичность (Select, обязательное)
  - Скоркарты (Autocomplete multiple, обязательное, минимум 1)
  - Подпродукты (Autocomplete multiple, опциональное)
  - Параметры эксперимента:
    - Размер выборки (TextField number)
    - Длительность (TextField number, в днях)
    - Дата начала (DatePicker, опциональное)
    - Дата окончания (DatePicker, опциональное)
  - Целевые метрики (динамический список):
    - Название метрики
    - Целевое значение
    - Единица измерения
- Кнопки:
  - "Создать" / "Сохранить" (primary)
  - "Отмена"

**Валидация:**
- Название: 3-200 символов
- Описание: 10-1000 символов
- Минимум одна скоркарта
- Размер выборки: > 0
- Длительность: > 0
- Минимум одна целевая метрика

#### Детальное окно (PilotDetailDialog)

**Структура:**
- Заголовок: название пилота + статус
- Кнопка закрытия (X)
- Вкладки:
  - "Общая информация"
  - "Скоркарты"
  - "Результаты и метрики" (только для active и completed)
  - "История версий"
  - "Артефакты"
- Футер с кнопками действий

**Вкладка "Общая информация":**
- Название
- Описание
- Инициатива (ссылка)
- Продукт
- Подпродукты (список)
- Критичность (цветной бадж)
- Параметры эксперимента:
  - Размер выборки
  - Длительность
  - Дата начала
  - Дата окончания
- Текущая версия
- Статус (с визуализацией этапа процесса)
- Дата создания
- Создатель
- Дата последнего изменения
- Последний редактор

**Вкладка "Скоркарты":**
- Таблица со скоркартами:
  - Название
  - Версия
  - Статус
  - Ссылка на детали

**Вкладка "Результаты и метрики":**
- Целевые метрики:
  - Название
  - Целевое значение
  - Текущее значение
  - Прогресс (прогресс-бар)
- Графики динамики метрик (линейные графики)
- Финансовые эффекты:
  - NPV (плановый и фактический)
  - IRR (плановый и фактический)
  - Payback Period
  - График эффектов по годам
- Статистика выборки:
  - Общий размер
  - Текущий размер
  - Охват (процент)

**Вкладка "История версий":**
- Timeline с версиями
- Для каждой версии:
  - Номер версии
  - Статус
  - Дата создания
  - Создатель
  - Изменения (diff)

**Вкладка "Артефакты":**
- Список артефактов:
  - Название
  - Тип
  - Дата загрузки
  - Загрузивший
  - Кнопка скачивания

**Футер:**
- Кнопка "Редактировать" (только для draft и requires_correction)
- Кнопка "Отправить на согласование" (только для draft)
- Кнопка "Активировать" (только для ratified)
- Кнопка "Завершить" (только для active)
- Кнопка "Требует корректировки" (только для active)
- Кнопка "Закрыть"

#### Меню действий (PilotActionsMenu)

**Действия в зависимости от статуса:**

**Draft:**
- Редактировать
- Отправить на согласование
- Удалить

**Requires_activation / In Approval / In Ratification:**
- Просмотреть процесс согласования
- Отозвать (только для создателя)

**Ratified:**
- Активировать

**Active:**
- Завершить
- Требует корректировки
- Просмотреть метрики

**Requires_correction:**
- Редактировать
- Отправить на согласование

**Completed:**
- Просмотреть результаты
- Просмотреть историю

### ФТ-5. Цветовая схема и иконки

**Статусы:**
- `draft`: серый (#9e9e9e), иконка: draft
- `requires_activation`: оранжевый (#ff9800), иконка: send
- `in_approval`: синий (#2196f3), иконка: pending
- `approved`: зеленый (#4caf50), иконка: check_circle
- `in_ratification`: фиолетовый (#9c27b0), иконка: gavel
- `ratified`: темно-зеленый (#2e7d32), иконка: verified
- `active`: зеленый (#1b5e20), иконка: play_circle
- `requires_correction`: оранжевый (#f57c00), иконка: edit
- `completed`: синий (#1565c0), иконка: check_circle_outline

**Критичность:**
- `critical`: красный (#d32f2f), иконка: error
- `high`: оранжевый (#f57c00), иконка: warning
- `medium`: синий (#1976d2), иконка: info
- `low`: серый (#757575), иконка: low_priority

**Действия:**
- Создать: зеленый (#4caf50), иконка: add
- Редактировать: серый (#757575), иконка: edit
- Отправить на согласование: синий (#2196f3), иконка: send
- Активировать: зеленый (#2e7d32), иконка: play_circle
- Завершить: синий (#1565c0), иконка: check_circle
- Требует корректировки: оранжевый (#f57c00), иконка: edit
- Удалить: красный (#f44336), иконка: delete

### ФТ-6. Визуализация процесса согласования

**Описание:** Отображение текущего этапа процесса согласования в детальном окне.

**Компонент:** Stepper (Material-UI)

**Этапы:**
1. Черновик (draft)
2. Согласование (in_approval)
3. Утверждение (in_ratification)
4. Активация (active)
5. Завершение (completed)

**Визуализация:**
- Активный этап подсвечивается
- Пройденные этапы отмечены галочкой
- Будущие этапы серые
- При наведении на этап показывается tooltip с деталями
- Для requires_correction - отображается ветка корректировки

### ФТ-7. Визуализация метрик

**Описание:** Графическое отображение метрик активного или завершенного пилота.

**Компоненты:**

#### График динамики метрик
- Линейный график (recharts или chart.js)
- Ось X: время (даты)
- Ось Y: значение метрики
- Несколько линий для разных метрик
- Легенда с названиями метрик
- Tooltip при наведении

#### Прогресс-бары для целевых метрик
- Для каждой метрики - прогресс-бар
- Цвет зависит от достижения цели:
  - Зеленый: >= 100%
  - Желтый: 80-99%
  - Красный: < 80%
- Отображение текущего и целевого значения

#### График финансовых эффектов
- Столбчатая диаграмма
- Сравнение плановых и фактических эффектов по годам
- Две серии: план и факт
- Легенда и tooltip

### ФТ-8. Адаптивность

**Описание:** Интерфейс должен корректно отображаться на разных размерах экрана.

**Breakpoints:**
- Desktop: >= 1200px (полная функциональность)
- Tablet: 768px - 1199px (адаптированная таблица)
- Mobile: < 768px (карточный вид вместо таблицы)

**Адаптации:**
- На мобильных устройствах таблица заменяется на карточки
- Фильтры сворачиваются в выдвижную панель
- Детальное окно занимает весь экран на мобильных устройствах
- Графики адаптируются под ширину экрана
- Меню действий адаптируется под ширину экрана

## Реализация для FRONTEND

### Технологический стек

**Обязательные технологии:**
- React 18+
- TypeScript 4.9+
- Material-UI (MUI) 5+
- React Router 6+ (для навигации)
- Axios (для HTTP запросов)
- React Query или SWR (для кеширования и управления серверным состоянием)
- Recharts или Chart.js (для графиков)

**Рекомендуемые библиотеки:**
- date-fns (для работы с датами)
- lodash (для утилит, особенно debounce)
- react-hook-form (для форм с валидацией)
- recharts (для визуализации метрик)

### Структура файлов

```
src/
  pages/
    PilotsPage/
      index.tsx                      # Корневой компонент
      PilotsList.tsx                 # Список пилотов
      components/
        PilotFilters.tsx             # Панель фильтров
        PilotRow.tsx                 # Строка таблицы
        PilotActionsMenu.tsx         # Меню действий
        CreatePilotDialog.tsx        # Диалог создания
        EditPilotDialog.tsx          # Диалог редактирования
        PilotDetailDialog.tsx        # Детальное окно
        PilotMetricsView.tsx         # Просмотр метрик
        PilotStepper.tsx             # Визуализация процесса
        MetricsChart.tsx             # График метрик
        FinancialEffectsChart.tsx    # График финансовых эффектов
      hooks/
        usePilots.ts                 # Hook для работы с пилотами
        usePilotActions.ts           # Hook для действий
        usePilotMetrics.ts           # Hook для метрик
      types/
        index.ts                     # TypeScript типы
      utils/
        filters.ts                   # Утилиты фильтрации
        formatters.ts                # Форматирование данных
        statusHelpers.ts             # Хелперы для статусов
        metricsCalculations.ts       # Расчеты метрик
      api/
        pilots.ts                    # API методы
```

### Пример реализации корневого компонента

```typescript
// src/pages/PilotsPage/index.tsx
import React, { useState } from 'react';
import { Box, Button, Paper, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import PilotsList from './PilotsList';
import CreatePilotDialog from './components/CreatePilotDialog';

export default function PilotsPage() {
  const [createDialogOpen, setCreateDialogOpen] = useState(false);

  return (
    <Box sx={{ width: '100%', p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Пилоты</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setCreateDialogOpen(true)}
        >
          Создать пилот
        </Button>
      </Box>

      <Paper sx={{ width: '100%' }}>
        <PilotsList />
      </Paper>

      <CreatePilotDialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
      />
    </Box>
  );
}
```

### Пример реализации custom hook для метрик

```typescript
// src/pages/PilotsPage/hooks/usePilotMetrics.ts
import { useQuery } from '@tanstack/react-query';
import { getPilotMetrics } from '../api/pilots';
import type { PilotMetrics } from '../types';

export function usePilotMetrics(pilotId: string, enabled: boolean = true) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['pilot-metrics', pilotId],
    queryFn: () => getPilotMetrics(pilotId),
    enabled: enabled,
    staleTime: 60000, // 1 minute
    refetchInterval: 300000, // 5 minutes for active pilots
  });

  return {
    metrics: data || null,
    isLoading,
    error,
    refetch,
  };
}
```

### Пример компонента графика метрик

```typescript
// src/pages/PilotsPage/components/MetricsChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Box, Typography } from '@mui/material';
import type { MetricTimeline } from '../types';

interface MetricsChartProps {
  data: MetricTimeline[];
  metricNames: string[];
}

const COLORS = ['#2196f3', '#4caf50', '#ff9800', '#f44336', '#9c27b0'];

export default function MetricsChart({ data, metricNames }: MetricsChartProps) {
  // Transform data for recharts
  const chartData = data.map(item => {
    const point: any = { date: new Date(item.date).toLocaleDateString() };
    item.metrics.forEach(metric => {
      point[metric.name] = metric.value;
    });
    return point;
  });

  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <Typography variant="h6" gutterBottom>
        Динамика метрик
      </Typography>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          {metricNames.map((name, index) => (
            <Line
              key={name}
              type="monotone"
              dataKey={name}
              stroke={COLORS[index % COLORS.length]}
              strokeWidth={2}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
}
```

## Интеграция с Backend API

### API-1. Получение списка пилотов

**Endpoint:** `GET /api/v1/pilots`

**Query параметры:**
- `status` (optional): фильтр по статусу
- `product_id` (optional): UUID продукта
- `priority` (optional): `critical` | `high` | `medium` | `low`
- `initiative_id` (optional): UUID инициативы
- `search` (optional): поиск по названию
- `sort_by` (optional): `createdAt` | `status` | `priority`
- `sort_order` (optional): `asc` | `desc`
- `page` (optional): номер страницы (default: 1)
- `page_size` (optional): размер страницы (default: 20)

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Pilot Name",
      "description": "Description",
      "initiative_id": "uuid",
      "initiative_name": "Initiative Name",
      "product_name": "Product Name",
      "current_version": {
        "id": "uuid",
        "version": 1,
        "status": "active",
        "priority": "high",
        "experiment_params": {
          "sample_size": 1000,
          "duration": 90,
          "start_date": "2026-03-01",
          "end_date": "2026-05-30"
        },
        "target_metrics": [
          {
            "name": "Approval Rate",
            "target_value": 75,
            "current_value": 72,
            "unit": "%"
          }
        ],
        "scorecards": [...],
        "subproducts": [...],
        "created_at": "2026-03-15T10:00:00Z",
        "created_by": "user@example.com"
      },
      "created_at": "2026-03-15T10:00:00Z",
      "created_by": "user@example.com"
    }
  ],
  "total_count": 42,
  "page": 1,
  "page_size": 20
}
```

### API-2. Получение детальной информации о пилоте

**Endpoint:** `GET /api/v1/pilots/{pilot_id}`

**Response:**
```json
{
  "id": "uuid",
  "name": "Pilot Name",
  "description": "Description",
  "initiative": {
    "id": "uuid",
    "name": "Initiative Name",
    "product_id": "uuid",
    "product_name": "Product Name"
  },
  "versions": [...],
  "current_version": {...},
  "metrics": {
    "target_metrics": [...],
    "financial_effects": {
      "npv": 1500000,
      "irr": 0.25,
      "payback_period": 18,
      "expected_effect_by_year": [...],
      "actual_effect_by_year": [...]
    },
    "sample_statistics": {
      "total_size": 1000,
      "current_size": 850,
      "coverage": 85
    },
    "timeline": [...]
  },
  "artifacts": [...],
  "created_at": "2026-03-15T10:00:00Z",
  "created_by": "user@example.com",
  "updated_at": "2026-03-16T14:00:00Z",
  "updated_by": "user@example.com"
}
```

### API-3. Создание пилота

**Endpoint:** `POST /api/v1/pilots`

**Request body:**
```json
{
  "name": "Pilot Name",
  "description": "Description",
  "initiative_id": "uuid",
  "priority": "high",
  "experiment_params": {
    "sample_size": 1000,
    "duration": 90,
    "start_date": "2026-03-01",
    "end_date": "2026-05-30"
  },
  "target_metrics": [
    {
      "name": "Approval Rate",
      "target_value": 75,
      "unit": "%"
    }
  ],
  "scorecard_ids": ["uuid1", "uuid2"],
  "subproduct_ids": ["uuid1", "uuid2"]
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Pilot Name",
  "current_version": {
    "id": "uuid",
    "version": 1,
    "status": "draft",
    ...
  },
  "created_at": "2026-03-15T10:00:00Z"
}
```

### API-4. Обновление пилота

**Endpoint:** `PATCH /api/v1/pilots/{pilot_id}`

**Request body:**
```json
{
  "name": "New Name",
  "description": "New description",
  "priority": "critical",
  "experiment_params": {
    "sample_size": 1500,
    "duration": 120
  },
  "target_metrics": [...],
  "scorecard_ids": ["uuid1", "uuid2", "uuid3"],
  "subproduct_ids": ["uuid1"]
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "New Name",
  "current_version": {...},
  "updated_at": "2026-03-16T14:00:00Z"
}
```

### API-5. Удаление пилота

**Endpoint:** `DELETE /api/v1/pilots/{pilot_id}`

**Response:**
```json
{
  "success": true
}
```

### API-6. Отправка на согласование

**Endpoint:** `POST /api/v1/pilots/{pilot_id}/send-to-approval`

**Request body:**
```json
{
  "stages": [
    {
      "name": "Risk Review",
      "assignee_ids": ["uuid1", "uuid2"]
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "pilot_id": "uuid",
  "new_status": "in_approval",
  "approval_instance_id": "uuid"
}
```

### API-7. Активация пилота

**Endpoint:** `POST /api/v1/pilots/{pilot_id}/activate`

**Response:**
```json
{
  "success": true,
  "pilot_id": "uuid",
  "new_status": "active",
  "activated_at": "2026-03-18T10:00:00Z"
}
```

### API-8. Завершение пилота

**Endpoint:** `POST /api/v1/pilots/{pilot_id}/complete`

**Response:**
```json
{
  "success": true,
  "pilot_id": "uuid",
  "new_status": "completed",
  "completed_at": "2026-05-30T18:00:00Z"
}
```

### API-9. Отправка на корректировку

**Endpoint:** `POST /api/v1/pilots/{pilot_id}/require-correction`

**Request body:**
```json
{
  "reason": "Metrics not meeting targets"
}
```

**Response:**
```json
{
  "success": true,
  "pilot_id": "uuid",
  "new_status": "requires_correction"
}
```

### API-10. Получение метрик пилота

**Endpoint:** `GET /api/v1/pilots/{pilot_id}/metrics`

**Response:**
```json
{
  "target_metrics": [
    {
      "name": "Approval Rate",
      "target_value": 75,
      "current_value": 72,
      "unit": "%"
    }
  ],
  "financial_effects": {
    "npv": 1500000,
    "irr": 0.25,
    "payback_period": 18,
    "expected_effect_by_year": [
      { "year": 2026, "effect": 500000 },
      { "year": 2027, "effect": 1000000 }
    ],
    "actual_effect_by_year": [
      { "year": 2026, "effect": 450000 }
    ]
  },
  "sample_statistics": {
    "total_size": 1000,
    "current_size": 850,
    "coverage": 85
  },
  "timeline": [
    {
      "date": "2026-03-01",
      "metrics": [
        { "name": "Approval Rate", "value": 70 }
      ]
    },
    {
      "date": "2026-03-15",
      "metrics": [
        { "name": "Approval Rate", "value": 72 }
      ]
    }
  ]
}
```

## Обработка ошибок

### ОШ-1. Типы ошибок

**Описание:** Система должна обрабатывать различные типы ошибок.

**Типы:**

#### Ошибки валидации (400)
- Отображаются рядом с соответствующими полями
- Не блокируют работу остального интерфейса
- Пример: "Размер выборки должен быть больше 0"

#### Ошибки прав доступа (403)
- Отображаются как toast-уведомление
- Действия, к которым нет доступа, скрываются или делаются неактивными
- Пример: "У вас нет прав для создания пилотов в этом продукте"

#### Ошибки состояния (409)
- Отображаются как модальное окно с объяснением
- Предлагают обновить данные
- Пример: "Пилот уже активирован"

#### Ошибки сервера (500)
- Отображаются как toast-уведомление
- Предлагают повторить попытку
- Логируются для отладки
- Пример: "Ошибка сервера. Попробуйте позже"

#### Ошибки сети
- Отображаются как banner в верхней части страницы
- Автоматически исчезают при восстановлении соединения
- Пример: "Нет подключения к серверу"

### ОШ-2. Обработка ошибок жизненного цикла

**Описание:** Специальная обработка ошибок при управлении жизненным циклом пилота.

**Сценарии:**

#### Отправка на согласование
- Проверка, что пилот в статусе draft или requires_correction
- Проверка, что все обязательные поля заполнены
- Проверка, что выбраны согласующие для всех этапов

#### Активация пилота
- Проверка, что пилот в статусе ratified
- Проверка, что параметры эксперимента корректны
- Подтверждение критичного действия

#### Завершение пилота
- Проверка, что пилот в статусе active
- Проверка, что собраны все необходимые метрики
- Подтверждение действия

#### Отправка на корректировку
- Проверка, что пилот в статусе active
- Обязательное указание причины корректировки
- Подтверждение действия

### ОШ-3. Graceful degradation

**Описание:** При ошибках загрузки некритичных данных интерфейс должен продолжать работать.

**Примеры:**
- Если не загрузились метрики - показываем остальные вкладки детального окна
- Если не загрузились графики - показываем табличное представление метрик
- Если не загрузились фильтры продуктов - показываем список без фильтра по продукту

## Валидация

### ВАЛ-1. Валидация на стороне клиента

**Описание:** Все пользовательские вводы должны валидироваться до отправки на сервер.

**Правила валидации:**

#### Название пилота
- Обязательное поле
- Минимум 3 символа
- Максимум 200 символов
- Сообщение: "Название должно содержать от 3 до 200 символов"

#### Описание пилота
- Обязательное поле
- Минимум 10 символов
- Максимум 1000 символов
- Сообщение: "Описание должно содержать от 10 до 1000 символов"

#### Выбор инициативы
- Обязательное поле
- Должна принадлежать продукту пользователя (для ПРМ/методолога)
- Сообщение: "Выберите инициативу"

#### Выбор скоркарт
- Обязательное поле
- Минимум одна скоркарта
- Сообщение: "Выберите хотя бы одну скоркарту"

#### Критичность
- Обязательное поле
- Одно из значений: critical/high/medium/low
- Сообщение: "Выберите критичность"

#### Размер выборки
- Обязательное поле
- Целое число > 0
- Сообщение: "Размер выборки должен быть больше 0"

#### Длительность эксперимента
- Обязательное поле
- Целое число > 0
- Сообщение: "Длительность должна быть больше 0 дней"

#### Целевые метрики
- Минимум одна метрика
- Для каждой метрики:
  - Название: обязательное, 2-100 символов
  - Целевое значение: обязательное, число
  - Единица измерения: обязательное, 1-20 символов
- Сообщение: "Добавьте хотя бы одну целевую метрику"

#### Даты эксперимента
- Дата начала должна быть раньше даты окончания
- Даты не могут быть в прошлом (для новых пилотов)
- Сообщение: "Дата начала должна быть раньше даты окончания"

### ВАЛ-2. Валидация перед действиями жизненного цикла

**Описание:** Перед выполнением действий должна проверяться возможность их выполнения.

**Проверки:**

#### Перед отправкой на согласование
- Пилот в статусе draft или requires_correction
- Все обязательные поля заполнены
- Выбраны согласующие для всех этапов
- Минимум одна целевая метрика
- Сообщение: "Заполните все обязательные поля и выберите согласующих"

#### Перед активацией
- Пилот в статусе ratified
- Параметры эксперимента корректны
- Сообщение: "Пилот готов к активации"

#### Перед завершением
- Пилот в статусе active
- Собраны метрики
- Сообщение: "Пилот готов к завершению"

#### Перед отправкой на корректировку
- Пилот в статусе active
- Указана причина корректировки
- Сообщение: "Укажите причину корректировки"

### ВАЛ-3. Реализация валидации

**Пример с react-hook-form:**
```typescript
import { useForm, useFieldArray, Controller } from 'react-hook-form';

interface CreatePilotFormData {
  name: string;
  description: string;
  initiativeId: string;
  priority: 'critical' | 'high' | 'medium' | 'low';
  experimentParams: {
    sampleSize: number;
    duration: number;
    startDate: string | null;
    endDate: string | null;
  };
  targetMetrics: Array<{
    name: string;
    targetValue: number;
    unit: string;
  }>;
  scorecardIds: string[];
  subproductIds: string[];
}

function CreatePilotDialog({ onClose, onCreate }: Props) {
  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors }
  } = useForm<CreatePilotFormData>({
    defaultValues: {
      targetMetrics: [{ name: '', targetValue: 0, unit: '' }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'targetMetrics'
  });

  const startDate = watch('experimentParams.startDate');
  const endDate = watch('experimentParams.endDate');

  const onSubmit = (data: CreatePilotFormData) => {
    onCreate(data);
    onClose();
  };

  return (
    <Dialog open onClose={onClose} maxWidth="md" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Создать пилот</DialogTitle>
        <DialogContent>
          <TextField
            {...register('name', {
              required: 'Название обязательно',
              minLength: { value: 3, message: 'Минимум 3 символа' },
              maxLength: { value: 200, message: 'Максимум 200 символов' }
            })}
            label="Название"
            fullWidth
            error={!!errors.name}
            helperText={errors.name?.message}
          />

          <TextField
            {...register('experimentParams.sampleSize', {
              required: 'Размер выборки обязателен',
              min: { value: 1, message: 'Размер выборки должен быть больше 0' }
            })}
            label="Размер выборки"
            type="number"
            fullWidth
            error={!!errors.experimentParams?.sampleSize}
            helperText={errors.experimentParams?.sampleSize?.message}
          />

          <TextField
            {...register('experimentParams.duration', {
              required: 'Длительность обязательна',
              min: { value: 1, message: 'Длительность должна быть больше 0' }
            })}
            label="Длительность (дней)"
            type="number"
            fullWidth
            error={!!errors.experimentParams?.duration}
            helperText={errors.experimentParams?.duration?.message}
          />

          <Typography variant="h6" sx={{ mt: 2, mb: 1 }}>
            Целевые метрики
          </Typography>
          {fields.map((field, index) => (
            <Box key={field.id} sx={{ display: 'flex', gap: 1, mb: 1 }}>
              <TextField
                {...register(`targetMetrics.${index}.name`, {
                  required: 'Название метрики обязательно',
                  minLength: { value: 2, message: 'Минимум 2 символа' }
                })}
                label="Название метрики"
                error={!!errors.targetMetrics?.[index]?.name}
                helperText={errors.targetMetrics?.[index]?.name?.message}
              />
              <TextField
                {...register(`targetMetrics.${index}.targetValue`, {
                  required: 'Целевое значение обязательно',
                  valueAsNumber: true
                })}
                label="Целевое значение"
                type="number"
                error={!!errors.targetMetrics?.[index]?.targetValue}
                helperText={errors.targetMetrics?.[index]?.targetValue?.message}
              />
              <TextField
                {...register(`targetMetrics.${index}.unit`, {
                  required: 'Единица измерения обязательна'
                })}
                label="Единица"
                error={!!errors.targetMetrics?.[index]?.unit}
                helperText={errors.targetMetrics?.[index]?.unit?.message}
              />
              <IconButton onClick={() => remove(index)} disabled={fields.length === 1}>
                <DeleteIcon />
              </IconButton>
            </Box>
          ))}
          <Button
            startIcon={<AddIcon />}
            onClick={() => append({ name: '', targetValue: 0, unit: '' })}
          >
            Добавить метрику
          </Button>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Отмена</Button>
          <Button type="submit" variant="contained">Создать</Button>
        </DialogActions>
      </form>
    </Dialog>
  );
}
```

### ВАЛ-4. Визуальная индикация валидации

**Описание:** Пользователь должен видеть результаты валидации в реальном времени.

**Индикаторы:**
- Красная обводка поля при ошибке
- Текст ошибки под полем
- Иконка ошибки справа от поля
- Disabled состояние кнопки при невалидной форме
- Tooltip с объяснением, почему кнопка disabled

**Пример:**
```typescript
<Tooltip
  title={
    pilot.status !== 'draft' && pilot.status !== 'requires_correction'
      ? 'Можно редактировать только черновики и пилоты, требующие корректировки'
      : !hasEditPermission
      ? 'У вас нет прав для редактирования'
      : ''
  }
>
  <span>
    <Button
      disabled={
        (pilot.status !== 'draft' && pilot.status !== 'requires_correction') ||
        !hasEditPermission
      }
      onClick={handleEdit}
    >
      Редактировать
    </Button>
  </span>
</Tooltip>
```

## BUGS

### Известные ограничения

1. **Одновременное редактирование**
   - Нет защиты от одновременного редактирования пилота несколькими пользователями
   - Последнее изменение перезаписывает предыдущие
   - Рекомендуется добавить optimistic locking в будущих версиях

2. **Обновление метрик**
   - Метрики активных пилотов обновляются с интервалом 5 минут
   - Нет real-time обновлений через WebSocket
   - Пользователь может видеть устаревшие данные между обновлениями

3. **Производительность графиков**
   - При большом количестве точек данных (>1000) графики могут тормозить
   - Рекомендуется агрегация данных на сервере для длительных пилотов

4. **Мобильная версия**
   - Графики на маленьких экранах сложно читать
   - Детальное окно с метриками занимает много места
   - Рекомендуется упрощенный вид для мобильных устройств

5. **Валидация дат**
   - Нет проверки пересечения дат с другими активными пилотами
   - Нет предупреждения о слишком коротких или длинных периодах эксперимента

6. **Экспорт данных**
   - Нет возможности экспортировать метрики в Excel/CSV
   - Нет возможности печати графиков

### Планируемые улучшения

1. **Real-time обновления метрик**
   - Внедрение WebSocket для получения обновлений метрик в реальном времени
   - Уведомления о достижении целевых значений

2. **Расширенная аналитика**
   - Сравнение результатов нескольких пилотов
   - Прогнозирование результатов на основе текущих данных
   - A/B тестирование на уровне отдельных клиентов

3. **Улучшенная визуализация**
   - Интерактивные графики с zoom и pan
   - Экспорт графиков в изображения
   - Дашборд с ключевыми метриками

4. **Автоматизация**
   - Автоматическое завершение пилота при достижении целей
   - Автоматические уведомления о критичных отклонениях
   - Интеграция с системами мониторинга

5. **Улучшенная история версий**
   - Визуальный diff между версиями
   - Возможность восстановления предыдущей версии
   - Комментарии к изменениям

## Доп. пояснения

### Архитектурные решения

#### Выбор React Query для управления серверным состоянием

**Обоснование:**
- Автоматическое кеширование запросов с настраиваемым временем жизни
- Встроенная поддержка retry и refetch
- Оптимистичные обновления для лучшего UX
- Автоматическая инвалидация кеша
- Отличная поддержка loading и error состояний
- Polling для обновления метрик активных пилотов

**Пример использования для метрик:**
```typescript
const { data: metrics } = useQuery({
  queryKey: ['pilot-metrics', pilotId],
  queryFn: () => getPilotMetrics(pilotId),
  enabled: pilot.status === 'active' || pilot.status === 'completed',
  staleTime: 60000, // 1 minute
  refetchInterval: pilot.status === 'active' ? 300000 : false, // 5 minutes for active
});
```

#### Выбор Recharts для визуализации

**Обоснование:**
- Декларативный API на основе React компонентов
- Хорошая производительность для средних объемов данных
- Встроенная поддержка responsive дизайна
- Легкая кастомизация стилей
- Хорошая документация

**Альтернативы:**
- Chart.js - более низкоуровневая, требует больше кода
- D3.js - очень мощная, но сложная для простых графиков
- Victory - похожа на Recharts, но менее популярна

#### Структура компонентов для метрик

**Принципы:**
- Разделение логики загрузки данных и визуализации
- Переиспользуемые компоненты графиков
- Lazy loading для тяжелых компонентов визуализации

**Пример архитектуры:**
```
PilotDetailDialog
├── PilotMetricsView (container)
│   ├── MetricsChart (presentational)
│   ├── FinancialEffectsChart (presentational)
│   ├── TargetMetricsProgress (presentational)
│   └── SampleStatistics (presentational)
```

### Производительность

#### Оптимизация рендеринга графиков

**Техники:**
- Мемоизация данных для графиков с useMemo
- Debounce для интерактивных элементов
- Lazy loading компонентов графиков
- Агрегация данных на сервере для длительных пилотов

**Пример оптимизации:**
```typescript
const MetricsChart = React.memo(({ data, metricNames }: Props) => {
  const chartData = useMemo(() => {
    return data.map(item => {
      const point: any = { date: new Date(item.date).toLocaleDateString() };
      item.metrics.forEach(metric => {
        point[metric.name] = metric.value;
      });
      return point;
    });
  }, [data]);

  return (
    <ResponsiveContainer>
      <LineChart data={chartData}>
        {/* ... */}
      </LineChart>
    </ResponsiveContainer>
  );
});
```

#### Оптимизация загрузки метрик

**Техники:**
- Polling только для активных пилотов
- Увеличенный staleTime для завершенных пилотов
- Prefetching метрик при hover на пилоте
- Кеширование графиков в памяти

**Пример:**
```typescript
export function usePilotMetrics(pilotId: string, status: PilotStatus) {
  const isActive = status === 'active';
  const isCompleted = status === 'completed';

  return useQuery({
    queryKey: ['pilot-metrics', pilotId],
    queryFn: () => getPilotMetrics(pilotId),
    enabled: isActive || isCompleted,
    staleTime: isCompleted ? 3600000 : 60000, // 1 hour for completed, 1 min for active
    refetchInterval: isActive ? 300000 : false, // 5 minutes for active only
  });
}
```

#### Оптимизация рендеринга списка

**Техники:**
- Виртуализация таблицы при большом количестве пилотов
- React.memo для строк таблицы
- useCallback для обработчиков событий

### Тестирование

#### Unit тесты

**Что тестировать:**
- Утилиты расчета метрик
- Форматирование данных для графиков
- Валидация форм
- Хелперы для статусов
- Расчет прогресса пилота

**Пример теста:**
```typescript
describe('calculateProgress', () => {
  it('calculates progress based on current and target metrics', () => {
    const metrics = [
      { name: 'Approval Rate', targetValue: 75, currentValue: 60 },
      { name: 'Default Rate', targetValue: 5, currentValue: 4 }
    ];

    const progress = calculateProgress(metrics);

    expect(progress).toBeCloseTo(82.5); // (60/75 + 4/5) / 2 * 100
  });

  it('returns 0 for pilot without metrics', () => {
    expect(calculateProgress([])).toBe(0);
  });
});
```

#### Integration тесты

**Что тестировать:**
- Создание пилота с метриками
- Редактирование параметров эксперимента
- Отправка на согласование
- Активация пилота
- Отображение метрик для активного пилота

**Пример теста:**
```typescript
describe('PilotMetricsView', () => {
  it('displays metrics for active pilot', async () => {
    const pilot = { id: '1', status: 'active' };
    const metrics = {
      targetMetrics: [
        { name: 'Approval Rate', targetValue: 75, currentValue: 72, unit: '%' }
      ]
    };

    server.use(
      rest.get('/api/v1/pilots/1/metrics', (req, res, ctx) => {
        return res(ctx.json(metrics));
      })
    );

    render(<PilotMetricsView pilotId="1" status="active" />);

    await waitFor(() => {
      expect(screen.getByText('Approval Rate')).toBeInTheDocument();
      expect(screen.getByText('72')).toBeInTheDocument();
      expect(screen.getByText('75')).toBeInTheDocument();
    });
  });
});
```

#### E2E тесты

**Критические сценарии:**
1. Создать пилот → Добавить метрики → Отправить на согласование → Активировать
2. Активный пилот → Просмотр метрик → Завершение
3. Активный пилот → Требует корректировки → Редактирование → Повторная отправка
4. Фильтрация пилотов по статусу
5. Просмотр графиков метрик

### Accessibility (A11y)

#### Требования

**WCAG 2.1 Level AA:**
- Все интерактивные элементы доступны с клавиатуры
- Правильные ARIA атрибуты для графиков
- Достаточный цветовой контраст
- Альтернативный текст для визуализаций
- Логичный порядок табуляции
- Доступность для screen readers

**Реализация для графиков:**
```typescript
<Box role="img" aria-label="График динамики метрик пилота">
  <ResponsiveContainer>
    <LineChart data={chartData} aria-hidden="true">
      {/* ... */}
    </LineChart>
  </ResponsiveContainer>

  {/* Табличное представление для screen readers */}
  <Table sx={{ display: 'none' }} aria-label="Данные метрик">
    <TableHead>
      <TableRow>
        <TableCell>Дата</TableCell>
        {metricNames.map(name => (
          <TableCell key={name}>{name}</TableCell>
        ))}
      </TableRow>
    </TableHead>
    <TableBody>
      {data.map(item => (
        <TableRow key={item.date}>
          <TableCell>{item.date}</TableCell>
          {item.metrics.map(metric => (
            <TableCell key={metric.name}>{metric.value}</TableCell>
          ))}
        </TableRow>
      ))}
    </TableBody>
  </Table>
</Box>
```

**Реализация для прогресс-баров:**
```typescript
<Box>
  <Typography id={`metric-${metric.name}`}>
    {metric.name}: {metric.currentValue} / {metric.targetValue} {metric.unit}
  </Typography>
  <LinearProgress
    variant="determinate"
    value={(metric.currentValue / metric.targetValue) * 100}
    aria-labelledby={`metric-${metric.name}`}
    aria-valuenow={metric.currentValue}
    aria-valuemin={0}
    aria-valuemax={metric.targetValue}
  />
</Box>
```

#### Keyboard navigation

**Горячие клавиши:**
- `Ctrl/Cmd + N` - создать новый пилот
- `Enter` - открыть детальное окно
- `Escape` - закрыть модальное окно
- `Tab` - навигация между элементами
- `Space` - активация кнопок
- `Arrow keys` - навигация по графикам (если поддерживается)

### Интернационализация (i18n)

**Подготовка:**
- Все тексты должны быть вынесены в отдельные файлы
- Использование библиотеки react-i18next
- Поддержка форматирования дат, чисел и валют по локали
- Форматирование метрик с учетом локали

**Пример структуры:**
```typescript
// locales/ru.json
{
  "pilots": {
    "title": "Пилоты",
    "create": "Создать пилот",
    "edit": "Редактировать пилот",
    "status": {
      "draft": "Черновик",
      "active": "Активен",
      "completed": "Завершен"
    },
    "actions": {
      "sendToApproval": "Отправить на согласование",
      "activate": "Активировать",
      "complete": "Завершить",
      "requireCorrection": "Требует корректировки"
    },
    "metrics": {
      "title": "Метрики",
      "targetValue": "Целевое значение",
      "currentValue": "Текущее значение",
      "progress": "Прогресс"
    }
  }
}
```

**Форматирование чисел:**
```typescript
import { useTranslation } from 'react-i18next';

function MetricValue({ value, unit }: Props) {
  const { i18n } = useTranslation();

  const formattedValue = new Intl.NumberFormat(i18n.language, {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(value);

  return <span>{formattedValue} {unit}</span>;
}
```

### Безопасность

#### Защита от XSS

**Меры:**
- React автоматически экранирует вывод
- Валидация всех пользовательских вводов
- Санитизация HTML в описаниях
- Content Security Policy headers

#### Защита данных метрик

**Меры:**
- HTTPS для всех запросов
- Проверка прав доступа на каждое действие
- Не хранить чувствительные метрики в localStorage
- Шифрование чувствительных данных при передаче

#### Аудит действий

**Логирование:**
- Все критичные действия (создание, активация, завершение, корректировка)
- Изменения параметров эксперимента
- Просмотр метрик (для аудита)
- Ошибки и исключения

### Мониторинг и аналитика

#### Метрики для отслеживания

**Производительность:**
- Время загрузки страницы
- Время ответа API метрик
- Время рендеринга графиков
- Количество ошибок

**Использование:**
- Количество созданных пилотов
- Количество активных пилотов
- Среднее время от создания до активации
- Частота просмотра метрик
- Популярные фильтры

**Бизнес-метрики:**
- Конверсия от черновика до активации
- Среднее время согласования
- Процент пилотов, требующих корректировки
- Процент успешно завершенных пилотов
- Средняя длительность пилотов

**Метрики качества данных:**
- Процент пилотов с заполненными метриками
- Частота обновления метрик
- Точность прогнозов vs фактических результатов

**Инструменты:**
- Google Analytics или аналоги
- Sentry для отслеживания ошибок
- Custom logging для бизнес-метрик
- Performance monitoring (Web Vitals)
- Grafana для визуализации метрик системы

### Интеграция с внешними системами

#### Потенциальные интеграции (не в MVP)

**Системы мониторинга рисков:**
- Автоматический сбор метрик из систем скоринга
- Уведомления о критичных отклонениях
- Интеграция с системами fraud detection

**Системы аналитики:**
- Экспорт данных в BI системы
- Интеграция с Tableau/Power BI
- API для внешних аналитических инструментов

**Системы уведомлений:**
- Email уведомления о статусе пилота
- Slack/Teams интеграция для команды
- SMS уведомления для критичных событий

### Рекомендации по развертыванию

#### Стратегия развертывания

**Поэтапное развертывание:**
1. Базовый функционал (CRUD пилотов)
2. Процесс согласования
3. Активация и управление жизненным циклом
4. Метрики и визуализация
5. Расширенная аналитика

**Feature flags:**
- Использовать feature flags для постепенного включения функций
- A/B тестирование новых возможностей
- Быстрый откат при проблемах

#### Мониторинг после развертывания

**Критичные метрики:**
- Количество ошибок при создании пилотов
- Время загрузки метрик
- Процент успешных активаций
- Отзывы пользователей

**Алерты:**
- Критичные ошибки в production
- Превышение времени ответа API
- Высокий процент неуспешных операций
