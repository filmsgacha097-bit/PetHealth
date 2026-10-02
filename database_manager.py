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
        self.connection.execute("PRAGMA foreign_keys = ON;")
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
            # ========== CRUD для питомцев ==========

    def add_pet(self, name: str, species: str,
                birth_date: Optional[str] = None,
                photo_path: Optional[str] = None,
                notes: Optional[str] = None) -> int:
        """Добавляет нового питомца в базу данных.

        Args:
            name (str): Кличка питомца.
            species (str): Вид животного.
            birth_date (Optional[str]): Дата рождения.
            photo_path (Optional[str]): Путь к фото.
            notes (Optional[str]): Заметки.

        Returns:
            int: ID добавленного питомца.
        """
        self.cursor.execute(
            "INSERT INTO pets (name, species, birth_date, photo_path, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, species, birth_date, photo_path, notes)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_pets(self) -> list:
        """Возвращает список всех питомцев.

        Returns:
            list: Список кортежей (id, name, species, birth_date, photo_path, notes).
        """
        self.cursor.execute("SELECT * FROM pets")
        return self.cursor.fetchall()

    def delete_pet(self, pet_id: int) -> None:
        """Удаляет питомца по ID. Записи и болезни удаляются каскадно.

        Args:
            pet_id (int): ID питомца.
        """
        self.cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
        self.connection.commit()

    # ========== CRUD для записей о здоровье ==========

    def add_record(self, pet_id: int, record_type: str, date: str,
                   value: Optional[str] = None,
                   next_date: Optional[str] = None) -> int:
        """Добавляет запись о здоровье питомца.

        Args:
            pet_id (int): ID питомца.
            record_type (str): Тип записи (vaccine, parasite, weight, note).
            date (str): Дата процедуры.
            value (Optional[str]): Значение записи.
            next_date (Optional[str]): Дата следующей процедуры.

        Returns:
            int: ID добавленной записи.
        """
        self.cursor.execute(
            "INSERT INTO records (pet_id, record_type, date, value, next_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (pet_id, record_type, date, value, next_date)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_records(self, pet_id: int) -> list:
        """Возвращает все записи о здоровье питомца.

        Args:
            pet_id (int): ID питомца.

        Returns:
            list: Список записей.
        """
        self.cursor.execute("SELECT * FROM records WHERE pet_id = ?", (pet_id,))
        return self.cursor.fetchall()

    def delete_record(self, record_id: int) -> None:
        """Удаляет запись о здоровье по ID."""
        self.cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        self.connection.commit()

    # ========== CRUD для справочника заболеваний ==========

    def add_disease(self, name: str, description: Optional[str] = None,
                    species: Optional[str] = None) -> int:
        """Добавляет заболевание в справочник.

        Args:
            name (str): Название заболевания.
            description (Optional[str]): Описание.
            species (Optional[str]): Для какого вида характерно.

        Returns:
            int: ID добавленного заболевания.
        """
        self.cursor.execute(
            "INSERT INTO diseases (name, description, species) VALUES (?, ?, ?)",
            (name, description, species)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_diseases(self) -> list:
        """Возвращает все заболевания из справочника.

        Returns:
            list: Список заболеваний.
        """
        self.cursor.execute("SELECT * FROM diseases")
        return self.cursor.fetchall()

    # ========== CRUD для медкарты (болезни питомцев) ==========

    def add_pet_disease(self, pet_id: int, disease_id: int, date_start: str,
                        date_end: Optional[str] = None, status: str = "активно",
                        treatment: Optional[str] = None,
                        notes: Optional[str] = None) -> int:
        """Добавляет запись о болезни питомца.

        Args:
            pet_id (int): ID питомца.
            disease_id (int): ID заболевания.
            date_start (str): Дата начала.
            date_end (Optional[str]): Дата окончания.
            status (str): Статус (активно, вылечено, хроническое).
            treatment (Optional[str]): Лечение.
            notes (Optional[str]): Заметки.

        Returns:
            int: ID добавленной записи.
        """
        self.cursor.execute(
            "INSERT INTO pet_diseases "
            "(pet_id, disease_id, date_start, date_end, status, treatment, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pet_id, disease_id, date_start, date_end, status, treatment, notes)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_pet_diseases(self, pet_id: int) -> list:
        """Возвращает все болезни питомца.

        Args:
            pet_id (int): ID питомца.

        Returns:
            list: Список записей о болезнях.
        """
        self.cursor.execute("SELECT * FROM pet_diseases WHERE pet_id = ?", (pet_id,))
        return self.cursor.fetchall()

    def delete_pet_disease(self, record_id: int) -> None:
        """Удаляет запись о болезни питомца по ID."""
        self.cursor.execute("DELETE FROM pet_diseases WHERE id = ?", (record_id,))
        self.connection.commit()

    def close(self) -> None:
        """Закрытие подключения к базе данных."""
        if self.connection:
            self.connection.close()