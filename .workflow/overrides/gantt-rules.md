# Gantt Rules Override

- Заголовок gantt генерируется скриптом, руками правим только include/preamble файлы и \`closed-days.txt\`.
- Праздники и нерабочие дни квартала хранятся в \`planning/<quarter>/gantt/closed-days.txt\`.
- Общие служебные блоки перед feature lanes кладём в \`planning/<quarter>/gantt/preamble/common.puml\`.
- View-специфичные блоки можно класть в \`planning/<quarter>/gantt/preamble/quarter-plan.puml\`, \`commander-plan.puml\`, \`actual-progress.puml\`.
- Feature lanes на общем gantt должны идти отдельными секциями \`-- Название фичи --\`.
- Actual-progress include-файлы генерируются из \`planning/actualization.md\` и \`slices/*/execution/tasks.md\`.
