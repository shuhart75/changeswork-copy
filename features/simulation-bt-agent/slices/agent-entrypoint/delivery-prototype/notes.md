# Delivery Prototype Notes

Срез: `agent-entrypoint`  
Дата обновления: `2026-04-27`

Покрытие прототипа:
- глобальная точка входа в окно агента со списка, деталки, вкладки деталки, формы редактирования и неподходящей симуляции;
- правая неблокирующая панель как единый container для всех контекстов открытия;
- единый вызов `POST /dialog/session` только с `session_id`;
- зависимость действия `Сформировать БТ` от контекста текущей страницы.

Что важно для handoff:
- панель открывается справа и не блокирует основной интерфейс;
- при повторном открытии используется тот же `session_id`;
- дата и время старта диалога показаны как состояние пользовательской сессии АС КОДА, но не отправляются при открытии окна.
- одна и та же кнопка вызова панели называется `AI-агент RAIN` на всех экранах;
- в макете отдельно показаны list/detail/results/edit и неподходящий detail-context, чтобы фронт не размазывал логику открытия по разным реализациям;
- визуальная оболочка прототипа повторяет текущий раздел симуляций: тёмный левый сайдбар, светлый top bar, pale-карточки и акцентные синий/зелёный цвета;
- в качестве базы взяты `context/source-materials/current-system/prototypes/raw/prototype.html` и скриншоты из `context/source-materials/current-system/screenshots/`.

Источники:
- `../requirements/frontend.md`
- `../requirements/backend.md`
- `../../../requirements.md`
- `../../../../../context/source-materials/current-system/prototypes/raw/prototype.html`
- `../../../../../context/source-materials/current-system/screenshots/`
- `/home/reutov/Documents/AI/simulations_AI_agent/prototype/simulation-agent-mock.html`
