#!/bin/bash

# Скрипт реорганизации структуры проекта

echo "=== Реорганизация структуры проекта ==="
echo

# 1. Переместить актуальную спецификацию
echo "1. Перемещение актуальной спецификации..."
cp domain_model_v3.1.md spec/domain_model.md
cp changes_data_model_v3.1.puml spec/data_model.puml
cp changes_state_machine_v3.1.puml spec/state_machine.puml
cp CLAUDE.md spec/GUIDE.md

# 2. Архивировать старые версии
echo "2. Архивирование старых версий..."
mv domain_model_v3.0.md spec/versions/v3.0/ 2>/dev/null
mv changes_data_model_v3.0.puml spec/versions/v3.0/ 2>/dev/null
mv changes_state_machine_v3.0.puml spec/versions/v3.0/ 2>/dev/null

mv domain_model_v3.1.md spec/versions/v3.1/ 2>/dev/null
mv changes_data_model_v3.1.puml spec/versions/v3.1/ 2>/dev/null
mv changes_state_machine_v3.1.puml spec/versions/v3.1/ 2>/dev/null
mv CLAUDE_v3.1.md spec/versions/v3.1/ 2>/dev/null

# 3. Переместить прототипы
echo "3. Перемещение прототипов..."
cp risk_strategy_ui_v3_table.html prototypes/current.html
mv risk_strategy_ui_mvp.html prototypes/archive/ 2>/dev/null
mv mvp_tasks_review*.html prototypes/archive/ 2>/dev/null

# 4. Переместить документацию
echo "4. Перемещение документации..."
mv executive_summary.md docs/ 2>/dev/null
mv presentation_stakeholders*.md docs/ 2>/dev/null
mv faq_stakeholders.md docs/ 2>/dev/null
mv glossary.md docs/ 2>/dev/null
mv use_cases.md docs/ 2>/dev/null
mv README_presentation.md docs/ 2>/dev/null

# 5. Переместить планирование
echo "5. Перемещение планирования..."
mv mvp_tasks_*.md planning/mvp/tasks/ 2>/dev/null
mv mvp_gantt*.puml planning/mvp/gantt/ 2>/dev/null
mv mvp_*.md planning/mvp/ 2>/dev/null
mv README_MVP.md planning/mvp/ 2>/dev/null

# 6. Переместить заметки
echo "6. Перемещение заметок..."
mv TODO.md notes/ 2>/dev/null
mv DECISION_POINT.md notes/ 2>/dev/null
mv agent_optimization_proposal.md notes/ 2>/dev/null

# 7. Переместить скрипты
echo "7. Перемещение скриптов..."
mv verify_dependencies*.py scripts/ 2>/dev/null
mv check_overlaps*.py scripts/ 2>/dev/null

echo
echo "=== Реорганизация завершена ==="
echo
echo "Новая структура:"
echo "  spec/           - Актуальная спецификация"
echo "  prototypes/     - HTML прототипы"
echo "  docs/           - Документация"
echo "  planning/       - Планирование"
echo "  notes/          - Рабочие заметки"
echo "  scripts/        - Утилиты"
