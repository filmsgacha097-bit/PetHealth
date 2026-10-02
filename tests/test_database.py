"""Тесты для модуля database_manager.

Проверяют корректность CRUD-операций:
- добавление, чтение и удаление питомцев;
- добавление и чтение записей о здоровье;
- добавление и чтение заболеваний;
- добавление и чтение болезней питомцев.

Для изоляции тестов используется временная база данных в памяти.
"""

import pytest
from database_manager import DatabaseManager


@pytest.fixture
def db():
    """Фикстура: создаёт временную БД в памяти для каждого теста.

    Yields:
        DatabaseManager: Менеджер с пустой базой.
    """
    database = DatabaseManager(":memory:")
    yield database
    database.close()


def test_add_pet(db):
    """Тест: добавление питомца."""
    pet_id = db.add_pet("Мурка", "Кошка", "01.01.2020")
    assert pet_id == 1

    pets = db.get_all_pets()
    assert len(pets) == 1
    assert pets[0][1] == "Мурка"
    assert pets[0][2] == "Кошка"


def test_add_multiple_pets(db):
    """Тест: добавление нескольких питомцев."""
    db.add_pet("Мурка", "Кошка")
    db.add_pet("Барсик", "Собака")
    db.add_pet("Хома", "Грызун")

    pets = db.get_all_pets()
    assert len(pets) == 3


def test_delete_pet(db):
    """Тест: удаление питомца."""
    pet_id = db.add_pet("Мурка", "Кошка")
    db.delete_pet(pet_id)

    pets = db.get_all_pets()
    assert len(pets) == 0


def test_add_record(db):
    """Тест: добавление записи о здоровье."""
    pet_id = db.add_pet("Мурка", "Кошка")
    db.add_record(pet_id, "vaccine", "15.10.2026", "Бешенство", "15.10.2027")

    records = db.get_records(pet_id)
    assert len(records) == 1
    assert records[0][2] == "vaccine"
    assert records[0][4] == "Бешенство"


def test_add_disease(db):
    """Тест: добавление заболевания в справочник."""
    disease_id = db.add_disease("Отит", "Воспаление уха", "Кошка")
    assert disease_id == 1

    diseases = db.get_diseases()
    assert len(diseases) == 1
    assert diseases[0][1] == "Отит"


def test_add_pet_disease(db):
    """Тест: добавление болезни питомцу."""
    pet_id = db.add_pet("Мурка", "Кошка")
    disease_id = db.add_disease("Отит", "Воспаление уха", "Кошка")
    db.add_pet_disease(pet_id, disease_id, "01.09.2026",
                       status="вылечено", treatment="Капли")

    pet_diseases = db.get_pet_diseases(pet_id)
    assert len(pet_diseases) == 1
    assert pet_diseases[0][5] == "вылечено"


def test_delete_pet_cascade(db):
    """Тест: каскадное удаление записей при удалении питомца."""
    pet_id = db.add_pet("Мурка", "Кошка")
    db.add_record(pet_id, "vaccine", "15.10.2026", "Бешенство")

    db.delete_pet(pet_id)

    records = db.get_records(pet_id)
    assert len(records) == 0