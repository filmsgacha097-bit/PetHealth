"""Диалог добавления записи о здоровье питомца.

Содержит класс AddRecordDialog — модальное окно с формой
для добавления записи о вакцинации, обработке, взвешивании
или заметке. Открывается из карточки питомца.
"""

import customtkinter as ctk
from tkinter import messagebox


class AddRecordDialog(ctk.CTkToplevel):
    """Модальное окно добавления записи о здоровье.

    Открывается из карточки питомца. После сохранения вызывает
    callback on_save, чтобы карточка обновила список записей.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        pet_id (int): ID питомца.
        on_save (callable): Функция, вызываемая после сохранения записи.
    """

    def __init__(self, master, db, pet_id: int, on_save) -> None:
        """Инициализация диалога добавления записи.

        Args:
            master: Родительское окно.
            db (DatabaseManager): Менеджер базы данных.
            pet_id (int): ID питомца.
            on_save (callable): Функция обновления карточки после сохранения.
        """
        super().__init__(master)
        self.db = db
        self.pet_id = pet_id
        self.on_save = on_save

        self.title("Добавить запись")
        self.geometry("520x620")
        self.resizable(False, False)
        self.configure(fg_color="#F7F4EB")

        # Открыть поверх и перехватить фокус
        self.lift()
        self.focus_force()
        self.grab_set()  # делает окно модальным
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы добавления записи."""
        # Белая карточка
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=24)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        ctk.CTkLabel(
            card, text="Добавить запись",
            font=("Nunito", 22, "bold"), text_color="#FEB2B1"
        ).pack(pady=(20, 20))

        # Поле "Тип записи"
        ctk.CTkLabel(
            card, text="Тип записи",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.combo_type = ctk.CTkComboBox(
            card,
            values=["Вакцинация", "Обработка", "Взвешивание", "Заметка"],
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.combo_type.pack(pady=(0, 15))

        # Поле "Дата процедуры"
        ctk.CTkLabel(
            card, text="Дата процедуры",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_date = ctk.CTkEntry(
            card, placeholder_text="дд.мм.гггг",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_date.pack(pady=(0, 15))

        # Поле "Значение"
        ctk.CTkLabel(
            card, text="Значение",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_value = ctk.CTkEntry(
            card, placeholder_text="Название вакцины / вес / текст",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_value.pack(pady=(0, 15))

        # Поле "Дата следующей процедуры"
        ctk.CTkLabel(
            card, text="Дата следующей процедуры",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_next_date = ctk.CTkEntry(
            card, placeholder_text="дд.мм.гггг (необязательно)",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_next_date.pack(pady=(0, 25))

        # Кнопки
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(pady=(10, 20))

        ctk.CTkButton(
            buttons_frame, text="Отмена",
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=180, height=42, corner_radius=12,
            command=self.destroy
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame, text="Сохранить",
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            width=180, height=42, corner_radius=12,
            command=self._save
        ).pack(side="left", padx=5)

    def _save(self) -> None:
        """Сохраняет запись в БД и вызывает on_save."""
        rec_type = self.combo_type.get().strip()
        date = self.entry_date.get().strip()
        value = self.entry_value.get().strip() or None
        next_date = self.entry_next_date.get().strip() or None

        if not date:
            messagebox.showerror("Ошибка", "Заполните дату процедуры")
            return

        # Преобразуем русский тип в код, который хранится в БД
        type_map = {
            "Вакцинация": "vaccine",
            "Обработка": "parasite",
            "Взвешивание": "weight",
            "Заметка": "note",
        }
        record_type = type_map.get(rec_type, "note")

        self.db.add_record(self.pet_id, record_type, date, value, next_date)
        self.on_save()
        self.destroy()