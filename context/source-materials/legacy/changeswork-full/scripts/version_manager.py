#!/usr/bin/env python3
"""
Version Manager - Управление версиями спецификации
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime
import json

class VersionManager:
    def __init__(self, spec_dir="spec", versions_dir="spec/versions"):
        self.spec_dir = Path(spec_dir)
        self.versions_dir = Path(versions_dir)

    def create_version(self, version_name: str, description: str = ""):
        """Создание новой версии спецификации"""
        print(f"=== Создание версии {version_name} ===\n")

        # Проверка существования версии
        version_path = self.versions_dir / version_name
        if version_path.exists():
            print(f"✗ Версия {version_name} уже существует")
            return False

        # Создание директории версии
        version_path.mkdir(parents=True, exist_ok=True)

        # Копирование текущих файлов
        files_to_copy = [
            "domain_model.md",
            "data_model.puml",
            "state_machine.puml",
            "GUIDE.md"
        ]

        copied_files = []
        for filename in files_to_copy:
            source = self.spec_dir / filename
            if source.exists():
                dest = version_path / filename
                shutil.copy2(source, dest)
                copied_files.append(filename)
                print(f"✓ Скопирован {filename}")
            else:
                print(f"⚠ Файл {filename} не найден, пропущен")

        # Создание метаданных версии
        metadata = {
            "version": version_name,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "files": copied_files
        }

        metadata_file = version_path / "version.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Версия {version_name} создана")
        print(f"  Расположение: {version_path}")
        print(f"  Файлов: {len(copied_files)}")

        return True

    def list_versions(self):
        """Список всех версий"""
        print("=== Доступные версии ===\n")

        if not self.versions_dir.exists():
            print("Версии не найдены")
            return

        versions = []
        for version_dir in sorted(self.versions_dir.iterdir()):
            if version_dir.is_dir():
                metadata_file = version_dir / "version.json"
                if metadata_file.exists():
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    versions.append(metadata)
                else:
                    # Версия без метаданных
                    versions.append({
                        "version": version_dir.name,
                        "created_at": "unknown",
                        "description": "",
                        "files": []
                    })

        if not versions:
            print("Версии не найдены")
            return

        for v in versions:
            print(f"📦 {v['version']}")
            if v.get('created_at') != 'unknown':
                created = datetime.fromisoformat(v['created_at'])
                print(f"   Создана: {created.strftime('%Y-%m-%d %H:%M')}")
            if v.get('description'):
                print(f"   Описание: {v['description']}")
            print(f"   Файлов: {len(v.get('files', []))}")
            print()

    def compare_versions(self, version1: str, version2: str):
        """Сравнение двух версий"""
        print(f"=== Сравнение версий {version1} и {version2} ===\n")

        v1_path = self.versions_dir / version1
        v2_path = self.versions_dir / version2

        if not v1_path.exists():
            print(f"✗ Версия {version1} не найдена")
            return False

        if not v2_path.exists():
            print(f"✗ Версия {version2} не найдена")
            return False

        # Сравнение файлов
        files_to_compare = ["domain_model.md", "data_model.puml", "state_machine.puml"]

        for filename in files_to_compare:
            file1 = v1_path / filename
            file2 = v2_path / filename

            if not file1.exists() or not file2.exists():
                print(f"⚠ {filename}: файл отсутствует в одной из версий")
                continue

            # Простое сравнение размеров
            size1 = file1.stat().st_size
            size2 = file2.stat().st_size

            if size1 == size2:
                print(f"✓ {filename}: без изменений ({size1} байт)")
            else:
                diff = size2 - size1
                sign = "+" if diff > 0 else ""
                print(f"📝 {filename}: изменён ({sign}{diff} байт)")

        print("\nДля детального сравнения используйте:")
        print(f"  diff {v1_path}/domain_model.md {v2_path}/domain_model.md")

        return True

    def restore_version(self, version_name: str):
        """Восстановление версии (копирование в spec/)"""
        print(f"=== Восстановление версии {version_name} ===\n")

        version_path = self.versions_dir / version_name
        if not version_path.exists():
            print(f"✗ Версия {version_name} не найдена")
            return False

        # Создание резервной копии текущей версии
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Создание резервной копии текущей версии: {backup_name}")
        self.create_version(backup_name, "Автоматическая резервная копия перед восстановлением")

        # Копирование файлов из версии
        files_to_restore = [
            "domain_model.md",
            "data_model.puml",
            "state_machine.puml",
            "GUIDE.md"
        ]

        restored_files = []
        for filename in files_to_restore:
            source = version_path / filename
            if source.exists():
                dest = self.spec_dir / filename
                shutil.copy2(source, dest)
                restored_files.append(filename)
                print(f"✓ Восстановлен {filename}")
            else:
                print(f"⚠ Файл {filename} не найден в версии, пропущен")

        print(f"\n✓ Версия {version_name} восстановлена")
        print(f"  Восстановлено файлов: {len(restored_files)}")
        print(f"  Резервная копия: {backup_name}")

        return True

def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python3 version_manager.py create <version> [description]")
        print("  python3 version_manager.py list")
        print("  python3 version_manager.py compare <version1> <version2>")
        print("  python3 version_manager.py restore <version>")
        sys.exit(1)

    manager = VersionManager()
    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("✗ Укажите имя версии")
            sys.exit(1)
        version = sys.argv[2]
        description = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        manager.create_version(version, description)

    elif command == "list":
        manager.list_versions()

    elif command == "compare":
        if len(sys.argv) < 4:
            print("✗ Укажите две версии для сравнения")
            sys.exit(1)
        manager.compare_versions(sys.argv[2], sys.argv[3])

    elif command == "restore":
        if len(sys.argv) < 3:
            print("✗ Укажите версию для восстановления")
            sys.exit(1)
        manager.restore_version(sys.argv[2])

    else:
        print(f"✗ Неизвестная команда: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()
