#!/usr/bin/env python3
"""
Task Generator - Генерация задач разработки из спецификации
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime


class TaskGenerator:
    def __init__(self, spec_dir="spec"):
        self.spec_dir = Path(spec_dir)
        self.domain_model_file = self.spec_dir / "domain_model.md"

        # Известные сущности
        self.entities = [
            "Initiative", "Simulation", "Pilot", "Deployment",
            "Scorecard", "Package"
        ]

        # Оценки времени (в часах)
        self.estimates = {
            "model": 2,           # Django модель
            "serializer": 1,      # DRF сериализатор
            "viewset": 2,         # DRF viewset
            "permissions": 2,     # Права доступа
            "tests": 4,           # Тесты
            "frontend_list": 4,   # Список (таблица)
            "frontend_detail": 4, # Детальный просмотр
            "frontend_form": 6,   # Форма создания/редактирования
            "state_machine": 3,   # State machine логика
            "migrations": 1,      # Миграции БД
        }

    def generate_backend_tasks(self):
        """Генерация задач для backend разработки"""
        tasks = []

        for entity in self.entities:
            entity_lower = entity.lower()

            # Модель
            tasks.append({
                "id": f"backend-{entity_lower}-model",
                "title": f"Создать Django модель {entity}",
                "description": f"Реализовать модель {entity} согласно data_model.puml",
                "type": "backend",
                "entity": entity,
                "estimate_hours": self.estimates["model"],
                "dependencies": []
            })

            # Сериализатор
            tasks.append({
                "id": f"backend-{entity_lower}-serializer",
                "title": f"Создать сериализатор для {entity}",
                "description": f"Реализовать DRF сериализатор для {entity}",
                "type": "backend",
                "entity": entity,
                "estimate_hours": self.estimates["serializer"],
                "dependencies": [f"backend-{entity_lower}-model"]
            })

            # ViewSet
            tasks.append({
                "id": f"backend-{entity_lower}-viewset",
                "title": f"Создать ViewSet для {entity}",
                "description": f"Реализовать CRUD операции для {entity}",
                "type": "backend",
                "entity": entity,
                "estimate_hours": self.estimates["viewset"],
                "dependencies": [f"backend-{entity_lower}-serializer"]
            })

            # Права доступа
            tasks.append({
                "id": f"backend-{entity_lower}-permissions",
                "title": f"Реализовать права доступа для {entity}",
                "description": f"Реализовать ролевую модель согласно матрице прав",
                "type": "backend",
                "entity": entity,
                "estimate_hours": self.estimates["permissions"],
                "dependencies": [f"backend-{entity_lower}-viewset"]
            })

            # State machine (для сущностей с состояниями)
            if entity in ["Initiative", "Simulation", "Pilot", "Deployment", "Package"]:
                tasks.append({
                    "id": f"backend-{entity_lower}-state-machine",
                    "title": f"Реализовать state machine для {entity}",
                    "description": f"Реализовать переходы состояний согласно state_machine.puml",
                    "type": "backend",
                    "entity": entity,
                    "estimate_hours": self.estimates["state_machine"],
                    "dependencies": [f"backend-{entity_lower}-model"]
                })

            # Тесты
            tasks.append({
                "id": f"backend-{entity_lower}-tests",
                "title": f"Написать тесты для {entity}",
                "description": f"Unit и integration тесты для {entity}",
                "type": "backend",
                "entity": entity,
                "estimate_hours": self.estimates["tests"],
                "dependencies": [
                    f"backend-{entity_lower}-viewset",
                    f"backend-{entity_lower}-permissions"
                ]
            })

        return tasks

    def generate_frontend_tasks(self):
        """Генерация задач для frontend разработки"""
        tasks = []

        for entity in self.entities:
            entity_lower = entity.lower()

            # Список (таблица)
            tasks.append({
                "id": f"frontend-{entity_lower}-list",
                "title": f"Создать список {entity}",
                "description": f"Реализовать таблицу с фильтрацией и сортировкой",
                "type": "frontend",
                "entity": entity,
                "estimate_hours": self.estimates["frontend_list"],
                "dependencies": []
            })

            # Детальный просмотр
            tasks.append({
                "id": f"frontend-{entity_lower}-detail",
                "title": f"Создать детальный просмотр {entity}",
                "description": f"Реализовать страницу с полной информацией о {entity}",
                "type": "frontend",
                "entity": entity,
                "estimate_hours": self.estimates["frontend_detail"],
                "dependencies": [f"frontend-{entity_lower}-list"]
            })

            # Форма создания/редактирования
            tasks.append({
                "id": f"frontend-{entity_lower}-form",
                "title": f"Создать форму для {entity}",
                "description": f"Реализовать форму создания и редактирования {entity}",
                "type": "frontend",
                "entity": entity,
                "estimate_hours": self.estimates["frontend_form"],
                "dependencies": [f"frontend-{entity_lower}-detail"]
            })

        return tasks

    def generate_infrastructure_tasks(self):
        """Генерация задач для инфраструктуры"""
        tasks = [
            {
                "id": "infra-setup-django",
                "title": "Настроить Django проект",
                "description": "Создать Django проект с базовой конфигурацией",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 4,
                "dependencies": []
            },
            {
                "id": "infra-setup-drf",
                "title": "Настроить Django REST Framework",
                "description": "Настроить DRF, аутентификацию, CORS",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 3,
                "dependencies": ["infra-setup-django"]
            },
            {
                "id": "infra-setup-postgres",
                "title": "Настроить PostgreSQL",
                "description": "Настроить БД, создать пользователя, схему",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 2,
                "dependencies": ["infra-setup-django"]
            },
            {
                "id": "infra-setup-react",
                "title": "Настроить React проект",
                "description": "Создать React + TypeScript проект с Material-UI",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 4,
                "dependencies": []
            },
            {
                "id": "infra-setup-ci",
                "title": "Настроить CI/CD",
                "description": "Настроить GitHub Actions для тестов и деплоя",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 6,
                "dependencies": ["infra-setup-django", "infra-setup-react"]
            },
            {
                "id": "infra-setup-docker",
                "title": "Создать Docker конфигурацию",
                "description": "Dockerfile и docker-compose для разработки",
                "type": "infrastructure",
                "entity": None,
                "estimate_hours": 4,
                "dependencies": ["infra-setup-django", "infra-setup-postgres"]
            }
        ]

        return tasks

    def calculate_estimates(self, tasks):
        """Расчёт общих оценок"""
        by_type = {}
        total = 0

        for task in tasks:
            task_type = task["type"]
            hours = task["estimate_hours"]

            if task_type not in by_type:
                by_type[task_type] = 0

            by_type[task_type] += hours
            total += hours

        return {
            "by_type": by_type,
            "total_hours": total,
            "total_weeks": round(total / 40, 1),  # 40 часов в неделю
            "total_sprints": round(total / 80, 1)  # 2-недельные спринты
        }

    def generate_all_tasks(self, output_format="json"):
        """Генерация всех задач"""
        print("=== Генерация задач разработки ===\n")

        # Генерация задач
        infra_tasks = self.generate_infrastructure_tasks()
        backend_tasks = self.generate_backend_tasks()
        frontend_tasks = self.generate_frontend_tasks()

        all_tasks = infra_tasks + backend_tasks + frontend_tasks

        # Расчёт оценок
        estimates = self.calculate_estimates(all_tasks)

        # Вывод статистики
        print(f"✓ Сгенерировано задач: {len(all_tasks)}")
        print(f"  - Инфраструктура: {len(infra_tasks)}")
        print(f"  - Backend: {len(backend_tasks)}")
        print(f"  - Frontend: {len(frontend_tasks)}")
        print()
        print("Оценка времени:")
        for task_type, hours in estimates["by_type"].items():
            print(f"  - {task_type}: {hours} часов")
        print()
        print(f"Итого: {estimates['total_hours']} часов")
        print(f"       {estimates['total_weeks']} недель")
        print(f"       {estimates['total_sprints']} спринтов (2 недели)")

        # Сохранение результата
        result = {
            "generated_at": datetime.now().isoformat(),
            "tasks": all_tasks,
            "estimates": estimates
        }

        if output_format == "json":
            output_file = Path("planning/generated_tasks.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"\n✓ Задачи сохранены в {output_file}")

        elif output_format == "markdown":
            output_file = Path("planning/generated_tasks.md")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# Задачи разработки\n\n")
                f.write(f"**Сгенерировано:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write("---\n\n")

                # Инфраструктура
                f.write("## Инфраструктура\n\n")
                for task in infra_tasks:
                    f.write(f"### {task['title']}\n\n")
                    f.write(f"**ID:** `{task['id']}`\n\n")
                    f.write(f"**Описание:** {task['description']}\n\n")
                    f.write(f"**Оценка:** {task['estimate_hours']} часов\n\n")
                    if task['dependencies']:
                        f.write(f"**Зависимости:** {', '.join(task['dependencies'])}\n\n")
                    f.write("---\n\n")

                # Backend
                f.write("## Backend\n\n")
                for entity in self.entities:
                    entity_tasks = [t for t in backend_tasks if t['entity'] == entity]
                    if entity_tasks:
                        f.write(f"### {entity}\n\n")
                        for task in entity_tasks:
                            f.write(f"- **{task['title']}** ({task['estimate_hours']}ч)\n")
                            f.write(f"  - {task['description']}\n")
                        f.write("\n")

                # Frontend
                f.write("## Frontend\n\n")
                for entity in self.entities:
                    entity_tasks = [t for t in frontend_tasks if t['entity'] == entity]
                    if entity_tasks:
                        f.write(f"### {entity}\n\n")
                        for task in entity_tasks:
                            f.write(f"- **{task['title']}** ({task['estimate_hours']}ч)\n")
                            f.write(f"  - {task['description']}\n")
                        f.write("\n")

                # Оценки
                f.write("## Оценка времени\n\n")
                for task_type, hours in estimates["by_type"].items():
                    f.write(f"- **{task_type}:** {hours} часов\n")
                f.write(f"\n**Итого:** {estimates['total_hours']} часов ({estimates['total_weeks']} недель, {estimates['total_sprints']} спринтов)\n")

            print(f"\n✓ Задачи сохранены в {output_file}")

        return result


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python3 task_generator.py generate [json|markdown]")
        print("  python3 task_generator.py estimate")
        sys.exit(1)

    generator = TaskGenerator()
    command = sys.argv[1]

    if command == "generate":
        output_format = sys.argv[2] if len(sys.argv) > 2 else "json"
        generator.generate_all_tasks(output_format)

    elif command == "estimate":
        # Только оценка без сохранения
        infra_tasks = generator.generate_infrastructure_tasks()
        backend_tasks = generator.generate_backend_tasks()
        frontend_tasks = generator.generate_frontend_tasks()
        all_tasks = infra_tasks + backend_tasks + frontend_tasks
        estimates = generator.calculate_estimates(all_tasks)

        print("=== Оценка времени разработки ===\n")
        print(f"Всего задач: {len(all_tasks)}")
        print(f"  - Инфраструктура: {len(infra_tasks)}")
        print(f"  - Backend: {len(backend_tasks)}")
        print(f"  - Frontend: {len(frontend_tasks)}")
        print()
        for task_type, hours in estimates["by_type"].items():
            print(f"{task_type}: {hours} часов")
        print()
        print(f"Итого: {estimates['total_hours']} часов")
        print(f"       {estimates['total_weeks']} недель")
        print(f"       {estimates['total_sprints']} спринтов")

    else:
        print(f"✗ Неизвестная команда: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
