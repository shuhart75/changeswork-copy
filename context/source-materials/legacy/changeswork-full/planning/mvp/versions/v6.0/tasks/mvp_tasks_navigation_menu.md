# Задача для навигационного меню (Navigation Menu)

## Обзор задачи

**Компонент:** Левое боковое меню (Navigation Sidebar)
**Расположение:** Левая часть экрана, фиксированное
**Статус:** Доработка существующего компонента

### Что показывает меню (из макета):

**Структура меню:**
- Логотип/название системы (вверху)
- Список разделов:
  - Внедрения (Deployments)
  - Симуляции (Simulations)
  - Пилоты (Pilots)
  - Изменения (Changes)
  - Скоркарты (Scorecards)
  - Пакеты (Packages) - если будет реализовано
  - Согласования (Approvals) - если будет реализовано
- Профиль пользователя (внизу)
- Кнопка сворачивания/разворачивания меню

**Функционал:**
- Активный пункт меню выделяется цветом
- Клик на пункт → переход к соответствующей странице
- Сворачивание меню (показывать только иконки)
- Счетчики (опционально) - количество элементов в разделе
- Иконки для каждого раздела

**Права доступа:**
- ПРМ видит все разделы (но с ограничениями по продукту внутри)
- Методолог видит все разделы
- Согласующий видит только "Согласования"
- Админ видит все разделы

---

## FE-NAV1: Доработка навигационного меню

**Тип:** Story
**Приоритет:** Средний
**Оценка:** 2 дня

### Summary
Доработка левого навигационного меню с добавлением всех разделов MVP и адаптацией под роли пользователей

### Description

Доработать компонент навигационного меню:

1. **Структура меню:**
   - Логотип/название системы (вверху)
   - Список разделов с иконками:
     - Внедрения (icon: rocket_launch)
     - Симуляции (icon: science)
     - Пилоты (icon: flight_takeoff)
     - Изменения (icon: change_circle)
     - Скоркарты (icon: description)
     - Пакеты (icon: inventory_2) - опционально
     - Согласования (icon: approval) - опционально
   - Профиль пользователя (внизу)
   - Кнопка сворачивания/разворачивания

2. **Активный пункт меню:**
   - Выделение цветом (primary color)
   - Индикатор слева (вертикальная полоска)
   - Изменение цвета иконки и текста

3. **Сворачивание меню:**
   - Кнопка с иконкой menu/menu_open
   - При сворачивании показывать только иконки
   - Tooltip при наведении на иконку (показывать название раздела)
   - Сохранение состояния в localStorage

4. **Счетчики (опционально):**
   - Показывать количество элементов в разделе
   - Обновление счетчиков при изменении данных
   - Стиль: маленький бейдж справа от названия

5. **Права доступа:**
   - ПРМ: все разделы видны
   - Методолог: все разделы видны
   - Согласующий: только "Согласования"
   - Админ: все разделы видны
   - Скрывать недоступные разделы (не показывать disabled)

6. **Профиль пользователя:**
   - Аватар (или инициалы)
   - Имя пользователя
   - Роль (ПРМ, Методолог, Согласующий, Админ)
   - Dropdown меню:
     - Настройки
     - Выход

7. **Responsive дизайн:**
   - Desktop: фиксированное меню слева (ширина 240px)
   - Tablet: сворачиваемое меню (overlay)
   - Mobile: hamburger menu (drawer)

8. **Навигация:**
   - React Router для переходов между страницами
   - Сохранение состояния при переходах
   - Breadcrumbs синхронизированы с активным пунктом меню

### Acceptance Criteria

- [ ] Компонент NavigationMenu реализован
- [ ] Все разделы MVP добавлены с иконками
- [ ] Активный пункт меню выделяется корректно
- [ ] Сворачивание/разворачивание меню работает
- [ ] Состояние сворачивания сохраняется в localStorage
- [ ] Tooltip показывается при наведении на свернутое меню
- [ ] Счетчики отображаются (если реализовано)
- [ ] Права доступа работают (разделы скрываются для ролей)
- [ ] Профиль пользователя отображается внизу
- [ ] Dropdown меню профиля работает
- [ ] Responsive дизайн работает (desktop/tablet/mobile)
- [ ] Навигация через React Router работает
- [ ] Breadcrumbs синхронизированы с меню
- [ ] Unit тесты для компонента (coverage > 70%)
- [ ] TypeScript типы определены

### Dependencies
- FE-1 (базовая структура проекта)
- FE-4 (AuthContext для проверки прав)
- Все страницы MVP должны быть реализованы

### Technical Notes

**Пример структуры компонента:**
```typescript
interface NavigationMenuItem {
  id: string;
  label: string;
  icon: string;
  path: string;
  roles: string[]; // Роли, которым доступен раздел
  count?: number; // Опциональный счетчик
}

const menuItems: NavigationMenuItem[] = [
  { id: 'deployments', label: 'Внедрения', icon: 'rocket_launch', path: '/deployments', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'simulations', label: 'Симуляции', icon: 'science', path: '/simulations', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'pilots', label: 'Пилоты', icon: 'flight_takeoff', path: '/pilots', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'changes', label: 'Изменения', icon: 'change_circle', path: '/changes', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'scorecards', label: 'Скоркарты', icon: 'description', path: '/scorecards', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'packages', label: 'Пакеты', icon: 'inventory_2', path: '/packages', roles: ['prm', 'methodologist', 'admin'] },
  { id: 'approvals', label: 'Согласования', icon: 'approval', path: '/approvals', roles: ['prm', 'methodologist', 'approver', 'admin'] }
];

function NavigationMenu() {
  const [collapsed, setCollapsed] = useState(() => {
    return localStorage.getItem('menuCollapsed') === 'true';
  });
  const { currentUser } = useAuth();
  const location = useLocation();

  const toggleCollapsed = () => {
    const newState = !collapsed;
    setCollapsed(newState);
    localStorage.setItem('menuCollapsed', String(newState));
  };

  const isActive = (path: string) => {
    return location.pathname.startsWith(path);
  };

  const hasAccess = (item: NavigationMenuItem) => {
    return item.roles.includes(currentUser.role);
  };

  const filteredItems = menuItems.filter(hasAccess);

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: collapsed ? 64 : 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: collapsed ? 64 : 240,
          boxSizing: 'border-box',
          transition: 'width 0.3s'
        }
      }}
    >
      {/* Logo */}
      <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
        <img src="/logo.svg" alt="Logo" width={32} height={32} />
        {!collapsed && <Typography variant="h6">Risk Strategy</Typography>}
      </Box>

      {/* Menu Items */}
      <List sx={{ flex: 1 }}>
        {filteredItems.map(item => (
          <Tooltip key={item.id} title={collapsed ? item.label : ''} placement="right">
            <ListItem
              button
              component={Link}
              to={item.path}
              selected={isActive(item.path)}
              sx={{
                borderLeft: isActive(item.path) ? '4px solid' : 'none',
                borderColor: 'primary.main',
                bgcolor: isActive(item.path) ? 'action.selected' : 'transparent'
              }}
            >
              <ListItemIcon>
                <span className="material-icons" style={{ color: isActive(item.path) ? 'primary' : 'inherit' }}>
                  {item.icon}
                </span>
              </ListItemIcon>
              {!collapsed && (
                <>
                  <ListItemText primary={item.label} />
                  {item.count && (
                    <Chip label={item.count} size="small" color="primary" />
                  )}
                </>
              )}
            </ListItem>
          </Tooltip>
        ))}
      </List>

      {/* User Profile */}
      <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Avatar sx={{ width: 32, height: 32 }}>
            {currentUser.full_name.charAt(0)}
          </Avatar>
          {!collapsed && (
            <Box sx={{ flex: 1 }}>
              <Typography variant="body2" fontWeight={500}>
                {currentUser.full_name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {getRoleLabel(currentUser.role)}
              </Typography>
            </Box>
          )}
        </Box>
      </Box>

      {/* Collapse Button */}
      <IconButton onClick={toggleCollapsed} sx={{ m: 1 }}>
        <span className="material-icons">
          {collapsed ? 'menu_open' : 'menu'}
        </span>
      </IconButton>
    </Drawer>
  );
}
```

**Responsive для mobile:**
```typescript
function NavigationMenuMobile() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <IconButton onClick={() => setOpen(true)}>
        <MenuIcon />
      </IconButton>
      <Drawer
        anchor="left"
        open={open}
        onClose={() => setOpen(false)}
      >
        {/* Same menu content */}
      </Drawer>
    </>
  );
}
```

---

## ✅ Ключевые особенности

1. **Доработка существующего компонента** - не новая разработка
2. **Все разделы MVP** - 5-7 пунктов меню
3. **Сворачивание меню** - с сохранением состояния в localStorage
4. **Права доступа** - скрывать недоступные разделы
5. **Активный пункт** - визуальное выделение
6. **Профиль пользователя** - внизу меню
7. **Responsive дизайн** - drawer на mobile
8. **Иконки Material Icons** - для каждого раздела
9. **Счетчики** - опционально, количество элементов
10. **React Router** - навигация между страницами

**Оценка:** 2 дня (только Frontend)

**Примечание:** Эта задача выполняется в конце, после реализации всех страниц MVP.

---
