"""Диалог добавления заболевания в справочник.

Содержит класс AddDiseaseToCatalogDialog — модальное окно
для добавления нового заболевания в справочник.
"""

import customtkinter as ctk
from tkinter import messagebox


class AddDiseaseToCatalogDialog(ctk.CTkToplevel):
    """Модальное окно добавления заболевания в справочник.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        on_save (callable): Функция, вызываемая после сохранения.
    """

    def __init__(self, master, db, on_save) -> None:
        """Инициализация диалога.

        Args:
            master: Родительское окно.
            db (DatabaseManager): Менеджер базы данных.
            on_save (callable): Функция обновления справочника.
        """
        super().__init__(master)
        self.db = db
        self.on_save = on_save

        self.title("Добавить заболевание в справочник")
        self.geometry("520x500")
        self.resizable(False, False)
        self.configure(fg_color="#F7F4EB")

        self.lift()
        self.focus_force()
        self.grab_set()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы."""
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=24)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            card, text="Новое заболевание",
            font=("Nunito", 22, "bold"), text_color="#FEB2B1"
        ).pack(pady=(20, 20))

        ctk.CTkLabel(
            card, text="Название",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_name = ctk.CTkEntry(
            card, placeholder_text="Например: Отит",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_name.pack(pady=(0, 15))

        ctk.CTkLabel(
            card, text="Описание",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_description = ctk.CTkEntry(
            card, placeholder_text="Краткое описание",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_description.pack(pady=(0, 15))

        ctk.CTkLabel(
            card, text="Вид животного",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.combo_species = ctk.CTkComboBox(
            card, values=["Кошка", "Собака", "Попугай", "Грызун", "Другое"],
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.combo_species.pack(pady=(0, 25))

                # Enter в полях — сохранить
        for entry in (self.entry_name, self.entry_description):
            entry.bind("<Return>", lambda e: self._save()) 

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
        """Сохраняет заболевание в справочник и вызывает on_save."""
        name = self.entry_name.get().strip()
        description = self.entry_description.get().strip() or None
        species = self.combo_species.get().strip() or None

        if not name:
            messagebox.showerror("Ошибка", "Заполните название заболевания")
            return

        try:
            self.db.add_disease(name, description, species)
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось добавить заболевание.\n"
                f"Возможно, оно уже есть в справочнике.\n\n{e}"
            )
            return

        self.on_save()
        self.destroy()