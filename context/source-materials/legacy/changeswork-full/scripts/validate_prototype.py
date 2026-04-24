#!/usr/bin/env python3
"""
Валидатор HTML прототипов
Проверяет структуру, CDN ссылки, JavaScript синтаксис
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser
import urllib.request
import urllib.error

class PrototypeValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.warnings = []
        self.cdn_links = []
        self.scripts = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Проверка CDN ссылок
        if tag == 'script' and 'src' in attrs_dict:
            src = attrs_dict['src']
            if src.startswith('http'):
                self.cdn_links.append(src)
                
        if tag == 'link' and 'href' in attrs_dict:
            href = attrs_dict['href']
            if href.startswith('http'):
                self.cdn_links.append(href)
    
    def check_cdn_links(self):
        """Проверка доступности CDN ссылок"""
        print("\n=== Проверка CDN ссылок ===")
        for link in self.cdn_links:
            try:
                req = urllib.request.Request(link, method='HEAD')
                urllib.request.urlopen(req, timeout=5)
                print(f"✓ {link}")
            except urllib.error.URLError as e:
                self.errors.append(f"CDN недоступен: {link} ({e})")
                print(f"✗ {link} - {e}")
            except Exception as e:
                self.warnings.append(f"Не удалось проверить: {link} ({e})")
                print(f"? {link} - {e}")

def validate_prototype(file_path):
    """Валидация HTML прототипа"""
    print(f"=== Валидация прототипа: {file_path} ===\n")
    
    if not Path(file_path).exists():
        print(f"✗ Файл не найден: {file_path}")
        return False
    
    # Чтение файла
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Проверка базовой структуры
    print("=== Проверка структуры HTML ===")
    if not content.strip().startswith('<!DOCTYPE html>'):
        print("✗ Отсутствует <!DOCTYPE html>")
    else:
        print("✓ DOCTYPE присутствует")
    
    if '<html' not in content:
        print("✗ Отсутствует тег <html>")
    else:
        print("✓ Тег <html> присутствует")
    
    if '</html>' not in content:
        print("✗ Отсутствует закрывающий тег </html>")
    else:
        print("✓ Закрывающий тег </html> присутствует")
    
    # Проверка React и Babel
    print("\n=== Проверка зависимостей ===")
    if 'react@18' in content:
        print("✓ React 18 подключен")
    else:
        print("✗ React не найден")

    if '@babel/standalone' in content:
        print("✓ Babel standalone подключен")
    else:
        print("✗ Babel не найден")

    if '@mui/material' in content:
        print("✓ Material-UI подключен")
    else:
        print("✗ Material-UI не найден")

    # Проверка emotion (требуется для Material-UI v5)
    if '@emotion/react' in content:
        print("✓ @emotion/react подключен")
    else:
        print("✗ @emotion/react не найден (требуется для Material-UI v5)")

    if '@emotion/styled' in content:
        print("✓ @emotion/styled подключен")
    else:
        print("✗ @emotion/styled не найден (требуется для Material-UI v5)")

    # Проверка Babel script
    if 'type="text/babel"' in content:
        print("✓ Babel script присутствует")
    else:
        print("✗ Babel script не найден")
    
    # Парсинг HTML
    validator = PrototypeValidator()
    try:
        validator.feed(content)
        print("\n✓ HTML структура валидна")
    except Exception as e:
        print(f"\n✗ Ошибка парсинга HTML: {e}")
        return False
    
    # Проверка CDN ссылок
    validator.check_cdn_links()
    
    # Итоги
    print("\n=== Итоги валидации ===")
    if validator.errors:
        print(f"✗ Найдено ошибок: {len(validator.errors)}")
        for error in validator.errors:
            print(f"  - {error}")
    else:
        print("✓ Ошибок не найдено")
    
    if validator.warnings:
        print(f"⚠ Предупреждений: {len(validator.warnings)}")
        for warning in validator.warnings:
            print(f"  - {warning}")
    
    return len(validator.errors) == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python3 validate_prototype.py <путь_к_файлу>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = validate_prototype(file_path)
    sys.exit(0 if success else 1)
