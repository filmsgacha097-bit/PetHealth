"""Интеграционные тесты приложения PetHealth.

Проверяют взаимодействие между слоями:
- бизнес-логика → база данных;
- сценарии работы пользователя (добавление, редактирование, удаление);
- корректность связей между таблицами.

Тесты симулируют действия пользователя через прямые вызовы
методов DatabaseManager, так как UI (CustomTkinter) требует
графического окружения.
"""

import pytest
from database_manager import DatabaseManager


@pytest.fixture
def db():
    """Фикстура: временная БД в памяти."""
    database = DatabaseManager(":memory:")
    yield database
    database.close()


# ========== Сценарий 1: Полный цикл работы с питомцем ==========

def test_full_pet_lifecycle(db):
    """Сценарий: добавить питомца → добавить записи → отредактировать → удалить."""
    # 1. Пользователь добавляет питомца
    pet_id = db.add_pet("Мурка", "Кошка", "01.01.2020", None, "Любит спать")
    assert pet_id is not None

    # 2. Проверяем, что питомец есть в БД
    pets = db.get_all_pets()
    assert len(pets) == 1
    assert pets[0][1] == "Мурка"

    # 3. Пользователь добавляет запись о вакцинации
    db.add_record(pet_id, "vaccine", "15.10.2026", "Бешенство", "15.10.2027")

    # 4. Проверяем, что запись есть в БД
    records = db.get_records(pet_id)
    assert len(records) == 1
    assert records[0][4] == "Бешенство"

    # 5. Пользователь редактирует питомца
    db.update_pet(pet_id, "Мурка Великая", "Кошка", "01.01.2020",
                  None, "Обновлённые заметки")

    # 6. Проверяем, что данные обновились
    pets = db.get_all_pets()
    assert pets[0][1] == "Мурка Великая"
    assert pets[0][5] == "Обновлённые заметки"

    # 7. Пользователь удаляет питомца
    db.delete_pet(pet_id)

    # 8. Проверяем, что питомец удалён
    assert db.get_all_pets() == []

    # 9. Проверяем каскадное удаление записей
    assert db.get_records(pet_id) == []


# ========== Сценарий 2: Работа со справочником ==========

def test_catalog_workflow(db):
    """Сценарий: справочник → болезнь → симптомы."""
    # 1. Справочник уже заполнен при инициализации
    diseases = db.get_diseases()
    assert len(diseases) >= 5

    # 2. Пользователь добавляет новую болезнь
    new_id = db.add_disease("Лишай", "Грибковое заболевание", "Кошка")
    assert new_id is not None

    # 3. Проверяем, что болезнь добавилась
    diseases = db.get_diseases()
    assert any(d[1] == "Лишай" for d in diseases)

    # 4. Пользователь добавляет симптомы к новой болезни
    db.add_symptom(new_id, "Выпадение шерсти")
    db.add_symptom(new_id, "Покраснение кожи")

    # 5. Проверяем симптомы
    symptoms = db.get_symptoms(new_id)
    assert len(symptoms) == 2


# ========== Сценарий 3: Медкарта питомца ==========

def test_pet_medical_card(db):
    """Сценарий: питомец болеет → записываем болезнь → лечим."""
    # 1. Добавляем питомца
    pet_id = db.add_pet("Барсик", "Кошка")

    # 2. Берём болезнь из справочника
    disease_id = db.get_diseases()[0][0]

    # 3. Записываем болезнь
    pd_id = db.add_pet_disease(
        pet_id, disease_id, "01.09.2026",
        status="активно", treatment="Капли"
    )
    assert pd_id is not None

    # 4. Проверяем, что болезнь есть в медкарте
    pet_diseases = db.get_pet_diseases(pet_id)
    assert len(pet_diseases) == 1
    assert pet_diseases[0][5] == "активно"

    # 5. Пользователь лечит питомца — обновляет статус
    db.update_pet_disease(
        pd_id, "01.09.2026", "10.09.2026",
        "вылечено", "Капли", "Помогло"
    )

    # 6. Проверяем обновление
    pet_diseases = db.get_pet_diseases(pet_id)
    assert pet_diseases[0][5] == "вылечено"
    assert pet_diseases[0][6] == "Капли"


# ========== Сценарий 4: Напоминания ==========

def test_reminders_workflow(db):
    """Сценарий: запись с будущей процедурой → попадает в напоминания."""
    from datetime import datetime, timedelta

    # 1. Добавляем питомца
    pet_id = db.add_pet("Хома", "Грызун")

    # 2. Добавляем запись с датой в пределах 7 дней
    soon = (datetime.now() + timedelta(days=3)).strftime("%d.%m.%Y")
    db.add_record(pet_id, "vaccine", "01.10.2026", "Вакцина", soon)

    # 3. Проверяем, что напоминание появилось
    upcoming = db.get_upcoming_procedures(days=7)
    assert len(upcoming) == 1
    assert upcoming[0][0] == "Хома"


# ========== Сценарий 5: Несколько питомцев ==========

def test_multiple_pets_isolation(db):
    """Сценарий: у двух питомцев — свои записи, не смешиваются."""
    # 1. Добавляем двух питомцев
    pet1 = db.add_pet("Мурка", "Кошка")
    pet2 = db.add_pet("Барсик", "Собака")

    # 2. Добавляем записи каждому
    db.add_record(pet1, "vaccine", "15.10.2026", "Бешенство")
    db.add_record(pet2, "parasite", "20.10.2026", "Клещи")

    # 3. Проверяем, что записи не смешались
    records1 = db.get_records(pet1)
    records2 = db.get_records(pet2)

    assert len(records1) == 1
    assert len(records2) == 1
    assert records1[0][2] == "vaccine"
    assert records2[0][2] == "parasite"


# ========== Сценарий 6: Удаление с каскадом ==========

def test_delete_pet_removes_all_related(db):
    """Сценарий: удаление питомца → удаляются все его записи и болезни."""
    # 1. Добавляем питомца
    pet_id = db.add_pet("Мурка", "Кошка")

    # 2. Добавляем записи и болезни
    db.add_record(pet_id, "vaccine", "15.10.2026", "Бешенство")
    dis_id = db.get_diseases()[0][0]
    db.add_pet_disease(pet_id, dis_id, "01.09.2026")

    # 3. Проверяем, что всё есть
    assert len(db.get_records(pet_id)) == 1
    assert len(db.get_pet_diseases(pet_id)) == 1

    # 4. Удаляем питомца
    db.delete_pet(pet_id)

    # 5. Проверяем, что всё удалилось каскадно
    assert db.get_all_pets() == []
    assert db.get_records(pet_id) == []
    assert db.get_pet_diseases(pet_id) == []
