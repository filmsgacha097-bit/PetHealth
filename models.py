"""Модели данных приложения PetHealth.

Содержит четыре класса-модели:
- Pet — информация о питомце;
- Record — запись о здоровье (вакцинация, обработка, взвешивание, заметка);
- Disease — заболевание из справочника;
- PetDisease — запись о болезни питомца (медкарта).

Каждый класс имеет метод get_info(), возвращающий строковое описание объекта.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Pet:
    """Модель питомца.

    Attributes:
        id (Optional[int]): Уникальный идентификатор питомца.
        name (str): Кличка питомца.
        species (str): Вид животного (кошка, собака, попугай, грызун, другое).
        birth_date (Optional[str]): Дата рождения в формате ДД.ММ.ГГГГ.
        photo_path (Optional[str]): Путь к файлу фотографии питомца.
        notes (Optional[str]): Дополнительные заметки.
    """

    id: Optional[int] = None
    name: str = ""
    species: str = ""
    birth_date: Optional[str] = None
    photo_path: Optional[str] = None
    notes: Optional[str] = None

    def get_info(self) -> str:
        """Возвращает краткое описание питомца.

        Returns:
            str: Строка вида "Мурка (Кошка)".
        """
        return f"{self.name} ({self.species})"


@dataclass
class Record:
    """Модель записи о здоровье питомца.

    Attributes:
        id (Optional[int]): Уникальный идентификатор записи.
        pet_id (int): Идентификатор питомца, к которому относится запись.
        record_type (str): Тип записи: vaccine, parasite, weight, note.
        date (str): Дата процедуры в формате ДД.ММ.ГГГГ.
        value (Optional[str]): Значение (название вакцины, вес, текст заметки).
        next_date (Optional[str]): Дата следующей процедуры.
    """

    id: Optional[int] = None
    pet_id: int = 0
    record_type: str = ""
    date: str = ""
    value: Optional[str] = None
    next_date: Optional[str] = None

    def get_info(self) -> str:
        """Возвращает краткое описание записи.

        Returns:
            str: Строка вида "vaccine: Бешенство (15.10.2026)".
        """
        return f"{self.record_type}: {self.value or '—'} ({self.date})"


@dataclass
class Disease:
    """Модель заболевания из справочника.

    Attributes:
        id (Optional[int]): Уникальный идентификатор заболевания.
        name (str): Название заболевания.
        description (Optional[str]): Краткое описание.
        species (Optional[str]): Для какого вида животного характерно.
    """

    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    species: Optional[str] = None

    def get_info(self) -> str:
        """Возвращает краткое описание заболевания.

        Returns:
            str: Название заболевания.
        """
        return self.name


@dataclass
class PetDisease:
    """Модель записи о болезни питомца (медкарта).

    Attributes:
        id (Optional[int]): Уникальный идентификатор записи.
        pet_id (int): Идентификатор питомца.
        disease_id (int): Идентификатор заболевания из справочника.
        date_start (str): Дата начала заболевания.
        date_end (Optional[str]): Дата окончания заболевания.
        status (str): Статус: "активно", "вылечено", "хроническое".
        treatment (Optional[str]): Назначенное лечение.
        notes (Optional[str]): Дополнительные заметки.
    """

    id: Optional[int] = None
    pet_id: int = 0
    disease_id: int = 0
    date_start: str = ""
    date_end: Optional[str] = None
    status: str = "активно"
    treatment: Optional[str] = None
    notes: Optional[str] = None

    def get_info(self) -> str:
        """Возвращает краткое описание болезни питомца.

        Returns:
            str: Строка вида "Отит (активно)".
        """
        return f"Болезнь #{self.disease_id} ({self.status})"

    def get_status(self) -> str:
        """Возвращает статус болезни.

        Returns:
            str: Один из статусов: "активно", "вылечено", "хроническое".
        """
        return self.status