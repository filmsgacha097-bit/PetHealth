"""Главный экран приложения PetHealth.

Содержит класс MainFrame — экран со списком питомцев,
шапкой и кнопками управления.

Это фрейм (CTkFrame), который встраивается в главное окно
PetHealthApp и переключается через него.
"""

import customtkinter as ctk
from tkinter import messagebox


class MainFrame(ctk.CTkFrame):
    """Главный экран со списком питомцев.

    Отображает шапку с логотипом и кнопками, список питомцев
    и кнопку добавления нового питомца.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        on_logout (callable): Функция выхода из аккаунта.
        pets_frame (ctk.CTkScrollableFrame): Фрейм со списком питомцев.
    """

    def __init__(self, master, db, on_logout) -> None:
        """Инициализация главного экрана.

        Args:
            master: Родительское окно (PetHealthApp).
            db (DatabaseManager): Менеджер базы данных.
            on_logout (callable): Функция выхода из аккаунта.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.db = db
        self.on_logout = on_logout

        self._build_header()
        self._build_pets_list()

    def _build_header(self) -> None:
        """Создаёт шапку окна с логотипом и кнопками."""
        header = ctk.CTkFrame(
            self, fg_color="#FFFFFF", height=80, corner_radius=0
        )
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Логотип
        logo = ctk.CTkLabel(
            header, text="🐾 PetHealth",
            font=("Nunito", 24, "bold"), text_color="#FEB2B1"
        )
        logo.pack(side="left", padx=20)

        # Кнопка "Выход"
        btn_exit = ctk.CTkButton(
            header, text="Выход", fg_color="#FEB2B1",
            hover_color="#FFB1CB", text_color="#FFFFFF",
            font=("Nunito", 12, "bold"),
            width=100, command=self.on_logout
        )
        btn_exit.pack(side="right", padx=20)

        # Кнопка "Справочник"
        btn_catalog = ctk.CTkButton(
            header, text="Справочник", fg_color="#BBE6FA",
            hover_color="#A0D8F0", text_color="#333333",
            font=("Nunito", 12, "bold"), width=120,
            command=self.master.show_catalog
        )
        btn_catalog.pack(side="right", padx=5)

        # Кнопка "Все напоминания"
        btn_reminders = ctk.CTkButton(
            header, text="Все напоминания", fg_color="#BBE6FA",
            hover_color="#A0D8F0", text_color="#333333",
            font=("Nunito", 12, "bold"), width=140,
            command=self.master.show_reminders
        )
        btn_reminders.pack(side="right", padx=5)

    def _build_pets_list(self) -> None:
        """Создаёт секцию со списком питомцев и кнопкой добавления."""
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(20, 10))

        title = ctk.CTkLabel(
            title_frame, text="Мои питомцы",
            font=("Nunito", 20, "bold"), text_color="#333333"
        )
        title.pack(side="left")

        btn_add = ctk.CTkButton(
            title_frame, text="+ Добавить питомца",
            fg_color="#FFEF77", hover_color="#FFE055",
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=180, command=self._add_pet_dialog
        )
        btn_add.pack(side="right")

        self.pets_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.pets_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self._refresh_pets()

    def _refresh_pets(self) -> None:
        """Обновляет список питомцев в окне."""
        for widget in self.pets_frame.winfo_children():
            widget.destroy()

        pets = self.db.get_all_pets()

        if not pets:
            empty_label = ctk.CTkLabel(
                self.pets_frame,
                text="Пока нет питомцев. Добавьте первого!",
                font=("Nunito", 14), text_color="#8A8A8A"
            )
            empty_label.pack(pady=20)
            return

        for pet in pets:
            self._create_pet_card(pet)

    def _create_pet_card(self, pet: tuple) -> None:
        """Создаёт карточку питомца в списке.

        Args:
            pet (tuple): Кортеж из БД: (id, name, species, birth_date, photo_path, notes).
        """
        pet_id, name, species, *_ = pet

        card = ctk.CTkFrame(
            self.pets_frame, fg_color="#FFFFFF",
            corner_radius=16, height=100
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)

        emoji = "🐱" if species == "Кошка" else "🐶" if species == "Собака" else "🐹"
        avatar = ctk.CTkLabel(
            card, text=emoji, font=("Nunito", 36),
            width=80, height=80, fg_color="#BBE6FA",
            corner_radius=16
        )
        avatar.pack(side="left", padx=15, pady=10)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, fill="y", pady=20)

        ctk.CTkLabel(
            info_frame, text=name,
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame, text=species,
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w")

        btn_delete = ctk.CTkButton(
            card, text="Удалить", fg_color="#FEB2B1",
            hover_color="#FFB1CB", text_color="#FFFFFF",
            font=("Nunito", 12, "bold"), width=100,
            command=lambda: self._delete_pet(pet_id, name)
        )
        btn_delete.pack(side="right", padx=15)

        btn_open = ctk.CTkButton(
            card, text="Открыть", fg_color="#BBE6FA",
            hover_color="#A0D8F0", text_color="#333333",
            font=("Nunito", 12, "bold"), width=100,
            command=lambda: self.master.show_pet_card(pet_id)
        )
        btn_open.pack(side="right", padx=5)

    def _add_pet_dialog(self) -> None:
        """Открывает диалог добавления нового питомца."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Добавить питомца")
        dialog.geometry("500x550")
        dialog.configure(fg_color="#F7F4EB")

        # Чтобы диалог открывался поверх
        dialog.lift()
        dialog.focus_force()
        dialog.attributes("-topmost", True)
        dialog.after(100, lambda: dialog.attributes("-topmost", False))

        ctk.CTkLabel(
            dialog, text="Добавить питомца",
            font=("Nunito", 20, "bold"), text_color="#FEB2B1"
        ).pack(pady=20)

        ctk.CTkLabel(dialog, text="Кличка", font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        entry_name = ctk.CTkEntry(dialog, placeholder_text="Введите кличку",
                                  width=400, height=40, fg_color="#FFFFFF",
                                  border_color="#BBE6FA")
        entry_name.pack(pady=(0, 15))

        ctk.CTkLabel(dialog, text="Вид животного", font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        combo_species = ctk.CTkComboBox(
            dialog, values=["Кошка", "Собака", "Попугай", "Грызун", "Другое"],
            width=400, height=40, fg_color="#FFFFFF", border_color="#BBE6FA"
        )
        combo_species.pack(pady=(0, 15))

        ctk.CTkLabel(dialog, text="Дата рождения", font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        entry_date = ctk.CTkEntry(dialog, placeholder_text="дд.мм.гггг",
                                  width=400, height=40, fg_color="#FFFFFF",
                                  border_color="#BBE6FA")
        entry_date.pack(pady=(0, 15))

        ctk.CTkLabel(dialog, text="Заметки", font=("Nunito", 12), text_color="#8A8A8A").pack(anchor="w", padx=40)
        entry_notes = ctk.CTkTextbox(dialog, width=400, height=80,
                                     fg_color="#FFFFFF", border_color="#BBE6FA")
        entry_notes.pack(pady=(0, 20))
                # Enter в полях — сохранить
        for entry in (entry_name, entry_date):
            entry.bind("<Return>", lambda e: save())

        def save():
            """Сохраняет питомца в БД и обновляет список."""
            name = entry_name.get().strip()
            species = combo_species.get().strip()

            if not name or not species:
                messagebox.showerror("Ошибка", "Заполните кличку и вид животного")
                return

            birth_date = entry_date.get().strip() or None
            notes = entry_notes.get("1.0", "end").strip() or None

            self.db.add_pet(name, species, birth_date, None, notes)
            self._refresh_pets()
            dialog.destroy()

        ctk.CTkButton(
            dialog, text="Сохранить", fg_color="#FEB2B1",
            hover_color="#FFB1CB", text_color="#FFFFFF",
            font=("Nunito", 14, "bold"), width=200, height=44,
            command=save
        ).pack(pady=5)

        ctk.CTkButton(
            dialog, text="Отмена", fg_color="#F7F4EB",
            border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 14, "bold"),
            width=200, height=44, command=dialog.destroy
        ).pack(pady=5)

    def _delete_pet(self, pet_id: int, name: str) -> None:
        """Удаляет питомца после подтверждения.

        Args:
            pet_id (int): ID питомца.
            name (str): Кличка питомца.
        """
        if messagebox.askyesno("Подтверждение", f"Удалить питомца {name}?"):
            self.db.delete_pet(pet_id)
            self._refresh_pets()