"""Тесты безопасности приложения PetHealth.

Проверяют, что приложение защищено от SQL-инъекций.
Все запросы параметризованы, поэтому вредоносный ввод
не может изменить структуру БД.
"""

import pytest
from database_manager import DatabaseManager


@pytest.fixture
def db():
    """Фикстура: временная БД в памяти."""
    database = DatabaseManager(":memory:")
    yield database
    database.close()


def test_sql_injection_drop_table(db):
    """Тест: попытка DROP TABLE через поле name — не должна сработать."""
    malicious_name = "'; DROP TABLE pets; --"

    # Пытаемся добавить питомца с вредоносным именем
    db.add_pet(malicious_name, "Кошка")

    # Таблица pets должна существовать
    pets = db.get_all_pets()
    assert len(pets) == 1
    # Имя сохранено как текст, а не выполнено как SQL
    assert pets[0][1] == malicious_name


def test_sql_injection_delete_all(db):
    """Тест: попытка удалить всех питомцев через инъекцию."""
    db.add_pet("Мурка", "Кошка")
    db.add_pet("Барсик", "Собака")

    # Пытаемся через запись удалить всё
    db.add_record(1, "vaccine", "'; DELETE FROM pets; --", "Бешенство")

    # Питомцы должны остаться
    pets = db.get_all_pets()
    assert len(pets) == 2


def test_sql_injection_union(db):
    """Тест: попытка UNION SELECT через поле species."""
    malicious = "' UNION SELECT * FROM users --"
    db.add_pet("Мурка", malicious)

    pets = db.get_all_pets()
    assert len(pets) == 1
    # Вид сохранён как текст, а не выполнен как SQL
    assert pets[0][2] == malicious


def test_sql_injection_or_always_true(db):
    """Тест: попытка OR 1=1 через логин."""
    # В нашем приложении логин хранится в auth.py (не в БД),
    # но проверим, что аналогичная инъекция не сработает в БД
    db.add_pet("' OR '1'='1", "Кошка")

    pets = db.get_all_pets()
    # Должен быть только 1 питомец, а не все (если бы OR сработал)
    assert len(pets) == 1


def test_sql_injection_comment(db):
    """Тест: попытка комментария через -- не должна ломать запрос."""
    db.add_pet("Мурка", "Кошка")
    db.add_pet("Тест -- комментарий", "Собака")

    pets = db.get_all_pets()
    assert len(pets) == 2


def test_sql_injection_semicolon(db):
    """Тест: точка с запятой не должна разделять запросы."""
    malicious = "Мурка; DELETE FROM pets;"
    db.add_pet(malicious, "Кошка")

    pets = db.get_all_pets()
    assert len(pets) == 1
    assert pets[0][1] == malicious


def test_sql_injection_in_search(db):
    """Тест: инъекция в фильтр по дате не должна срабатывать."""
    db.add_pet("Мурка", "Кошка")
    db.add_record(1, "vaccine", "15.10.2026", "'; DROP TABLE records; --")

    records = db.get_records(1)
    assert len(records) == 1
    # Таблица records не должна удалиться
    assert records[0][2] == "vaccine"


def test_sql_injection_update(db):
    """Тест: попытка UPDATE всех записей через инъекцию."""
    db.add_pet("Мурка", "Кошка")
    db.add_pet("Барсик", "Собака")

    # Пытаемся обновить всех через инъекцию в имени
    db.update_pet(1, "Мурка'; UPDATE pets SET name='hacked'; --",
                  "Кошка")

    pets = db.get_all_pets()
    # Второй питомец не должен измениться
    assert pets[1][1] == "Барсик"