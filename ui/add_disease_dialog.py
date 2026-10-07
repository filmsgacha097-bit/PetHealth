"""Диалог добавления заболевания питомца.

Содержит класс AddDiseaseDialog — модальное окно с формой
для добавления записи о болезни питомца: выбор заболевания
из справочника, даты, статус, лечение, заметки.
"""

import customtkinter as ctk
from tkinter import messagebox


class AddDiseaseDialog(ctk.CTkToplevel):
    """Модальное окно добавления заболевания питомца.

    Открывается из карточки питомца. После сохранения вызывает
    callback on_save, чтобы карточка обновила список болезней.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        pet_id (int): ID питомца.
        on_save (callable): Функция, вызываемая после сохранения.
    """

    def __init__(self, master, db, pet_id: int, on_save) -> None:
        """Инициализация диалога добавления заболевания.

        Args:
            master: Родительское окно.
            db (DatabaseManager): Менеджер базы данных.
            pet_id (int): ID питомца.
            on_save (callable): Функция обновления карточки.
        """
        super().__init__(master)
        self.db = db
        self.pet_id = pet_id
        self.on_save = on_save

        self.title("Добавить заболевание")
        self.geometry("520x680")
        self.resizable(False, False)
        self.configure(fg_color="#F7F4EB")

        self.lift()
        self.focus_force()
        self.grab_set()
        self.attributes("-topmost", True)
        self.after(100, lambda: self.attributes("-topmost", False))

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы добавления заболевания."""
        card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=24)
        card.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            card, text="Добавить заболевание",
            font=("Nunito", 22, "bold"), text_color="#FEB2B1"
        ).pack(pady=(20, 20))

        # Список заболеваний из справочника
        diseases = self.db.get_diseases()
        disease_names = [d[1] for d in diseases] if diseases else ["Нет заболеваний"]

        ctk.CTkLabel(
            card, text="Заболевание",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.combo_disease = ctk.CTkComboBox(
            card, values=disease_names,
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.combo_disease.pack(pady=(0, 15))

        # Дата начала
        ctk.CTkLabel(
            card, text="Дата начала",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_start = ctk.CTkEntry(
            card, placeholder_text="дд.мм.гггг",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_start.pack(pady=(0, 15))

        # Дата окончания
        ctk.CTkLabel(
            card, text="Дата окончания (необязательно)",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_end = ctk.CTkEntry(
            card, placeholder_text="дд.мм.гггг",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_end.pack(pady=(0, 15))

        # Статус
        ctk.CTkLabel(
            card, text="Статус",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.combo_status = ctk.CTkComboBox(
            card, values=["Активно", "Вылечено", "Хроническое"],
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.combo_status.pack(pady=(0, 15))

        # Лечение
        ctk.CTkLabel(
            card, text="Лечение",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=40)
        self.entry_treatment = ctk.CTkEntry(
            card, placeholder_text="Назначенное лечение",
            width=400, height=42, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_treatment.pack(pady=(0, 20))

                # Enter в полях — сохранить
        for entry in (self.entry_start, self.entry_end, self.entry_treatment):
            entry.bind("<Return>", lambda e: self._save())

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
        """Сохраняет запись о болезни в БД и вызывает on_save."""
        disease_name = self.combo_disease.get().strip()
        date_start = self.entry_start.get().strip()
        date_end = self.entry_end.get().strip() or None
        status_ru = self.combo_status.get().strip()
        treatment = self.entry_treatment.get().strip() or None

        if not date_start:
            messagebox.showerror("Ошибка", "Заполните дату начала")
            return

        # Ищем ID заболевания в справочнике по названию
        diseases = self.db.get_diseases()
        disease_id = None
        for d in diseases:
            if d[1] == disease_name:
                disease_id = d[0]
                break

        if disease_id is None:
            messagebox.showerror(
                "Ошибка",
                "Заболевание не найдено в справочнике. "
                "Добавьте его в справочник сначала."
            )
            return

        # Преобразуем русский статус в код для БД
        status_map = {
            "Активно": "активно",
            "Вылечено": "вылечено",
            "Хроническое": "хроническое",
        }
        status = status_map.get(status_ru, "активно")

        self.db.add_pet_disease(
            self.pet_id, disease_id, date_start,
            date_end, status, treatment
        )
        self.on_save()
        self.destroy()