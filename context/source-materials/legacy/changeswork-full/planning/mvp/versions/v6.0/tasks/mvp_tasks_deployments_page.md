# Задачи для страницы "Внедрения" (Deployments)

## Обзор страницы

**Страница:** Список внедрений (Deployments List View)
**Путь в макете:** Боковое меню → "Внедрения"
**Статус:** Новая страница, требует полной реализации

### Что показывает страница (из макета):

**Табличное представление со столбцами:**
- ID (DEP-XXX)
- Название внедрения
- Продукт
- Статус (draft/active/deployed/archived)
- Автор
- Дата создания

**Функционал:**
- Фильтрация по продукту (dropdown)
- Поиск по названию
- Сортировка по столбцам
- Пагинация
- Кнопка "Создать внедрение" (только для ПРМ своего продукта)
- Клик на строку → переход к детальному просмотру

**Права доступа:**
- ПРМ видит только внедрения своего продукта
- Методолог видит все внедрения и может создавать
- Админ видит все внедрения

---

## AN-D1: Аналитика страницы "Внедрения"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 2 дня

### Summary
Детализация требований и проектирование UI/UX для страницы списка внедрений

### Description

Провести аналитику и детализацию требований для страницы "Внедрения":

1. **Детализация бизнес-требований:**
   - Уточнить правила фильтрации по продуктам
   - Определить правила сортировки по умолчанию
   - Уточнить логику отображения статусов
   - Определить правила доступа для разных ролей

2. **Спецификация UI/UX:**
   - Wireframe списка внедрений (таблица)
   - Спецификация фильтров и поиска
   - Дизайн статусных бейджей
   - Спецификация пагинации
   - Адаптивность (desktop/tablet/mobile)

3. **Спецификация API контракта:**
   - GET /api/deployments/ - список с фильтрацией
   - Параметры запроса (product_id, status, search, page, page_size, ordering)
   - Формат ответа (список + метаданные пагинации)
   - Коды ошибок (403, 404, 500)

4. **Определение полей таблицы:**
   - ID (формат DEP-XXX)
   - Название (обязательное, кликабельное)
   - Продукт (название продукта)
   - Статус (цветной бейдж с автоматическим расчетом)
   - Автор (ФИО или username)
   - Дата создания (формат DD.MM.YYYY HH:MM)

5. **Правила валидации:**
   - Минимальная длина названия
   - Уникальность названия в рамках продукта
   - Обязательность выбора продукта

### Acceptance Criteria

- [ ] Бизнес-требования задокументированы и согласованы
- [ ] Wireframe страницы готов (Figma/Sketch или описание)
- [ ] API контракт задокументирован (OpenAPI спецификация или описание)
- [ ] Определены все поля таблицы с типами данных
- [ ] Правила фильтрации и сортировки описаны
- [ ] Права доступа для ролей определены
- [ ] Правила валидации описаны
- [ ] Адаптивность для разных разрешений учтена
- [ ] Документ согласован с заказчиком

### Dependencies
Нет

### Deliverables
- Документ "Спецификация страницы Внедрения" (markdown/confluence)
- API контракт для GET /api/deployments/
- Wireframe или описание UI

---

## BE-D1: Backend для страницы "Внедрения"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Реализация API endpoint для списка внедрений с фильтрацией, пагинацией и правами доступа

### Description

Реализовать Backend API для страницы списка внедрений:

1. **Миграция БД (если требуется):**
   - Проверить наличие всех необходимых полей в таблице `deployment`
   - Добавить индексы для фильтрации (product_id, status, created_at)
   - Добавить индекс для поиска по названию (GIN/GIST для PostgreSQL)
   - **КРИТИЧНО:** Миграция данных - раскидать все существующие пилоты и симуляции по внедрениям
     - В новой архитектуре пилоты и симуляции ОБЯЗАТЕЛЬНО должны принадлежать внедрению (deployment_id NOT NULL)
     - Необходимо вручную или через скрипт миграции назначить deployment_id для всех существующих записей
     - Варианты:
       1. Создать "дефолтные" внедрения для каждого продукта и привязать к ним orphan-сущности
       2. Проанализировать существующие данные и сгруппировать по смыслу
       3. Создать одно техническое внедрение "Миграция из старой системы" для каждого продукта
     - После миграции данных добавить constraint NOT NULL на поля simulation.deployment_id и pilot.deployment_id

2. **API Endpoint: GET /api/deployments/**

   **Параметры запроса:**
   - `product_id` (optional) - фильтр по продукту (показывать ВСЕ продукты в dropdown)
   - `status` (optional) - фильтр по статусу (draft/active/deployed/archived)
   - `search` (optional) - поиск по названию И описанию (case-insensitive, partial match)
   - `page` (optional, default=1) - номер страницы
   - `page_size` (optional, default=20) - размер страницы
   - `ordering` (optional, default='-created_at') - сортировка по дате создания (новые первые)

   **Формат ответа:**
   ```json
   {
     "count": 42,
     "next": "http://api/deployments/?page=2",
     "previous": null,
     "results": [
       {
         "id": "uuid",
         "display_id": "DEP-001",
         "name": "Оптимизация риск-стратегии Premium карт",
         "description": "Полное описание внедрения...",
         "product": {
           "id": "credit_cards",
           "label": "Кредитные карты"
         },
         "status": "active",
         "status_calculated": true,
         "status_reason": "Есть активные пилоты",
         "created_at": "2026-03-01T10:00:00Z",
         "created_by": {
           "id": "user-uuid",
           "full_name": "Иван Иванов"
         }
       }
     ]
   }
   ```

3. **Бизнес-логика:**
   - Автоматический расчет статуса (draft/active/deployed/archived)
   - Фильтрация по правам доступа:
     - ПРМ видит только свой продукт
     - Методолог видит все и может создавать
     - Админ видит все
   - Поиск по названию И описанию (case-insensitive, ILIKE для PostgreSQL)
   - Фильтр по продукту показывает ВСЕ продукты (не только доступные пользователю)

4. **Права доступа:**
   - Middleware проверяет роль пользователя
   - Автоматическая фильтрация по product_id для ПРМ
   - HTTP 403 если ПРМ пытается получить чужой продукт

5. **Оптимизация:**
   - Select related для product и created_by (избежать N+1)
   - Annotate для счетчиков (один запрос вместо множества)
   - Кэширование списка продуктов (если не меняется часто)

### Acceptance Criteria

- [ ] Миграция БД применена (если требуется)
- [ ] **Миграция данных выполнена: все существующие пилоты и симуляции привязаны к внедрениям**
- [ ] **Constraint NOT NULL добавлен на simulation.deployment_id и pilot.deployment_id**
- [ ] Индексы созданы для оптимизации
- [ ] GET /api/deployments/ endpoint реализован
- [ ] Фильтрация по product_id, status работает
- [ ] Поиск по названию И описанию работает (case-insensitive)
- [ ] Пагинация работает корректно (default page_size=20)
- [ ] Сортировка по умолчанию: -created_at (новые первые)
- [ ] Статус рассчитывается автоматически с флагом status_calculated
- [ ] Права доступа реализованы (ПРМ видит только свой продукт)
- [ ] HTTP 403 возвращается при попытке доступа к чужому продукту
- [ ] Select related/annotate оптимизация применена
- [ ] Unit тесты покрывают все сценарии (coverage > 80%)
- [ ] Integration тесты для прав доступа
- [ ] API документация обновлена (Swagger/OpenAPI)
- [ ] Postman коллекция с примерами запросов

### Dependencies
- AN-D1 (требуется API контракт)
- BE-1 (таблица deployment должна существовать)
- BE-4 (ORM модели должны быть готовы)

### Technical Notes

**Пример запроса:**
```bash
GET /api/deployments/?product_id=credit_cards&status=active&search=премиум&page=1&page_size=20&ordering=-created_at
```

**Пример SQL оптимизации (Django ORM):**
```python
from django.db.models import Q

Deployment.objects.filter(
    Q(name__icontains=search) | Q(description__icontains=search),
    product_id=product_id,
    status=status
).select_related(
    'product', 'created_by'
).order_by('-created_at')  # По умолчанию: новые первые
```

---

## FE-D1: Frontend для страницы "Внедрения"

**Тип:** Story
**Приоритет:** Критический
**Оценка:** 3 дня

### Summary
Реализация UI страницы списка внедрений с таблицей, фильтрами, поиском и пагинацией

### Description

Реализовать Frontend для страницы списка внедрений:

1. **Компонент DeploymentsView:**
   - Табличное представление (Material-UI Table)
   - Столбцы: ID (DEP-XXX), Название, Продукт, Статус, Автор, Дата создания
   - Responsive дизайн (на мобильных - карточки вместо таблицы)

2. **Фильтры и поиск:**
   - Dropdown фильтр по продукту (ВСЕ продукты системы)
   - Dropdown фильтр по статусу (draft/active/deployed/archived)
   - Поле поиска по названию И описанию (debounce 300ms)
   - Кнопка "Сбросить фильтры"

3. **Сортировка:**
   - По умолчанию: по дате создания (новые первые)
   - Клик на заголовок столбца → сортировка
   - Индикатор направления сортировки (стрелка вверх/вниз)
   - Сортировка по: Название, Дата создания, Статус

4. **Пагинация:**
   - Material-UI Pagination компонент
   - Показывать "Показано X-Y из Z"
   - Выбор размера страницы (10/20/50)

5. **Статусные бейджи:**
   - draft: серый
   - active: синий
   - deployed: зеленый
   - archived: серый с opacity

6. **Кнопка "Создать внедрение":**
   - Показывается для ПРМ и Методолога
   - Disabled если не выбран продукт в фильтре
   - Открывает форму создания (отдельная задача)

7. **Навигация:**
   - Клик на строку → переход к детальному просмотру
   - Breadcrumbs: "Внедрения"

8. **Loading и Error состояния:**
   - Skeleton loader при загрузке
   - Error message при ошибке API
   - Empty state если нет данных

9. **API интеграция:**
    - DeploymentService.getList(filters, page, pageSize, ordering)
    - Обработка ошибок (403, 404, 500)
    - Toast уведомления при ошибках

### Acceptance Criteria

- [ ] DeploymentsView компонент реализован
- [ ] Таблица отображает все столбцы корректно
- [ ] Фильтр по продукту работает (показывает ВСЕ продукты)
- [ ] Фильтр по статусу работает
- [ ] Поиск по названию И описанию работает (с debounce)
- [ ] Сортировка по столбцам работает
- [ ] Пагинация работает корректно
- [ ] Статусные бейджи отображаются с правильными цветами
- [ ] Кнопка "Создать" показывается для ПРМ и Методолога
- [ ] Клик на строку открывает детальный просмотр
- [ ] Breadcrumbs отображается корректно
- [ ] Loading состояние (skeleton) работает
- [ ] Error состояние отображается
- [ ] Empty state отображается если нет данных
- [ ] Responsive дизайн работает (desktop/tablet/mobile)
- [ ] API интеграция работает корректно
- [ ] Обработка ошибок реализована
- [ ] Toast уведомления при ошибках
- [ ] Unit тесты для компонента (coverage > 70%)
- [ ] TypeScript типы определены

### Dependencies
- AN-D1 (требуется UI спецификация)
- BE-D1 (требуется готовый API endpoint)
- FE-1 (базовая структура проекта)
- FE-2 (UI Kit компоненты: DataTable, StatusBadge)
- FE-3 (DeploymentService)
- FE-4 (AuthContext для проверки прав)

### Technical Notes

**Пример структуры компонента:**
```typescript
interface DeploymentsViewProps {
  data: Deployment[];
  productFilter: string;
  onSelectDeployment: (deployment: Deployment) => void;
}

function DeploymentsView({ data, productFilter, onSelectDeployment }: DeploymentsViewProps) {
  const [filters, setFilters] = useState({ product: 'all', status: 'all', search: '' });
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [ordering, setOrdering] = useState('-created_at');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch data with filters
  useEffect(() => {
    fetchDeployments();
  }, [filters, page, pageSize, ordering]);

  // Render table
  return (
    <Box sx={{ width: '100%' }}>
      {/* Filters */}
      {/* Table */}
      {/* Pagination */}
    </Box>
  );
}
```

**Debounce для поиска:**
```typescript
const debouncedSearch = useMemo(
  () => debounce((value: string) => {
    setFilters(prev => ({ ...prev, search: value }));
  }, 300),
  []
);
```

---

## Итоговая зависимость задач

```
AN-D1 (2 дня)
  ↓
BE-D1 (3 дня) ← зависит от BE-1, BE-4
  ↓
FE-D1 (3 дня) ← зависит от FE-1, FE-2, FE-3, FE-4
```

**Общая длительность (критический путь):** 8 дней

**Параллельная работа:**
- BE-D1 может начаться сразу после AN-D1
- FE-D1 может начаться только после готовности BE-D1 (нужен работающий API)

---

## ✅ Уточненные требования

1. **Фильтр по продукту:** Показывать ВСЕ продукты системы
2. **Поиск:** По названию И описанию (даже если столбец описания скрыт)
3. **Сортировка по умолчанию:** По дате создания (новые первые, -created_at)
4. **Пагинация:** Размер страницы по умолчанию 20
5. **Счетчики:** НЕТ счетчиков на этой странице
6. **Права доступа:** Методолог МОЖЕТ создавать внедрения

---

## BE-D-LC: Lifecycle управление для Deployment

**Тип:** Story
**Приоритет:** Высокий
**Оценка:** 2 дня

### Summary
Реализация автоматического расчета статуса внедрения и правил жизненного цикла (draft/active/deployed/archived)

### Description

Реализовать lifecycle управление для Deployment:

1. **Автоматический расчет статуса:**
   - draft: пустое внедрение ИЛИ все вложенные сущности в draft
   - active: хотя бы одна вложенная сущность не в draft
   - deployed: хотя бы одно Внедрение в deployed
   - archived: переведено вручную (нельзя, если есть deployed Изменения)

2. **Логика расчета статуса:**
   - При создании/обновлении Simulation → пересчет статуса Deployment
   - При создании/обновлении Pilot → пересчет статуса Deployment
   - При создании/обновлении Change → пересчет статуса Deployment
   - Кэширование статуса в поле deployment.status

3. **Правила архивирования:**
   - Нельзя архивировать Deployment с deployed Изменениями
   - При архивировании все вложенные сущности архивируются
   - Проверка прав доступа (только ПРМ и Админ)

4. **API endpoints:**
   - POST /api/deployments/{id}/archive/ - архивирование
   - GET /api/deployments/{id}/status/ - получение статуса с причиной
   - Автоматический пересчет при изменении вложенных сущностей

5. **Валидация переходов:**
   - draft → active: автоматически при создании вложенной сущности
   - active → deployed: автоматически при deployed Deployment
   - * → archived: вручную, только если нет deployed Changes
   - archived → *: нельзя (финальное состояние)

### Acceptance Criteria

- [ ] Автоматический расчет статуса реализован
- [ ] Статус пересчитывается при изменении вложенных сущностей
- [ ] Правило draft: пустое ИЛИ все вложенные в draft работает
- [ ] Правило active: хотя бы одна вложенная не в draft работает
- [ ] Правило deployed: хотя бы одно Deployment в deployed работает
- [ ] POST /api/deployments/{id}/archive/ реализован
- [ ] Валидация: нельзя архивировать с deployed Changes
- [ ] При архивировании все вложенные сущности архивируются
- [ ] GET /api/deployments/{id}/status/ возвращает статус с причиной
- [ ] Права доступа проверяются (ПРМ, Админ)
- [ ] HTTP 400 при попытке архивировать с deployed Changes
- [ ] HTTP 403 при отсутствии прав
- [ ] Unit тесты для всех правил (coverage > 80%)
- [ ] Integration тесты для пересчета статуса

### Dependencies
- BE-D1 (базовый CRUD для Deployment)
- BE-S1 (API симуляций)
- BE-P1 (API пилотов)
- BE-C1 (API изменений)

### Technical Notes

**Пример расчета статуса:**
```python
class Deployment(models.Model):
    # ... fields ...
    status = models.CharField(max_length=20)  # Кэшированный статус
    
    def calculate_status(self):
        """Рассчитать статус на основе вложенных сущностей"""
        # Если вручную архивировано
        if self.status == 'archived':
            return 'archived'
        
        # Получаем все вложенные сущности
        simulations = self.simulations.all()
        pilots = self.pilots.all()
        changes = self.changes.all()
        
        # Если пусто
        if not simulations and not pilots and not changes:
            return 'draft'
        
        # Если хотя бы одно Deployment в deployed
        if changes.filter(status='deployed').exists():
            return 'deployed'
        
        # Если все вложенные в draft
        all_draft = (
            all(s.status == 'draft' for s in simulations) and
            all(p.status == 'draft' for p in pilots) and
            all(c.status == 'draft' for c in changes)
        )
        
        if all_draft:
            return 'draft'
        
        # Иначе active
        return 'active'
    
    def save(self, *args, **kwargs):
        # Автоматический пересчет статуса (кроме archived)
        if self.status != 'archived':
            self.status = self.calculate_status()
        super().save(*args, **kwargs)
```

**Пример архивирования:**
```python
@api_view(['POST'])
def archive_deployment(request, deployment_id):
    deployment = get_object_or_404(Deployment, id=deployment_id)
    
    # Проверка прав
    if not (is_prm(request.user, deployment.product) or is_admin(request.user)):
        return Response({'error': 'Недостаточно прав'}, status=403)
    
    # Проверка: нельзя архивировать с deployed Changes
    if deployment.changes.filter(status='deployed').exists():
        return Response({
            'error': 'Нельзя архивировать внедрение с deployed изменениями'
        }, status=400)
    
    # Архивируем все вложенные сущности
    deployment.simulations.update(status='archived')
    deployment.pilots.update(status='archived')
    deployment.changes.update(status='archived')
    
    # Архивируем само внедрение
    deployment.status = 'archived'
    deployment.save()
    
    return Response({'status': 'archived'})
```

