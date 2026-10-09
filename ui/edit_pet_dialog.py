"""Диалог редактирования данных питомца.

Содержит класс EditPetDialog — модальное окно с формой
для изменения клички, вида, даты рождения и заметок питомца.
"""

import customtkinter as ctk
from tkinter import messagebox


class EditPetDialog(ctk.CTkToplevel):
    """Модальное окно редактирования питомца.

    Открывается из карточки питомца. После сохранения вызывает
    callback on_save, чтобы карточка обновила данные.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        pet (tuple): Данные питомца из БД.
        on_save (callable): Функция обновления карточки.
    """

    def __init__(self, master, db, pet: tuple, on_save) -> None:
        """Инициализация диалога редактирования.

        Args:
            master: Родительское окно.
            db (DatabaseManager): Менеджер базы данных.
            pet (tuple): Кортеж из БД (id, name, species, birth_date, photo_path, notes).
            on_save (callable): Функция обновления карточки.
        """
        super().__init__(master)
        self.db = db
        self.pet = pet
        self.on_save = on_save

        self.title("Редактировать питомца")
        self.geometry("500x550")
        self.resizable(False, False)
        self.configure(fg_color="#F7F4EB")

        self.lift()
        self.focus_force()
        self.grab_set()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы редактирования."""
        pet_id, name, species, birth_date, photo_path, notes = self.pet

        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=24)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            card, text="Редактировать питомца",
            font=("Nunito", 22, "bold"), text_color="#FEB2B1"
        ).pack(pady=(20, 20))

        # Кличка
        ctk.CTkLabel(card, text="Кличка",
                     font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        self.entry_name = ctk.CTkEntry(
            card, width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_name.insert(0, name)
        self.entry_name.pack(pady=(0, 15))

        # Вид
        ctk.CTkLabel(card, text="Вид животного",
                     font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        self.combo_species = ctk.CTkComboBox(
            card, values=["Кошка", "Собака", "Попугай", "Грызун", "Другое"],
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.combo_species.set(species)
        self.combo_species.pack(pady=(0, 15))

        # Дата рождения
        ctk.CTkLabel(card, text="Дата рождения",
                     font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        self.entry_date = ctk.CTkEntry(
            card, placeholder_text="дд.мм.гггг",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        if birth_date:
            self.entry_date.insert(0, birth_date)
        self.entry_date.pack(pady=(0, 15))

        # Заметки
        ctk.CTkLabel(card, text="Заметки",
                     font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        self.entry_notes = ctk.CTkTextbox(
            card, width=400, height=80,
            fg_color="#F7F4EB", border_color="#BBE6FA"
        )
        if notes:
            self.entry_notes.insert("1.0", notes)
        self.entry_notes.pack(pady=(0, 20))

        # Кнопки
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(pady=(5, 20))

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
        """Сохраняет изменения и вызывает on_save."""
        pet_id = self.pet[0]
        name = self.entry_name.get().strip()
        species = self.combo_species.get().strip()
        birth_date = self.entry_date.get().strip() or None
        notes = self.entry_notes.get("1.0", "end").strip() or None

        if not name or not species:
            messagebox.showerror("Ошибка", "Заполните кличку и вид")
            return

        self.db.update_pet(pet_id, name, species, birth_date, None, notes)
        self.on_save()
        self.destroy()