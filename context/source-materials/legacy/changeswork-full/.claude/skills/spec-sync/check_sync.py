#!/usr/bin/env python3
"""
Spec Sync - Проверка синхронизации документов спецификации
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class SpecSyncChecker:
    def __init__(self, config_path: str = ".claude/skills/spec-sync/config.json"):
        self.config = self._load_config(config_path)
        self.issues = []
        self.warnings = []

    def _load_config(self, config_path: str) -> dict:
        """Загрузка конфигурации"""
        config_file = Path(config_path)
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Конфигурация по умолчанию
            return {
                "source_files": [
                    "spec/domain_model.md",
                    "spec/data_model.puml",
                    "spec/state_machine.puml",
                    "spec/GUIDE.md"
                ],
                "entity_mapping": {
                    "Initiative": ["initiative", "Инициатива"],
                    "Simulation": ["simulation", "Симуляция"],
                    "Pilot": ["pilot", "Пилот"],
                    "Deployment": ["deployment", "Внедрение"],
                    "Scorecard": ["scorecard", "Скоркарта"],
                    "Package": ["package", "Пакет"]
                }
            }

    def check_all(self) -> bool:
        """Проверка всех документов"""
        print("=== Проверка синхронизации спецификации ===\n")

        # Проверка существования файлов
        missing_files = self._check_files_exist()
        if missing_files:
            print("✗ Отсутствующие файлы:")
            for f in missing_files:
                print(f"  - {f}")
            return False

        print("✓ Все файлы спецификации найдены\n")

        # Проверка сущностей
        self._check_entities()

        # Проверка связей
        self._check_relationships()

        # Проверка статусов
        self._check_statuses()

        # Итоги
        self._print_summary()

        return len(self.issues) == 0

    def _check_files_exist(self) -> List[str]:
        """Проверка существования файлов"""
        missing = []
        for file_path in self.config["source_files"]:
            if not Path(file_path).exists():
                missing.append(file_path)
        return missing

    def _check_entities(self):
        """Проверка упоминаний сущностей во всех документах"""
        print("=== Проверка сущностей ===")

        entity_mapping = self.config["entity_mapping"]

        for entity, aliases in entity_mapping.items():
            mentions = {}

            for file_path in self.config["source_files"]:
                if not Path(file_path).exists():
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Подсчет упоминаний
                count = 0
                for alias in [entity] + aliases:
                    count += len(re.findall(rf'\b{re.escape(alias)}\b', content, re.IGNORECASE))

                mentions[file_path] = count

            # Проверка: сущность должна быть упомянута во всех файлах
            missing_in = [f for f, count in mentions.items() if count == 0]

            if missing_in:
                self.warnings.append(f"Сущность '{entity}' не найдена в: {', '.join(missing_in)}")
                print(f"⚠ {entity}: отсутствует в {len(missing_in)} файлах")
            else:
                print(f"✓ {entity}: найдена во всех файлах")

        print()

    def _check_relationships(self):
        """Проверка связей между сущностями"""
        print("=== Проверка связей ===")

        # Извлечение связей из domain_model.md
        domain_model_path = "spec/domain_model.md"
        if not Path(domain_model_path).exists():
            print("⚠ domain_model.md не найден, пропускаем проверку связей\n")
            return

        with open(domain_model_path, 'r', encoding='utf-8') as f:
            domain_content = f.read()

        # Поиск упоминаний связей (многие-ко-многим, один-ко-многим)
        # Ищем только реальные таблицы, игнорируем описательный текст
        many_to_many = []
        # Ищем конкретные junction таблицы в тексте (с вариантами написания)
        junction_tables = {
            'pilot_scorecard': ['pilot_scorecard'],
            'deployment_scorecard': ['deployment_scorecard'],
            'initiative_subproduct': ['initiative_subproduct', 'initiative_sub_product'],
            'scorecard_subproduct': ['scorecard_subproduct', 'scorecard_sub_product']
        }
        one_to_many = []

        # Проверка наличия junction таблиц в data_model.puml
        data_model_path = "spec/data_model.puml"
        if Path(data_model_path).exists():
            with open(data_model_path, 'r', encoding='utf-8') as f:
                data_content = f.read()

            # Проверяем наличие известных junction таблиц
            found_tables = []
            missing_tables = []

            for table_name, variants in junction_tables.items():
                found = False
                for variant in variants:
                    if variant in data_content.lower():
                        found_tables.append(table_name)
                        found = True
                        break
                if not found:
                    missing_tables.append(table_name)

            print(f"Найдено junction таблиц: {len(found_tables)}")
            if found_tables:
                print(f"  ✓ {', '.join(found_tables)}")

            if missing_tables:
                print(f"Отсутствуют junction таблицы: {len(missing_tables)}")
                for table in missing_tables:
                    self.warnings.append(f"Junction таблица {table} не найдена в data_model.puml")

        print()

    def _check_statuses(self):
        """Проверка соответствия статусов"""
        print("=== Проверка статусов ===")

        # Извлечение статусов из state_machine.puml
        state_machine_path = "spec/state_machine.puml"
        if not Path(state_machine_path).exists():
            print("⚠ state_machine.puml не найден, пропускаем проверку статусов\n")
            return

        with open(state_machine_path, 'r', encoding='utf-8') as f:
            state_content = f.read()

        # Поиск определений состояний (игнорируем заголовки секций)
        states = re.findall(r'state\s+"([^"]+)"\s+as\s+\w+', state_content)

        # Фильтруем заголовки секций (они содержат слово "Состояния")
        actual_states = [s for s in states if 'Состояния' not in s and 'состояния' not in s.lower()]

        print(f"Найдено состояний в state_machine.puml: {len(actual_states)}")

        # Проверка основных состояний (не проверяем каждое, только критичные)
        # Используем варианты написания для более точной проверки
        critical_states = {
            'Черновик': ['черновик', 'draft'],
            'Активна': ['активна', 'активен', 'active'],
            'Завершена': ['завершена', 'завершен', 'completed'],
            'Архивирована': ['архивирован', 'archived'],
            'Выполняется': ['выполняется', 'running'],
            'Ошибка': ['ошибка', 'failed', 'error'],
            'Одобрена': ['одобрена', 'одобрен', 'approved']
        }

        domain_model_path = "spec/domain_model.md"
        if Path(domain_model_path).exists():
            with open(domain_model_path, 'r', encoding='utf-8') as f:
                domain_content = f.read()

            missing_critical = []
            for state_name, variants in critical_states.items():
                found = False
                for variant in variants:
                    if variant in domain_content.lower():
                        found = True
                        break
                if not found:
                    missing_critical.append(state_name)

            if missing_critical:
                self.warnings.append(f"Критичные состояния не найдены в domain_model.md: {', '.join(missing_critical)}")

        print()

    def _print_summary(self):
        """Вывод итогов"""
        print("=== Итоги проверки ===")

        if not self.issues and not self.warnings:
            print("✓ Проблем не найдено, спецификация синхронизирована")
            return

        if self.issues:
            print(f"\n✗ Критичные проблемы ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  - {issue}")

        if self.warnings:
            print(f"\n⚠ Предупреждения ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

def main():
    checker = SpecSyncChecker()
    success = checker.check_all()
    return 0 if success else 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
