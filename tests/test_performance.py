"""Тесты производительности приложения PetHealth.

Проверяют, что время отклика на ключевые операции
не превышает требования ТЗ (не более 1 секунды).
"""

import time
import pytest
from database_manager import DatabaseManager


@pytest.fixture
def db():
    """Фикстура: временная БД в памяти."""
    database = DatabaseManager(":memory:")
    yield database
    database.close()


def test_add_100_pets_performance(db):
    """Тест: добавление 100 питомцев — не дольше 1 секунды."""
    start = time.time()

    for i in range(100):
        db.add_pet(f"Питомец{i}", "Кошка", "01.01.2020")

    elapsed = time.time() - start
    print(f"\nДобавление 100 питомцев: {elapsed:.3f} сек")

    pets = db.get_all_pets()
    assert len(pets) == 100
    assert elapsed < 1.0, f"Слишком медленно: {elapsed:.3f} сек"


def test_get_all_pets_performance(db):
    """Тест: получение всех питомцев — быстрее 1 секунды."""
    # Подготовка: 100 питомцев
    for i in range(100):
        db.add_pet(f"Питомец{i}", "Кошка")

    start = time.time()
    pets = db.get_all_pets()
    elapsed = time.time() - start

    print(f"\nПолучение 100 питомцев: {elapsed:.3f} сек")
    assert len(pets) == 100
    assert elapsed < 1.0


def test_add_100_records_performance(db):
    """Тест: добавление 100 записей — не дольше 1 секунды."""
    pet_id = db.add_pet("Мурка", "Кошка")

    start = time.time()
    for i in range(100):
        db.add_record(pet_id, "vaccine", f"{i+1:02d}.10.2026", f"Вакцина{i}")
    elapsed = time.time() - start

    print(f"\nДобавление 100 записей: {elapsed:.3f} сек")
    assert elapsed < 1.0

    records = db.get_records(pet_id)
    assert len(records) == 100


def test_search_performance(db):
    """Тест: получение записей питомца — быстрее 1 секунды."""
    pet_id = db.add_pet("Мурка", "Кошка")
    for i in range(100):
        db.add_record(pet_id, "vaccine", f"{i+1:02d}.10.2026", f"Вакцина{i}")

    start = time.time()
    records = db.get_records(pet_id)
    elapsed = time.time() - start

    print(f"\nПолучение 100 записей: {elapsed:.3f} сек")
    assert len(records) == 100
    assert elapsed < 1.0


def test_update_performance(db):
    """Тест: обновление 100 питомцев — быстрее 1 секунды."""
    ids = [db.add_pet(f"Питомец{i}", "Кошка") for i in range(100)]

    start = time.time()
    for pet_id in ids:
        db.update_pet(pet_id, f"Обновлённый{pet_id}", "Собака")
    elapsed = time.time() - start

    print(f"\nОбновление 100 питомцев: {elapsed:.3f} сек")
    assert elapsed < 1.0


def test_delete_performance(db):
    """Тест: удаление 100 питомцев — быстрее 1 секунды."""
    ids = [db.add_pet(f"Питомец{i}", "Кошка") for i in range(100)]

    start = time.time()
    for pet_id in ids:
        db.delete_pet(pet_id)
    elapsed = time.time() - start

    print(f"\nУдаление 100 питомцев: {elapsed:.3f} сек")
    assert elapsed < 1.0
    assert db.get_all_pets() == []


def test_upcoming_procedures_performance(db):
    """Тест: получение напоминаний — быстрее 1 секунды."""
    from datetime import datetime, timedelta

    pet_id = db.add_pet("Мурка", "Кошка")
    soon = (datetime.now() + timedelta(days=3)).strftime("%d.%m.%Y")

    for i in range(100):
        db.add_record(pet_id, "vaccine", "01.10.2026", f"Вакцина{i}", soon)

    start = time.time()
    upcoming = db.get_upcoming_procedures(days=7)
    elapsed = time.time() - start

    print(f"\nПолучение напоминаний: {elapsed:.3f} сек")
    assert len(upcoming) == 100
    assert elapsed < 1.0