"""Конфигурация pytest для проекта PetHealth.

Добавляет корневую папку проекта в sys.path, чтобы тесты
могли импортировать модули database_manager и models.
"""

import sys
from pathlib import Path

# Добавляем корень проекта в путь импорта
sys.path.insert(0, str(Path(__file__).parent))