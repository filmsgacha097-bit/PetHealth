"""Модуль работы с базой данных приложения PetHealth.

Содержит класс DatabaseManager, который отвечает за:
- подключение к базе данных SQLite;
- создание таблиц при первом запуске;
- выполнение CRUD-операций (создание, чтение, обновление, удаление).

База данных состоит из пяти таблиц:
- pets — информация о питомцах;
- records — записи о здоровье (вакцинации, обработки, взвешивания);
- diseases — справочник заболеваний;
- symptoms — справочник симптомов;
- pet_diseases — история болезней питомцев.
"""

import sqlite3
from typing import Optional


class DatabaseManager:
    """Класс для работы с базой данных SQLite.

    Отвечает за подключение к БД, создание таблиц
    и выполнение операций с данными.

    Attributes:
        db_name (str): Имя файла базы данных.
        connection (sqlite3.Connection): Подключение к БД.
        cursor (sqlite3.Cursor): Курсор для выполнения запросов.
    """

    def __init__(self, db_name: str = "pets.db") -> None:
        """Инициализация менеджера базы данных.

        Args:
            db_name (str): Имя файла базы данных. По умолчанию "pets.db".
        """
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        """Создание таблиц базы данных, если они ещё не существуют.

        Создаёт пять таблиц: pets, records, diseases, symptoms, pet_diseases.
        Использует IF NOT EXISTS, чтобы не пересоздавать таблицы при повторных запусках.
        """
        # Таблица питомцев
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                species TEXT NOT NULL,
                birth_date TEXT,
                photo_path TEXT,
                notes TEXT
            )
        """)

        # Таблица записей о здоровье
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                record_type TEXT NOT NULL,
                date TEXT NOT NULL,
                value TEXT,
                next_date TEXT,
                FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE
            )
        """)

        # Таблица справочника заболеваний
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                species TEXT
            )
        """)

        # Таблица справочника симптомов
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (disease_id) REFERENCES diseases (id) ON DELETE CASCADE
            )
        """)

        # Таблица истории болезней питомцев (медкарта)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pet_diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_id INTEGER NOT NULL,
                disease_id INTEGER NOT NULL,
                date_start TEXT NOT NULL,
                date_end TEXT,
                status TEXT NOT NULL,
                treatment TEXT,
                notes TEXT,
                FOREIGN KEY (pet_id) REFERENCES pets (id) ON DELETE CASCADE,
                FOREIGN KEY (disease_id) REFERENCES diseases (id) ON DELETE CASCADE
            )
        """)

        self.connection.commit()

    def close(self) -> None:
        """Закрытие подключения к базе данных."""
        if self.connection:
            self.connection.close()