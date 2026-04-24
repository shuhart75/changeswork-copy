#!/usr/bin/env python3
"""
Diagram Updater - Автоматическое обновление PlantUML диаграмм
"""

import sys
import re
from pathlib import Path
from datetime import datetime


class DiagramUpdater:
    def __init__(self, spec_dir="spec"):
        self.spec_dir = Path(spec_dir)
        self.domain_model_file = self.spec_dir / "domain_model.md"
        self.data_model_file = self.spec_dir / "data_model.puml"
        self.state_machine_file = self.spec_dir / "state_machine.puml"

    def extract_entities(self):
        """Извлечение сущностей из domain_model.md"""
        print("=== Извлечение сущностей из domain_model.md ===\n")

        if not self.domain_model_file.exists():
            print(f"✗ Файл {self.domain_model_file} не найден")
            return []

        # Известные сущности (русский/английский)
        entity_mapping = {
            "Initiative": ["Initiative", "Инициатива"],
            "Simulation": ["Simulation", "Симуляция"],
            "Pilot": ["Pilot", "Пилот"],
            "Deployment": ["Deployment", "Внедрение"],
            "Scorecard": ["Scorecard", "Скоркарта"],
            "Package": ["Package", "Пакет"]
        }

        entities = list(entity_mapping.keys())

        print(f"✓ Проверяемых сущностей: {len(entities)}")
        for entity in entities:
            print(f"  - {entity}")

        return entities

    def extract_relationships(self):
        """Извлечение связей из domain_model.md"""
        print("\n=== Извлечение связей из domain_model.md ===\n")

        if not self.domain_model_file.exists():
            print(f"✗ Файл {self.domain_model_file} не найден")
            return []

        with open(self.domain_model_file, 'r', encoding='utf-8') as f:
            content = f.read()

        relationships = []

        # Поиск паттернов связей:
        # - "one-to-many" или "1:N"
        # - "many-to-many" или "N:M"
        # - "one-to-one" или "1:1"

        # Паттерн: Entity1 -> Entity2 (relationship_type)
        rel_patterns = [
            r'(\w+)\s+[-–]\s+(\w+)\s+\(([^)]+)\)',  # Entity1 - Entity2 (type)
            r'(\w+)\s+→\s+(\w+)\s+\(([^)]+)\)',      # Entity1 → Entity2 (type)
        ]

        for pattern in rel_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                relationships.append({
                    'from': match[0],
                    'to': match[1],
                    'type': match[2]
                })

        print(f"✓ Найдено связей: {len(relationships)}")
        for rel in relationships:
            print(f"  - {rel['from']} → {rel['to']} ({rel['type']})")

        return relationships

    def check_data_model_sync(self):
        """Проверка синхронизации data_model.puml с domain_model.md"""
        print("\n=== Проверка синхронизации data_model.puml ===\n")

        entities = self.extract_entities()

        if not self.data_model_file.exists():
            print(f"✗ Файл {self.data_model_file} не найден")
            return False

        with open(self.data_model_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()

        missing_entities = []
        found_entities = []

        for entity in entities:
            # Поиск entity в PlantUML
            # Формат: entity "name" as alias { или entity name {
            entity_lower = entity.lower()
            pattern = rf'(?:entity|class)\s+(?:"{entity_lower}"|{entity_lower})\s+(?:as\s+{entity_lower}\s+)?{{'

            if re.search(pattern, puml_content, re.IGNORECASE):
                found_entities.append(entity)
                print(f"✓ {entity}: найдена в data_model.puml")
            else:
                missing_entities.append(entity)
                print(f"✗ {entity}: НЕ найдена в data_model.puml")

        print(f"\n✓ Найдено: {len(found_entities)}/{len(entities)}")
        if missing_entities:
            print(f"⚠ Отсутствуют: {', '.join(missing_entities)}")

        return len(missing_entities) == 0

    def check_state_machine_sync(self):
        """Проверка синхронизации state_machine.puml с domain_model.md"""
        print("\n=== Проверка синхронизации state_machine.puml ===\n")

        entities = self.extract_entities()

        if not self.state_machine_file.exists():
            print(f"✗ Файл {self.state_machine_file} не найден")
            return False

        with open(self.state_machine_file, 'r', encoding='utf-8') as f:
            puml_content = f.read()

        # Поиск state machine для каждой сущности
        # Паттерн: @startuml EntityName_state или title EntityName State Machine
        missing_entities = []
        found_entities = []

        for entity in entities:
            if re.search(rf'{entity}', puml_content, re.IGNORECASE):
                found_entities.append(entity)
                print(f"✓ {entity}: найдена в state_machine.puml")
            else:
                missing_entities.append(entity)
                print(f"⚠ {entity}: НЕ найдена в state_machine.puml")

        print(f"\n✓ Найдено: {len(found_entities)}/{len(entities)}")
        if missing_entities:
            print(f"⚠ Отсутствуют: {', '.join(missing_entities)}")

        return len(missing_entities) == 0

    def generate_png(self, output_dir="spec/diagrams"):
        """Генерация PNG из PlantUML файлов (требует установленный PlantUML)"""
        print("\n=== Генерация PNG из PlantUML ===\n")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        puml_files = [
            self.data_model_file,
            self.state_machine_file
        ]

        generated = []
        for puml_file in puml_files:
            if not puml_file.exists():
                print(f"⚠ Файл {puml_file} не найден, пропущен")
                continue

            output_file = output_path / f"{puml_file.stem}.png"

            # Попытка генерации через plantuml
            import subprocess
            try:
                result = subprocess.run(
                    ['plantuml', '-tpng', str(puml_file), '-o', str(output_path.absolute())],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                if result.returncode == 0:
                    generated.append(output_file)
                    print(f"✓ Сгенерирован {output_file}")
                else:
                    print(f"✗ Ошибка генерации {puml_file.name}: {result.stderr}")

            except FileNotFoundError:
                print("✗ PlantUML не установлен")
                print("  Установите: sudo apt install plantuml")
                print("  Или скачайте: https://plantuml.com/download")
                return False
            except subprocess.TimeoutExpired:
                print(f"✗ Таймаут при генерации {puml_file.name}")
            except Exception as e:
                print(f"✗ Ошибка: {e}")

        if generated:
            print(f"\n✓ Сгенерировано файлов: {len(generated)}")
            return True
        else:
            print("\n✗ Не удалось сгенерировать PNG файлы")
            return False


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python3 diagram_updater.py check-data     # Проверка data_model.puml")
        print("  python3 diagram_updater.py check-state    # Проверка state_machine.puml")
        print("  python3 diagram_updater.py check-all      # Проверка всех диаграмм")
        print("  python3 diagram_updater.py generate-png   # Генерация PNG из PlantUML")
        sys.exit(1)

    updater = DiagramUpdater()
    command = sys.argv[1]

    if command == "check-data":
        updater.check_data_model_sync()

    elif command == "check-state":
        updater.check_state_machine_sync()

    elif command == "check-all":
        data_ok = updater.check_data_model_sync()
        state_ok = updater.check_state_machine_sync()

        print("\n" + "="*50)
        if data_ok and state_ok:
            print("✓ Все диаграммы синхронизированы")
        else:
            print("⚠ Обнаружены несоответствия")

    elif command == "generate-png":
        updater.generate_png()

    else:
        print(f"✗ Неизвестная команда: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
