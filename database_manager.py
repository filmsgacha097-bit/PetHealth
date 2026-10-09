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
        self._seed_initial_data()

    def _create_tables(self) -> None:
        """Создание таблиц базы данных, если они ещё не существуют."""
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diseases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                species TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS symptoms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disease_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (disease_id) REFERENCES diseases (id) ON DELETE CASCADE
            )
        """)
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

    def _seed_initial_data(self) -> None:
        """Заполняет справочник при первом запуске."""
        self.cursor.execute("SELECT COUNT(*) FROM diseases")
        if self.cursor.fetchone()[0] > 0:
            return

        diseases_data = [
            ("Отит", "Воспаление уха", "Кошка, Собака"),
            ("Чума плотоядных", "Вирусное заболевание", "Собака"),
            ("Хламидиоз", "Инфекционное заболевание", "Кошка"),
            ("Ожирение", "Избыточная масса тела", "Кошка, Собака, Грызун"),
            ("Аллергия", "Реакция на раздражитель", "Кошка, Собака"),
        ]
        symptoms_data = {
            "Отит": ["Зуд в ухе", "Покраснение", "Неприятный запах"],
            "Чума плотоядных": ["Температура", "Отказ от еды", "Выделения из глаз"],
            "Хламидиоз": ["Слезотечение", "Кашель", "Отказ от еды"],
            "Ожирение": ["Избыточный вес", "Одышка"],
            "Аллергия": ["Зуд", "Покраснение кожи", "Выпадение шерсти"],
        }

        disease_ids = {}
        for name, description, species in diseases_data:
            self.cursor.execute(
                "INSERT INTO diseases (name, description, species) VALUES (?, ?, ?)",
                (name, description, species)
            )
            disease_ids[name] = self.cursor.lastrowid

        for disease_name, symptoms in symptoms_data.items():
            for symptom in symptoms:
                self.cursor.execute(
                    "INSERT INTO symptoms (disease_id, name) VALUES (?, ?)",
                    (disease_ids[disease_name], symptom)
                )
        self.connection.commit()

    # ========== CRUD для питомцев ==========

    def add_pet(self, name: str, species: str,
                birth_date: Optional[str] = None,
                photo_path: Optional[str] = None,
                notes: Optional[str] = None) -> int:
        """Добавляет нового питомца.

        Args:
            name (str): Кличка.
            species (str): Вид.
            birth_date (Optional[str]): Дата рождения.
            photo_path (Optional[str]): Путь к фото.
            notes (Optional[str]): Заметки.

        Returns:
            int: ID добавленного питомца.
        """
        self.cursor.execute(
            "INSERT INTO pets (name, species, birth_date, photo_path, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, species, birth_date, photo_path, notes),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_all_pets(self) -> list:
        """Возвращает список всех питомцев."""
        self.cursor.execute("SELECT * FROM pets")
        return self.cursor.fetchall()

    def update_pet(self, pet_id: int, name: str, species: str,
                   birth_date: Optional[str] = None,
                   photo_path: Optional[str] = None,
                   notes: Optional[str] = None) -> None:
        """Обновляет данные питомца.

        Args:
            pet_id (int): ID питомца.
            name (str): Новая кличка.
            species (str): Новый вид.
            birth_date (Optional[str]): Новая дата рождения.
            photo_path (Optional[str]): Новый путь к фото.
            notes (Optional[str]): Новые заметки.
        """
        self.cursor.execute(
            "UPDATE pets SET name = ?, species = ?, birth_date = ?, "
            "photo_path = ?, notes = ? WHERE id = ?",
            (name, species, birth_date, photo_path, notes, pet_id)
        )
        self.connection.commit()

    def delete_pet(self, pet_id: int) -> None:
        """Удаляет питомца по ID.

        Args:
            pet_id (int): ID питомца.
        """
        self.cursor.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
        self.connection.commit()

    # ========== CRUD для записей о здоровье ==========

    def add_record(self, pet_id: int, record_type: str, date: str,
                   value: Optional[str] = None,
                   next_date: Optional[str] = None) -> int:
        """Добавляет запись о здоровье.

        Args:
            pet_id (int): ID питомца.
            record_type (str): Тип (vaccine, parasite, weight, note).
            date (str): Дата процедуры.
            value (Optional[str]): Значение.
            next_date (Optional[str]): Дата следующей процедуры.

        Returns:
            int: ID записи.
        """
        self.cursor.execute(
            "INSERT INTO records (pet_id, record_type, date, value, next_date) "
            "VALUES (?, ?, ?, ?, ?)",
            (pet_id, record_type, date, value, next_date),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_records(self, pet_id: int) -> list:
        """Возвращает записи питомца.

        Args:
            pet_id (int): ID питомца.

        Returns:
            list: Список записей.
        """
        self.cursor.execute("SELECT * FROM records WHERE pet_id = ?", (pet_id,))
        return self.cursor.fetchall()

    def update_record(self, record_id: int, record_type: str, date: str,
                      value: Optional[str] = None,
                      next_date: Optional[str] = None) -> None:
        """Обновляет запись о здоровье.

        Args:
            record_id (int): ID записи.
            record_type (str): Новый тип.
            date (str): Новая дата.
            value (Optional[str]): Новое значение.
            next_date (Optional[str]): Новая дата следующей процедуры.
        """
        self.cursor.execute(
            "UPDATE records SET record_type = ?, date = ?, value = ?, "
            "next_date = ? WHERE id = ?",
            (record_type, date, value, next_date, record_id)
        )
        self.connection.commit()

    def delete_record(self, record_id: int) -> None:
        """Удаляет запись по ID.

        Args:
            record_id (int): ID записи.
        """
        self.cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
        self.connection.commit()

    # ========== CRUD для справочника заболеваний ==========

    def add_disease(self, name: str, description: Optional[str] = None,
                    species: Optional[str] = None) -> int:
        """Добавляет заболевание в справочник.

        Args:
            name (str): Название.
            description (Optional[str]): Описание.
            species (Optional[str]): Вид животного.

        Returns:
            int: ID заболевания.
        """
        self.cursor.execute(
            "INSERT INTO diseases (name, description, species) VALUES (?, ?, ?)",
            (name, description, species),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_diseases(self) -> list:
        """Возвращает все заболевания из справочника."""
        self.cursor.execute("SELECT * FROM diseases")
        return self.cursor.fetchall()

    def add_symptom(self, disease_id: int, name: str) -> int:
        """Добавляет симптом к заболеванию.

        Args:
            disease_id (int): ID заболевания.
            name (str): Название симптома.

        Returns:
            int: ID симптома.
        """
        self.cursor.execute(
            "INSERT INTO symptoms (disease_id, name) VALUES (?, ?)",
            (disease_id, name)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_symptoms(self, disease_id: int) -> list:
        """Возвращает симптомы заболевания.

        Args:
            disease_id (int): ID заболевания.

        Returns:
            list: Список симптомов.
        """
        self.cursor.execute(
            "SELECT * FROM symptoms WHERE disease_id = ?", (disease_id,)
        )
        return self.cursor.fetchall()

    # ========== CRUD для медкарты ==========

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
            status (str): Статус.
            treatment (Optional[str]): Лечение.
            notes (Optional[str]): Заметки.

        Returns:
            int: ID записи.
        """
        self.cursor.execute(
            "INSERT INTO pet_diseases "
            "(pet_id, disease_id, date_start, date_end, status, treatment, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pet_id, disease_id, date_start, date_end, status, treatment, notes),
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def get_pet_diseases(self, pet_id: int) -> list:
        """Возвращает болезни питомца.

        Args:
            pet_id (int): ID питомца.

        Returns:
            list: Список записей о болезнях.
        """
        self.cursor.execute("SELECT * FROM pet_diseases WHERE pet_id = ?", (pet_id,))
        return self.cursor.fetchall()

    def update_pet_disease(self, record_id: int, date_start: str,
                           date_end: Optional[str] = None,
                           status: str = "активно",
                           treatment: Optional[str] = None,
                           notes: Optional[str] = None) -> None:
        """Обновляет запись о болезни питомца.

        Args:
            record_id (int): ID записи.
            date_start (str): Новая дата начала.
            date_end (Optional[str]): Новая дата окончания.
            status (str): Новый статус.
            treatment (Optional[str]): Новое лечение.
            notes (Optional[str]): Новые заметки.
        """
        self.cursor.execute(
            "UPDATE pet_diseases SET date_start = ?, date_end = ?, "
            "status = ?, treatment = ?, notes = ? WHERE id = ?",
            (date_start, date_end, status, treatment, notes, record_id)
        )
        self.connection.commit()

    def delete_pet_disease(self, record_id: int) -> None:
        """Удаляет запись о болезни по ID.

        Args:
            record_id (int): ID записи.
        """
        self.cursor.execute("DELETE FROM pet_diseases WHERE id = ?", (record_id,))
        self.connection.commit()

    def get_upcoming_procedures(self, days: int = 7) -> list:
        """Возвращает записи с предстоящими процедурами.

        Args:
            days (int): Количество дней вперёд.

        Returns:
            list: Список записей.
        """
        from datetime import datetime, timedelta

        today = datetime.now().date()
        end_date = today + timedelta(days=days)

        self.cursor.execute("""
            SELECT pets.name, pets.species, records.record_type,
                   records.next_date, records.value
            FROM records
            JOIN pets ON records.pet_id = pets.id
            WHERE records.next_date IS NOT NULL
              AND records.next_date != ''
        """)

        upcoming = []
        for record in self.cursor.fetchall():
            try:
                next_date = datetime.strptime(record[3], "%d.%m.%Y").date()
                if today <= next_date <= end_date:
                    upcoming.append(record)
            except ValueError:
                continue
        return upcoming

    def close(self) -> None:
        """Закрывает подключение к базе данных."""
        if self.connection:
            self.connection.close()

    def close(self) -> None:
        """Закрытие подключения к базе данных."""
        if self.connection:
            self.connection.close()
