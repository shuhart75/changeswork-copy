# Gantt Rules Override

- Заголовок gantt генерируется скриптом, руками правим только include/preamble файлы и \`closed-days.txt\`.
- Праздники и нерабочие дни квартала хранятся в \`planning/<quarter>/gantt/closed-days.txt\`.
- Общие служебные блоки перед feature lanes кладём в \`planning/<quarter>/gantt/preamble/common.puml\`.
- View-специфичные блоки можно класть в \`planning/<quarter>/gantt/preamble/quarter-plan.puml\`, \`commander-plan.puml\`, \`actual-progress.puml\`.
- Feature lanes на общем gantt должны идти отдельными секциями \`-- Название фичи --\`.
- Actual-progress include-файлы генерируются из \`planning/actualization.md\` и \`slices/*/execution/tasks.md\`.
- Не начатые execution tasks (\`Progress % = 0\`, нет actual dates) не рисуются в прошлом: при каждой генерации генератор сдвигает их на today/следующий рабочий день только в PlantUML.
- Внутри feature не начатый frontend стартует не раньше чем через 3 рабочих дня после старта не начатого backend/API.
- Resource lanes канонические: \`A<N>\`, \`B<N>\`, \`F<N>\`, \`Q<N>\`; неизвестный ресурс с известной ролью — \`TBD_A\`, \`TBD_B\`, \`TBD_F\`, \`TBD_Q\`.
- Состав команды и допустимые lanes лежат в \`.workflow/team.md\`.
- Не начатые задачи раскладываются без перегруза ресурса выше 100% в один рабочий день; пустой/\`TBD_*\`/неростерный executor назначается автоматически по роли или префиксу задачи.
