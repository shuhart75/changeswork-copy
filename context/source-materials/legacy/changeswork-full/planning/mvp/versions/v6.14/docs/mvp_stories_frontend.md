# Frontend Stories - Детальные описания

## FE-1: Настройка проекта и роутинг

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 2 дня
**Спринт:** 1
**Исполнитель:** Frontend Dev 1

### Описание
Настройка базовой структуры React приложения с роутингом, API клиентом и базовым Layout. Это фундамент для всей Frontend разработки.

### Технические требования
- React 18+ с TypeScript
- React Router v6
- Axios для API запросов
- Material-UI v5
- Vite или Create React App

### Acceptance Criteria
- [ ] React проект создан с TypeScript
- [ ] React Router настроен с маршрутами:
  - / - главная страница
  - /deployments - список Deployment
  - /deployments/:id - детальный просмотр Deployment
  - /simulations - список Simulation
  - /pilots - список Pilot
  - /changes - список Change
  - /scorecards - список Scorecard
  - /packages - список Package
  - /approvals - раздел согласований
  - /approval-routes - маршруты согласования (только Админ)
  - /users - управление пользователями (только Админ)
- [ ] Структура папок создана:
  ```
  src/
  ├── components/     # Переиспользуемые компоненты
  ├── views/          # Страницы/представления
  ├── services/       # API сервисы
  ├── utils/          # Утилиты
  ├── types/          # TypeScript типы
  ├── contexts/       # React Context
  └── App.tsx
  ```
- [ ] API клиент настроен (axios):
  - baseURL из environment variables
  - Interceptors для добавления auth token
  - Interceptors для обработки ошибок
- [ ] Environment variables настроены (.env файлы):
  - VITE_API_BASE_URL
  - VITE_ENV (dev/staging/prod)
- [ ] Layout компонент создан с:
  - Боковое меню (Drawer)
  - Header с названием приложения и пользователем
  - Breadcrumbs навигация
  - Content area
- [ ] Боковое меню содержит пункты:
  - Главная
  - Внедрения (Deployments)
  - Симуляции (Simulations)
  - Пилоты (Pilots)
  - Изменения (Changes)
  - Скоркарты (Scorecards)
  - Пакеты (Packages)
  - Мои согласования (Approvals) - только для Approver/Ratifier
  - Маршруты согласования (Approval Routes) - только для Админа
  - Пользователи (Users) - только для Админа
- [ ] Документация по структуре проекта создана (README.md)

### Зависимости
Нет

### Технические заметки
```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor для добавления auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## FE-2: Компоненты UI Kit

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Frontend Dev 1, Frontend Dev 2

### Описание
Создание переиспользуемых UI компонентов на базе Material-UI. Эти компоненты будут использоваться во всех разделах приложения для обеспечения единого стиля.

### Технические требования
- Material-UI v5
- TypeScript для типизации props
- Единый стиль согласно макету
- Responsive дизайн

### Acceptance Criteria
- [ ] Компонент DataTable создан:
  - Props: columns, data, loading, onRowClick, filters, sorting, pagination
  - Фильтрация по колонкам
  - Сортировка (ascending/descending)
  - Пагинация (page size: 20)
  - Loading состояние (skeleton)
  - Empty state (когда нет данных)
  - TypeScript интерфейсы для props
- [ ] Компонент FormField создан:
  - Обертка для TextField, Select, DatePicker
  - Единый стиль для всех полей
  - Отображение ошибок валидации
  - Required индикатор (*)
  - Props: label, value, onChange, error, helperText, required
- [ ] Компонент StatusBadge создан:
  - Цветные бейджи для статусов
  - Маппинг статус → цвет:
    - draft: grey
    - active: blue
    - pending_approval: orange
    - approved: green
    - deployed: green
    - rejected: red
    - failed: red
  - Props: status, label (optional)
- [ ] Компонент ConfirmDialog создан:
  - Диалог подтверждения действия
  - Props: open, title, message, onConfirm, onCancel
  - Кнопки: Отмена, Подтвердить
- [ ] Компонент FileUpload создан:
  - Drag-and-drop область
  - Кнопка выбора файла
  - Отображение выбранного файла
  - Прогресс-бар загрузки
  - Валидация размера и типа файла
  - Props: onUpload, maxSize, acceptedTypes
- [ ] Компонент CommentBox создан:
  - Текстовое поле для комментария
  - Счетчик символов
  - Props: value, onChange, maxLength, required
- [ ] Все компоненты типизированы (TypeScript)
- [ ] Компоненты переиспользуемые и не зависят от бизнес-логики
- [ ] Storybook настроен (опционально)
- [ ] Документация по использованию компонентов

### Зависимости
FE-1

### Технические заметки
```typescript
// src/components/StatusBadge.tsx
import { Chip } from '@mui/material';

interface StatusBadgeProps {
  status: string;
  label?: string;
}

const STATUS_COLORS: Record<string, 'default' | 'primary' | 'secondary' | 'error' | 'warning' | 'info' | 'success'> = {
  draft: 'default',
  active: 'info',
  pending_approval: 'warning',
  approved: 'success',
  deployed: 'success',
  rejected: 'error',
  failed: 'error',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label }) => {
  return (
    <Chip
      label={label || status}
      color={STATUS_COLORS[status] || 'default'}
      size="small"
    />
  );
};
```

---

## FE-3: Сервисы для работы с API

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 2 дня
**Спринт:** 1
**Исполнитель:** Frontend Dev 1

### Описание
Создание сервисов для взаимодействия с Backend API. Каждый сервис инкапсулирует логику работы с конкретной сущностью.

### Технические требования
- TypeScript интерфейсы для всех данных
- Обработка ошибок
- Toast уведомления при ошибках

### Acceptance Criteria
- [ ] DeploymentService создан с методами:
  - getAll(filters?, pagination?) → Promise<Deployment[]>
  - getById(id) → Promise<Deployment>
  - create(data) → Promise<Deployment>
  - update(id, data) → Promise<Deployment>
  - delete(id) → Promise<void>
- [ ] SimulationService создан с методами CRUD
- [ ] PilotService создан с методами CRUD
- [ ] ChangeService создан с методами:
  - CRUD методы
  - submit(id) → Promise<Change> (отправка на согласование)
- [ ] ScorecardService создан с методами CRUD
- [ ] LineageService создан с методами:
  - getByDeployment(deploymentId) → Promise<LineageData> (визуализация Lineage для Deployment)
  - getByChange(changeId) → Promise<LineageData> (визуализация Lineage для Change)
- [ ] PackageService создан с методами:
  - CRUD методы
  - submit(id) → Promise<Package> (отправка на согласование)
- [ ] ApprovalService создан с методами:
  - getInstances(filters?) → Promise<ApprovalInstance[]>
  - getInstanceById(id) → Promise<ApprovalInstance>
  - approve(id, comment?) → Promise<ApprovalInstance>
  - reject(id, comment) → Promise<ApprovalInstance>
  - getHistory(id) → Promise<ApprovalDecision[]>
- [ ] ArtifactService создан с методами:
  - getAll(entityType, entityId) → Promise<Artifact[]>
  - upload(file, entityType, entityId) → Promise<Artifact>
  - download(id) → Promise<Blob>
  - delete(id) → Promise<void>
- [ ] UserService создан с методами:
  - getAll(filters?) → Promise<User[]>
  - getById(id) → Promise<User>
  - assignRole(userId, role, productId?) → Promise<UserRole>
  - removeRole(roleId) → Promise<void>
- [ ] ApprovalRouteService создан с методами CRUD
- [ ] TypeScript интерфейсы созданы для всех сущностей:
  - Deployment, Simulation, Pilot, Change, Scorecard, Package
  - ApprovalRoute, ApprovalStage, ApprovalInstance, ApprovalDecision
  - Artifact, User, UserRole, LineageData
- [ ] Обработка ошибок реализована:
  - try/catch в каждом методе
  - Toast уведомления при ошибках
  - Логирование ошибок в console
- [ ] Документация по API методам

### Зависимости
FE-1, BE-5 - BE-15

### Технические заметки
```typescript
// src/services/DeploymentService.ts
import api from './api';
import { Deployment, DeploymentCreateData } from '../types';

export class DeploymentService {
  static async getAll(filters?: any): Promise<Deployment[]> {
    try {
      const response = await api.get('/deployments/', { params: filters });
      return response.data.results;
    } catch (error) {
      console.error('Error fetching deployments:', error);
      throw error;
    }
  }

  static async getById(id: string): Promise<Deployment> {
    try {
      const response = await api.get(`/deployments/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching deployment ${id}:`, error);
      throw error;
    }
  }

  static async create(data: DeploymentCreateData): Promise<Deployment> {
    try {
      const response = await api.post('/deployments/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating deployment:', error);
      throw error;
    }
  }

  // ... остальные методы
}
```

---

## FE-4: Управление состоянием (Context/Redux)

**Тип:** Task
**Приоритет:** High
**Оценка:** 2 дня
**Спринт:** 1
**Исполнитель:** Frontend Dev 1

### Описание
Настройка управления глобальным состоянием приложения с использованием React Context API. Необходимо создать контексты для аутентификации и уведомлений.

### Технические требования
- React Context API
- TypeScript для типизации
- Хуки для удобного использования

### Acceptance Criteria
- [ ] AuthContext создан:
  - State: currentUser, roles, isAuthenticated, loading
  - Methods: login(email, password), logout(), checkAuth()
  - Provider компонент
  - Хук useAuth() для использования в компонентах
- [ ] NotificationContext создан:
  - State: notifications (array)
  - Methods: showSuccess(message), showError(message), showInfo(message), hideNotification(id)
  - Provider компонент
  - Хук useNotification() для использования
  - Интеграция с Material-UI Snackbar
- [ ] ProtectedRoute компонент создан:
  - Проверка аутентификации
  - Redirect на /login если не аутентифицирован
  - Props: allowedRoles (optional) для проверки ролей
- [ ] RoleBasedRoute компонент создан:
  - Проверка роли пользователя
  - Redirect на /forbidden если нет прав
  - Props: allowedRoles (required)
- [ ] Хуки useAuth и useNotification экспортированы
- [ ] Providers обернуты вокруг App компонента
- [ ] Документация по использованию контекстов

### Зависимости
FE-1, FE-3

### Технические заметки
```typescript
// src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { User } from '../types';
import { UserService } from '../services/UserService';

interface AuthContextType {
  currentUser: User | null;
  roles: string[];
  isAuthenticated: boolean;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const checkAuth = async () => {
    try {
      const user = await UserService.getCurrentUser();
      setCurrentUser(user);
    } catch (error) {
      setCurrentUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const value = {
    currentUser,
    roles: currentUser?.roles || [],
    isAuthenticated: !!currentUser,
    loading,
    login: async (email, password) => {
      // Логика логина
    },
    logout: () => {
      localStorage.removeItem('authToken');
      setCurrentUser(null);
    },
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

---

## FE-5: Раздел Deployments

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 4 дня
**Спринт:** 2
**Исполнитель:** Frontend Dev 1

### User Story
Как ПРМ, я хочу просматривать список Deployment и создавать новые Deployment для своего продукта, чтобы группировать работу по внедрению риск-стратегий.

### Описание
Реализация раздела Deployments с списком, детальным просмотром, формами создания и редактирования.

### Технические требования
- Material-UI компоненты
- Responsive дизайн
- Фильтрация и пагинация
- Breadcrumbs навигация

### Acceptance Criteria
- [ ] DeploymentsView создан:
  - Список Deployment в виде таблицы (DataTable)
  - Колонки: Название, Продукт, Статус, Дата создания, Действия
  - Фильтрация: по продукту, статусу
  - Сортировка: по дате создания, названию
  - Пагинация: 20 элементов на страницу
  - Кнопка "Создать Deployment"
  - Клик по строке → переход на детальный просмотр
  - Loading состояние (skeleton)
  - Empty state (когда нет данных)
- [ ] DeploymentDetailView создан:
  - Breadcrumbs: Главная / Внедрения / {название}
  - Заголовок с названием и статусом (StatusBadge)
  - Табы:
    - Info: основная информация (название, описание, продукт, даты)
    - Simulations: список связанных Simulation
    - Pilots: список связанных Pilot
    - Changes: список связанных Change
    - Lineage: визуализация происхождения (граф связей)
    - Artifacts: список артефактов с возможностью добавления ссылок
  - Кнопки действий: Редактировать, Удалить (только для draft)
- [ ] CreateDeploymentForm создан:
  - Диалог или отдельная страница
  - Поля: Название (required), Описание (required), Продукт (select, required)
  - Валидация: все поля обязательны
  - Кнопки: Отмена, Создать
  - После создания → redirect на детальный просмотр
  - Toast уведомление об успехе/ошибке
- [ ] EditDeploymentForm создан:
  - Аналогично CreateDeploymentForm
  - Предзаполнение полей текущими значениями
  - Нельзя изменить продукт
  - После сохранения → обновление данных на странице
- [ ] Права доступа реализованы:
  - ПРМ видит Deployment по всем продуктам (read-only для чужих), но создавать/редактировать/отправлять на согласование может только Deployment своего продукта
  - Админ видит все Deployment
  - Кнопка "Создать" видна только ПРМ и Админу
  - Кнопки "Редактировать", "Удалить" видны только владельцу или Админу
- [ ] Responsive дизайн работает на всех разрешениях
- [ ] Unit тесты для компонентов (Jest + React Testing Library)
- [ ] Документация по использованию

### Зависимости
FE-1, FE-2, FE-3, FE-4, BE-5

---

## FE-6: Адаптация раздела Simulations

**Тип:** Task
**Приоритет:** High
**Оценка:** 3 дня
**Спринт:** 2
**Исполнитель:** Frontend Dev 2

### Описание
Адаптация существующего раздела Simulations под новый макет и новую модель данных. Необходимо добавить поле deployment_id и интегрировать с новым Layout.

### Технические требования
- Сохранить существующую функциональность
- Адаптировать под новый дизайн
- Добавить связь с Deployment

### Acceptance Criteria
- [ ] SimulationsView адаптирован под новый макет:
  - Использование DataTable компонента
  - Единый стиль с остальными разделами
  - Breadcrumbs навигация
- [ ] Добавлена фильтрация по deployment_id
- [ ] CreateSimulationForm обновлен:
  - Поле deployment_id (select, required)
  - Валидация: Simulation и Deployment в одном продукте
- [ ] SimulationDetailView обновлен:
  - Отображение связанного Deployment
  - Ссылка на Deployment
- [ ] EditSimulationForm обновлен:
  - Нельзя изменить deployment_id после создания
- [ ] Навигация через breadcrumbs работает
- [ ] Responsive дизайн
- [ ] Существующие unit тесты обновлены
- [ ] Новые тесты для deployment_id

### Зависимости
FE-1, FE-2, FE-3, FE-5, BE-6

---

## FE-7: Адаптация раздела Pilots

**Тип:** Task
**Приоритет:** High
**Оценка:** 4 дня
**Спринт:** 2
**Исполнитель:** Frontend Dev 2

### Описание
Адаптация существующего раздела Pilots под новую модель данных. Необходимо добавить deployment_id и связь со Scorecard (многие-ко-многим).

### Технические требования
- Сохранить существующую функциональность
- Добавить связь со Scorecard
- Multi-select для выбора Scorecard

### Acceptance Criteria
- [ ] PilotsView адаптирован под новый макет
- [ ] Добавлена фильтрация по deployment_id и scorecard_id
- [ ] CreatePilotForm обновлен:
  - Поле deployment_id (select, required)
  - Поле scorecards (multi-select, минимум 1)
  - Валидация: минимум 1 scorecard
  - Валидация: Pilot, Deployment и Scorecard в одном продукте
- [ ] PilotDetailView обновлен:
  - Таб Scorecards со списком связанных Scorecard
  - Отображение Deployment
  - Ссылки на Deployment и Scorecard
- [ ] EditPilotForm обновлен:
  - Можно изменить scorecards
  - Нельзя изменить deployment_id
- [ ] Навигация через breadcrumbs
- [ ] Responsive дизайн
- [ ] Unit тесты обновлены

### Зависимости
FE-1, FE-2, FE-3, FE-5, FE-8, BE-7

---

## FE-8: Раздел Scorecards

**Тип:** Story
**Приоритет:** High
**Оценка:** 4 дня
**Спринт:** 2
**Исполнитель:** Frontend Dev 1

### User Story
Как Методолог, я хочу создавать и управлять Scorecard, чтобы определять конфигурации скоринговых моделей для использования в Pilot и Change.

### Описание
Реализация раздела Scorecards с возможностью создания, просмотра и редактирования скоркарт.

### Acceptance Criteria
- [ ] ScorecardsView создан:
  - Список Scorecard в таблице
  - Колонки: Название, Версия, Продукт, Источник, Дата создания
  - Фильтрация: по продукту, источнику (simulation/pilot)
  - Кнопка "Создать Scorecard" (только Методолог и Админ)
- [ ] ScorecardDetailView создан:
  - Breadcrumbs навигация
  - Основная информация: название, описание, версия, продукт
  - Конфигурация (JSON, read-only или с подсветкой синтаксиса)
  - Источник (Simulation или Pilot, если есть)
  - Список Pilots использующих эту Scorecard
  - Список Changes использующих эту Scorecard
  - Кнопки: Редактировать (только Методолог), Удалить (только Методолог, если не используется)
- [ ] CreateScorecardForm создан:
  - Поля: Название, Описание, Версия, Продукт, Конфигурация (textarea для JSON)
  - Опционально: Источник (select: Simulation/Pilot), Source ID
  - Валидация JSON конфигурации
  - Права: только Методолог или Админ
- [ ] EditScorecardForm создан:
  - Аналогично CreateScorecardForm
  - Нельзя изменить продукт и источник
  - Права: только Методолог или Админ
- [ ] Валидация: нельзя удалить Scorecard, используемую в Pilot или Change
- [ ] Права доступа реализованы:
  - Все роли могут просматривать
  - Только Методолог и Админ могут создавать/редактировать/удалять
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-4, BE-8

---

## FE-9: Раздел Changes

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 5 дней
**Спринт:** 3
**Исполнитель:** Frontend Dev 1

### User Story
Как ПРМ, я хочу создавать Change и отправлять их на согласование, чтобы внедрять утвержденные изменения в продуктовую среду.

### Описание
Реализация раздела Changes - ключевой сущности для продуктового внедрения.

### Acceptance Criteria
- [ ] ChangesView создан:
  - Список Change в таблице
  - Колонки: Название, Deployment, Статус, Критичность, Плановая дата, Дата создания
  - Фильтрация: по deployment, статусу, критичности
  - Сортировка: по критичности, плановой дате, дате создания
  - Кнопка "Создать Change"
  - Цветовая индикация критичности (low: green, medium: yellow, high: orange, critical: red)
- [ ] ChangeDetailView создан:
  - Breadcrumbs навигация
  - Заголовок с названием, статусом и критичностью
  - Табы:
    - Info: основная информация (название, описание, deployment, критичность, плановая дата, даты внедрения/отката)
    - Scorecards: список связанных Scorecard
    - Artifacts: список артефактов с возможностью добавления ссылок
    - Approval History: история согласований (если Change был на согласовании)
  - Кнопки действий:
    - Редактировать (только для draft)
    - Удалить (только для draft)
- [ ] CreateChangeForm создан:
  - Поля:
    - Название (required)
    - Описание (required)
    - Deployment (select, required)
    - Scorecards (multi-select, минимум 1, required)
    - Критичность (select: low/medium/high/critical, required)
    - Плановая дата внедрения (date picker, required)
  - Валидация: минимум 1 scorecard
  - Валидация: Change, Deployment и Scorecard в одном продукте
  - Права: ПРМ своего продукта или Админ
- [ ] EditChangeForm создан:
  - Можно редактировать только в статусе draft
  - Нельзя изменить deployment_id
  - Можно изменить scorecards, критичность, плановую дату
- [ ] Отображение истории согласований:
  - Этапы согласования
  - Решения Approver/Ratifier (approved/rejected)
  - Комментарии
  - Даты решений
- [ ] Права доступа реализованы
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-4, FE-5, FE-8, BE-9

---

## FE-10: Компонент LineageVisualization

**Тип:** Story
**Приоритет:** High
**Оценка:** 3 дня
**Спринт:** 3
**Исполнитель:** Frontend Dev 1

### User Story
Как ПРМ, я хочу видеть визуализацию Lineage (происхождения) для Deployment или Change, чтобы понимать полный путь внедрения стратегии через Simulation → Pilot → Change.

### Описание
Реализация компонента визуализации Lineage (происхождения). Lineage НЕ является CRUD-сущностью - это визуализация связей "создано из", которые отслеживаются через Scorecards и таблицы источников.

### Acceptance Criteria
- [ ] LineageVisualization компонент создан:
  - Принимает props: deploymentId или changeId
  - Загружает данные через LineageService
  - Визуализирует граф связей (узлы: Simulation/Pilot/Change, рёбра: связи через Scorecards)
  - Использует библиотеку для графов (react-flow, vis.js или аналог)
- [ ] Интеграция в DeploymentDetailView:
  - Новый таб "Lineage"
  - Показывает весь Lineage Deployment (все связи)
  - Интерактивность: клик на узел открывает детальный просмотр сущности
- [ ] Интеграция в ChangeDetailView:
  - Новый таб "Lineage"
  - Показывает Lineage конкретного Change (путь от Simulation через Pilot к Change)
  - Интерактивность: клик на узел открывает детальный просмотр
- [ ] Визуализация графа:
  - Узлы разных типов (Simulation/Pilot/Change) имеют разные цвета/иконки
  - Рёбра показывают направление связи (стрелки)
  - Tooltip при наведении на узел (краткая информация)
  - Zoom и pan для больших графов
- [ ] Обработка пустого Lineage:
  - Если нет связей - показать сообщение "Нет данных о происхождении"
- [ ] Loading состояние при загрузке данных
- [ ] Обработка ошибок
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-5, FE-6, FE-7, FE-9, BE-10

---

## FE-12: Диалог создания Package и отправки на утверждение

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 4 дня
**Спринт:** 3
**Исполнитель:** Frontend Dev 2

### User Story
Как ПРМ, я хочу создать Package для группировки Pilot/Change и отправить их на утверждение (Ratification) одновременно, чтобы ускорить процесс утверждения.

### Описание
Реализация диалога для создания Package и отправки на утверждение (Ratification). Package создаётся и отправляется на утверждение одновременно (НЕТ draft состояния). Package группирует Pilot/Change (не Chain) для совместного утверждения.

### Acceptance Criteria
- [ ] SubmitToRatificationDialog компонент создан:
  - Диалог открывается из PilotDetailView или ChangeDetailView
  - Поля:
    - Название Package (required)
    - Описание Package (required)
    - Pilot/Change для включения (multi-select, минимум 1)
    - Ratifier (select из пользователей с ролью ratifier, required)
  - Критичность отображается автоматически (MAX от выбранных Pilot/Change)
  - Валидация: минимум 1 Pilot/Change выбран
  - Валидация: все выбранные Pilot/Change из одного продукта
  - Кнопка "Отправить на утверждение" создаёт Package и ApprovalInstance одновременно
  - После успешной отправки: закрытие диалога, toast уведомление, обновление данных
- [ ] Интеграция в PilotDetailView:
  - Кнопка "Отправить на утверждение" (только для Pilot в статусе requires_activation или requires_correction)
  - При клике открывается SubmitToRatificationDialog с предвыбранным текущим Pilot
- [ ] Интеграция в ChangeDetailView:
  - Кнопка "Отправить на утверждение" (только для Change в статусе requires_approval)
  - При клике открывается SubmitToRatificationDialog с предвыбранным текущим Change
- [ ] PackagesView создан (список отправленных Package):
  - Список Package в таблице
  - Колонки: Название, Критичность, Количество элементов, Ratifier, Статус, Дата создания
  - Фильтрация: по критичности, статусу
  - Сортировка: по критичности, дате создания
  - Цветовая индикация критичности
- [ ] PackageDetailView создан:
  - Breadcrumbs навигация
  - Заголовок с названием и критичностью
  - Табы:
    - Info: основная информация (название, описание, критичность, Ratifier)
    - Items: список Pilot/Change в Package (таблица с типом, названием, статусом)
    - Approval History: история согласований (этапы, решения, комментарии)
- [ ] Отображение истории согласований:
  - Текущий этап (Approval/Ratification)
  - Список решений по каждому этапу
  - Approver/Ratifier, их решения и комментарии
  - Даты решений
- [ ] Права доступа реализованы:
  - ПРМ видит Package по всем продуктам (read-only для чужих элементов)
  - Кнопка "Отправить на утверждение" видна только если у пользователя есть права отправки выбранных элементов (обычно элементы его продукта)
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-4, FE-7, FE-9, FE-11, BE-12

---

## FE-13: Раздел "Мои согласования"

**Тип:** Story
**Приоритет:** Critical
**Оценка:** 5 дней
**Спринт:** 3-4
**Исполнитель:** Frontend Dev 2

### User Story
Как Approver или Ratifier, я хочу видеть список Package на согласовании/утверждении и принимать решения (согласовать/отклонить), чтобы контролировать внедрение изменений.

### Описание
Реализация раздела для Approver и Ratifier - ключевой интерфейс для процесса согласования.

### Acceptance Criteria
- [ ] ApprovalsView создан:
  - Список Package на согласовании (только назначенные текущему пользователю)
  - Колонки: Название Package, Текущий этап, Статус, Критичность, Дата отправки
  - Фильтрация: по этапу (approval/ratification), статусу (pending/approved/rejected)
  - Сортировка: по критичности, дате отправки
  - Цветовая индикация критичности и статуса
  - Индикатор "Требует моего решения" (если пользователь еще не принял решение)
- [ ] ApprovalDetailView создан:
  - Breadcrumbs навигация
  - Заголовок с названием Package, статусом и критичностью
  - Информация о Package:
    - Название, описание
    - Текущий этап (approval/ratification)
    - Список Pilot/Change в Package
  - Детали каждого Pilot/Change:
    - Тип (Pilot/Change)
    - Deployment
    - Основная информация
    - Связанные Scorecards
  - Текущий этап согласования:
    - Список Approver/Ratifier этапа
    - Статус каждого (ожидает/согласовал/отклонил)
    - Комментарии
  - История предыдущих этапов (если есть)
  - Кнопки действий (если пользователь еще не принял решение):
    - "Согласовать" (зеленая кнопка)
    - "Отклонить" (красная кнопка)
- [ ] Диалог согласования создан:
  - Открывается при клике на "Согласовать"
  - Поле комментария (optional)
  - Подтверждение: "Вы уверены, что хотите согласовать?"
  - Кнопки: Отмена, Согласовать
- [ ] Диалог отклонения создан:
  - Открывается при клике на "Отклонить"
  - Поле комментария (required)
  - Валидация: комментарий опционален при отклонении
  - Подтверждение: "Вы уверены, что хотите отклонить?"
  - Кнопки: Отмена, Отклонить
- [ ] После принятия решения:
  - Toast уведомление об успехе
  - Обновление статуса на странице
  - Если все Approver/Ratifier этапа приняли решение:
    - Отображение перехода на следующий этап или завершения
- [ ] История согласований отображается:
  - Все этапы
  - Решения всех Approver/Ratifier
  - Комментарии
  - Даты решений
- [ ] Права доступа:
  - Только назначенные Approver/Ratifier видят Package
  - Только Approver/Ratifier текущего этапа могут принимать решения
  - Нельзя изменить решение после принятия
- [ ] Уведомления:
  - Бейдж с количеством Package, требующих решения
  - Выделение Package, требующих решения
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-4, FE-12, BE-13

---

## FE-14: Управление артефактами

**Тип:** Task
**Приоритет:** Medium
**Оценка:** 3 дня
**Спринт:** 2-4
**Исполнитель:** Frontend Dev 2

### Описание
Реализация функционала работы с артефактами (документами) для Deployment и Change.

### Технические требования
- Drag-and-drop загрузка
- Прогресс-бар
- Валидация размера и типа файла

### Acceptance Criteria
- [ ] ArtifactsList компонент создан:
  - Список артефактов в виде таблицы
  - Колонки: Название файла, Размер, Тип, Загрузил, Дата загрузки, Действия
  - Кнопка "Загрузить файл"
  - Для каждого артефакта:
    - Иконка типа файла (PDF/DOCX/XLSX)
    - Кнопка скачивания
    - Кнопка удаления (только для владельца или Методолога)
  - Empty state (когда нет артефактов)
- [ ] UploadArtifactDialog компонент создан:
  - Диалог загрузки файла
  - Drag-and-drop область
  - Кнопка "Выбрать файл"
  - Отображение выбранного файла:
    - Название
    - Размер
    - Тип
  - Валидация:
    - Размер <= 10 MB (показать ошибку если больше)
    - Тип: PDF, DOCX, XLSX (показать ошибку если другой)
  - Прогресс-бар загрузки
  - Кнопки: Отмена, Загрузить
- [ ] Скачивание файла реализовано:
  - Клик по кнопке скачивания → файл скачивается
  - Правильное имя файла
  - Правильный Content-Type
- [ ] Удаление файла реализовано:
  - Диалог подтверждения: "Вы уверены, что хотите удалить файл?"
  - После удаления: обновление списка, toast уведомление
  - Права: только владелец или Методолог или Админ
- [ ] Интеграция с DeploymentDetailView:
  - Таб "Artifacts" с ArtifactsList
  - Кнопка "Загрузить файл"
- [ ] Интеграция с ChangeDetailView:
  - Таб "Artifacts" с ArtifactsList
  - Кнопка "Загрузить файл"
- [ ] Права доступа реализованы:
  - ПРМ управляет артефактами своих сущностей
  - Методолог управляет артефактами всех сущностей
  - Админ управляет всеми артефактами
- [ ] Обработка ошибок:
  - Файл слишком большой → toast с ошибкой
  - Неподдерживаемый тип → toast с ошибкой
  - Ошибка загрузки → toast с ошибкой
- [ ] Responsive дизайн
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-5, FE-9, BE-14

---

## FE-16: Главная страница (Dashboard)

**Тип:** Task
**Приоритет:** Low
**Оценка:** 3 дня
**Спринт:** 1
**Исполнитель:** Frontend Dev 2

### Описание
Реализация главной страницы с метриками и быстрыми ссылками.

### Технические требования
- Карточки с метриками
- Адаптивная верстка
- Быстрые ссылки

### Acceptance Criteria
- [ ] Dashboard создан с карточками метрик:
  - Для ПРМ:
    - Количество активных Deployments
    - Количество Changes на согласовании
    - Количество Changes в draft
  - Для Approver/Ratifier:
    - Количество Package, требующих моего решения
    - Количество Package на согласовании (всего)
  - Для Методолога:
    - Количество Scorecard
    - Количество Scorecard, используемых в активных Pilot/Change
  - Для Админа:
    - Все метрики выше
    - Количество пользователей
    - Количество маршрутов согласования
- [ ] Список последних действий:
  - Последние 10 действий пользователя
  - Тип действия (создание, обновление, согласование)
  - Сущность (Deployment, Change, Package)
  - Дата и время
  - Ссылка на сущность
- [ ] Быстрые ссылки:
  - Создать Deployment
  - Создать Change
  - Мои согласования (для Approver/Ratifier)
  - Создать Scorecard (для Методолога)
- [ ] Метрики обновляются при загрузке страницы
- [ ] Responsive дизайн (карточки адаптируются под размер экрана)
- [ ] Unit тесты

### Зависимости
FE-1, FE-2, FE-3, FE-4

---

## FE-17: Интеграция с Backend API

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 4
**Исполнитель:** Frontend Dev 1

### Описание
Интеграция всех Frontend компонентов с Backend API, обработка ошибок и edge cases.

### Технические требования
- Обработка всех типов ошибок
- Retry логика для сетевых ошибок
- Loading состояния

### Acceptance Criteria
- [ ] Все API вызовы проверены и работают корректно:
  - Deployment CRUD
  - Simulation CRUD
  - Pilot CRUD
  - Change CRUD + submit
  - Scorecard CRUD
  - Lineage GET (визуализация)
  - Package создание и отправка на утверждение
  - Approval approve/reject
  - Artifact links (добавление/обновление/удаление ссылок)
  - User roles
  - Approval routes CRUD
- [ ] Обработка ошибок реализована для всех сценариев:
  - 400 Bad Request → toast с описанием ошибки валидации
  - 401 Unauthorized → redirect на /login
  - 403 Forbidden → toast "У вас нет прав для этого действия"
  - 404 Not Found → toast "Сущность не найдена" или страница 404
  - 500 Internal Server Error → toast "Ошибка сервера, попробуйте позже"
  - Network Error → toast "Ошибка сети, проверьте подключение"
- [ ] Toast уведомления реализованы:
  - Успешные операции: зеленый toast с сообщением
  - Ошибки: красный toast с описанием ошибки
  - Информационные: синий toast
  - Автоматическое закрытие через 5 секунд
  - Возможность закрыть вручную
- [ ] Loading состояния реализованы:
  - Skeleton для списков (пока загружаются данные)
  - Spinner для форм (пока отправляется запрос)
  - Disabled кнопки во время отправки
  - Loading индикатор для страниц
- [ ] Retry логика реализована:
  - При сетевых ошибках: автоматический retry (1 попытка)
  - Exponential backoff для повторных запросов
  - Показать пользователю, что идет повторная попытка
- [ ] Оптимистичные обновления (optional):
  - При создании/обновлении: сразу обновить UI, откатить при ошибке
- [ ] Документация по обработке ошибок

### Зависимости
FE-5 - FE-15, BE-5 - BE-15

---

## FE-18: E2E тесты (Cypress/Playwright)

**Тип:** Task
**Приоритет:** High
**Оценка:** 4 дня
**Спринт:** 4
**Исполнитель:** Frontend Dev 1

### Описание
Написание E2E тестов для критичных сценариев работы системы.

### Технические требования
- Cypress или Playwright
- Тесты для happy path и негативных сценариев
- Автоматический запуск в CI/CD

### Acceptance Criteria
- [ ] E2E тесты для happy path:
  - Тест: Создание Deployment → Simulation → Pilot → Change → Визуализация Lineage → Package → Согласование
    - Логин как ПРМ
    - Создание Initiative
    - Создание Simulation (связь с Initiative)
    - Создание Scorecard (как Методолог)
    - Создание Pilot (связь с Initiative и Scorecard)
    - Создание Deployment (связь с Initiative и Scorecard)
    - Визуализация Lineage (проверка связей через Scorecards)
    - Создание Package (группировка Pilot/Deployment) и отправка на утверждение
    - Логин как Approver
    - Согласование на этапе approval
    - Логин как Ratifier
    - Утверждение на этапе ratification
    - Проверка: Deployment в статусе approved
- [ ] E2E тесты для негативных сценариев:
  - Тест: Отклонение на первом этапе
    - Создание и отправка Package
    - Approver отклоняет на этапе approval
    - Проверка: Package в статусе rejected
  - Тест: Попытка создать Deployment чужого продукта
    - Логин как ПРМ продукта A
    - Попытка создать Deployment для продукта B
    - Проверка: ошибка 403
  - Тест: Попытка согласовать не назначенный Package
    - Логин как Approver, не назначенный на Package
    - Попытка согласовать Package
    - Проверка: ошибка 403 или Package не виден
- [ ] E2E тесты для разных ролей:
  - Тест: ПРМ видит все Deployment, но может изменять только свои
  - Тест: Методолог создает Scorecard
  - Тест: Approver видит только назначенные Package на этапе Approval
  - Тест: Ratifier видит только назначенные Package на этапе Ratification
  - Тест: Админ видит все сущности
- [ ] E2E тесты для артефактов:
  - Добавление ссылки на документ к Change
  - Обновление ссылки
  - Удаление ссылки
  - Попытка добавить невалидный URL (ошибка)
- [ ] Тесты запускаются автоматически:
  - Настроен CI/CD pipeline
  - Тесты запускаются при каждом PR
  - Отчет о результатах тестов
- [ ] Coverage отчет:
  - E2E тесты покрывают критичные сценарии
  - Отчет генерируется автоматически
- [ ] Документация по запуску тестов:
  - Инструкция по локальному запуску
  - Инструкция по запуску в CI/CD

### Зависимости
FE-5 - FE-15, BE-17

---

## FE-19: Оптимизация производительности

**Тип:** Task
**Приоритет:** Medium
**Оценка:** 2 дня
**Спринт:** 4
**Исполнитель:** Frontend Dev 2

### Описание
Оптимизация производительности приложения для улучшения пользовательского опыта.

### Технические требования
- Code splitting
- Мемоизация
- Виртуализация длинных списков
- Bundle size анализ

### Acceptance Criteria
- [ ] Code splitting реализован:
  - Lazy loading для всех маршрутов (React.lazy + Suspense)
  - Отдельные chunks для каждого раздела
  - Loading индикатор при загрузке chunk
- [ ] Мемоизация компонентов:
  - React.memo для тяжелых компонентов (DataTable, LineageVisualization)
  - useMemo для дорогих вычислений
  - useCallback для функций, передаваемых в дочерние компоненты
- [ ] Оптимизация ре-рендеров:
  - Проверка ненужных ре-рендеров (React DevTools Profiler)
  - Оптимизация Context (разделение на несколько контекстов)
  - Использование useReducer для сложного state
- [ ] Виртуализация длинных списков:
  - Использование react-window или react-virtualized
  - Виртуализация для списков > 100 элементов
  - Применено к: DeploymentsView, ChangesView, PackagesView
- [ ] Bundle size анализ:
  - Использование webpack-bundle-analyzer
  - Удаление неиспользуемых зависимостей
  - Tree shaking настроен
  - Bundle size < 500KB (gzipped)
- [ ] Lighthouse audit:
  - Performance score > 90
  - Accessibility score > 90
  - Best Practices score > 90
  - SEO score > 90
- [ ] Оптимизация изображений:
  - Использование WebP формата
  - Lazy loading для изображений
- [ ] Документация по оптимизации:
  - Список примененных оптимизаций
  - Рекомендации для будущих разработчиков

### Зависимости
FE-5 - FE-15

---

## FE-20: Финальное тестирование и баг-фиксы

**Тип:** Task
**Приоритет:** Critical
**Оценка:** 3 дня
**Спринт:** 4
**Исполнитель:** Frontend Dev 1, Frontend Dev 2

### Описание
Финальное тестирование всего приложения, исправление найденных багов и подготовка к релизу.

### Технические требования
- Ручное тестирование всех сценариев
- Кросс-браузерное тестирование
- Responsive тестирование

### Acceptance Criteria
- [ ] Ручное тестирование всех сценариев:
  - Полный цикл: Deployment → Simulation → Pilot → Change → Визуализация Lineage → Package → Согласование
  - Все CRUD операции для всех сущностей
  - Все формы и валидация
  - Все права доступа для разных ролей
  - Артефакты: добавление ссылок, обновление, удаление
  - Процесс согласования: отправка, согласование, отклонение
- [ ] Кросс-браузерное тестирование:
  - Chrome (последняя версия)
  - Firefox (последняя версия)
  - Safari (последняя версия)
  - Edge (последняя версия)
  - Все функции работают на всех браузерах
  - Нет визуальных багов
- [ ] Responsive тестирование:
  - Desktop (1920x1080, 1366x768)
  - Tablet (768x1024)
  - Mobile (375x667, 414x896)
  - Все компоненты адаптируются корректно
  - Навигация работает на всех устройствах
  - Формы удобны для заполнения на мобильных
- [ ] Список найденных багов:
  - Все критичные баги исправлены
  - Все высокоприоритетные баги исправлены
  - Средние и низкие баги задокументированы (для будущих версий)
- [ ] Проверка производительности:
  - Время загрузки главной страницы < 2 сек
  - Время загрузки списков < 1 сек
  - Время отклика форм < 500 мс
  - Нет memory leaks
- [ ] Проверка доступности (Accessibility):
  - Навигация с клавиатуры работает
  - Screen reader friendly
  - Контрастность текста достаточная
  - ARIA атрибуты добавлены где необходимо
- [ ] Финальная проверка:
  - Все функции работают согласно требованиям
  - Нет критичных багов
  - Документация актуальна
  - README обновлен
  - Готовность к релизу подтверждена
- [ ] Документация по найденным багам и их исправлениям

### Зависимости
FE-5 - FE-19

---

## Итого Frontend: 20 задач, 61 день

**Критический путь:**
FE-1 → FE-2 → FE-3 → FE-5 → FE-9 → FE-10 → FE-12 → FE-13 → FE-17 → FE-18 → FE-20

**Ключевые задачи:**
- FE-1, FE-2, FE-3: Инфраструктура (фундамент)
- FE-5, FE-9: Основные разделы (Deployments, Changes)
- FE-12, FE-13: Процесс согласования (ключевая функциональность)
- FE-17: Интеграция с Backend (критично для работы)
- FE-18: E2E тесты (качество)
- FE-20: Финальное тестирование (готовность к релизу)

**Распределение:**
- Frontend Dev 1: 30.5 дней (основной поток - разделы и интеграция)
- Frontend Dev 2: 30.5 дней (поддержка - адаптация, согласование, артефакты)
