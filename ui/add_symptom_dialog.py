"""Диалог добавления симптома к заболеванию.

Содержит класс AddSymptomDialog — модальное окно для добавления
нового симптома к выбранному заболеванию.
"""

import customtkinter as ctk
from tkinter import messagebox


class AddSymptomDialog(ctk.CTkToplevel):
    """Модальное окно добавления симптома.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        disease_id (int): ID заболевания.
        disease_name (str): Название заболевания (для заголовка).
        on_save (callable): Функция, вызываемая после сохранения.
    """

    def __init__(self, master, db, disease_id: int,
                 disease_name: str, on_save) -> None:
        """Инициализация диалога.

        Args:
            master: Родительское окно.
            db (DatabaseManager): Менеджер базы данных.
            disease_id (int): ID заболевания.
            disease_name (str): Название заболевания.
            on_save (callable): Функция обновления справочника.
        """
        super().__init__(master)
        self.db = db
        self.disease_id = disease_id
        self.disease_name = disease_name
        self.on_save = on_save

        self.title("Добавить симптом")
        self.geometry("480x350")
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
            card, text="Новый симптом",
            font=("Nunito", 22, "bold"), text_color="#FEB2B1"
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            card, text=f"Заболевание: {self.disease_name}",
            font=("Nunito", 14), text_color="#8A8A8A"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            card, text="Название симптома",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_name = ctk.CTkEntry(
            card, placeholder_text="Например: Зуд в ухе",
            width=360, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_name.pack(pady=(0, 25))
        self.entry_name.bind("<Return>", lambda e: self._save())

        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(pady=(5, 20))

        ctk.CTkButton(
            buttons_frame, text="Отмена",
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=160, height=42, corner_radius=12,
            command=self.destroy
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame, text="Сохранить",
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            width=160, height=42, corner_radius=12,
            command=self._save
        ).pack(side="left", padx=5)

    def _save(self) -> None:
        """Сохраняет симптом в БД и вызывает on_save."""
        name = self.entry_name.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "Заполните название симптома")
            return

        self.db.add_symptom(self.disease_id, name)
        self.on_save()
        self.destroy()