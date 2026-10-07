"""Экран напоминаний о предстоящих процедурах.

Содержит класс RemindersFrame — экран со списком предстоящих
процедур на ближайшие 7 дней.
"""

import customtkinter as ctk


class RemindersFrame(ctk.CTkFrame):
    """Экран напоминаний.

    Отображает список предстоящих процедур (вакцинации, обработки,
    взвешивания) на основе поля next_date в таблице records.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        on_back (callable): Функция возврата на главный экран.
    """

    def __init__(self, master, db, on_back) -> None:
        """Инициализация экрана напоминаний.

        Args:
            master: Родительское окно (PetHealthApp).
            db (DatabaseManager): Менеджер базы данных.
            on_back (callable): Функция возврата на главный экран.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.db = db
        self.on_back = on_back

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс экрана напоминаний."""
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            top_bar, text="← Назад",
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=120, height=40, command=self.on_back
        ).pack(side="left")

        ctk.CTkLabel(
            self, text="🔔 Все напоминания",
            font=("Nunito", 24, "bold"), text_color="#333333"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self, text="Предстоящие процедуры на ближайшие 7 дней",
            font=("Nunito", 13), text_color="#8A8A8A"
        ).pack(pady=(0, 15))

        # Список напоминаний
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self._refresh()

    def _refresh(self) -> None:
        """Обновляет список напоминаний."""
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        reminders = self.db.get_upcoming_procedures(days=7)

        if not reminders:
            ctk.CTkLabel(
                self.list_frame,
                text="Нет предстоящих процедур на ближайшие 7 дней",
                font=("Nunito", 14), text_color="#8A8A8A"
            ).pack(pady=30)
            return

        for reminder in reminders:
            self._create_reminder_card(reminder)

    def _create_reminder_card(self, reminder: tuple) -> None:
        """Создаёт карточку напоминания.

        Args:
            reminder (tuple): Кортеж из БД:
                (pet_name, pet_species, record_type, next_date, value).
        """
        pet_name, pet_species, record_type, next_date, value = reminder

        emoji_map = {
            "vaccine": "💉",
            "parasite": "💊",
            "weight": "⚖️",
            "note": "📝",
        }
        emoji = emoji_map.get(record_type, "📌")

        type_ru = {
            "vaccine": "Вакцинация",
            "parasite": "Обработка",
            "weight": "Взвешивание",
            "note": "Заметка",
        }
        type_label = type_ru.get(record_type, record_type)

        card = ctk.CTkFrame(
            self.list_frame, fg_color="#FFFFFF",
            corner_radius=16
        )
        card.pack(fill="x", pady=8, padx=5)

        # Левая часть — эмодзи
        ctk.CTkLabel(
            card, text=emoji, font=("Nunito", 32),
            width=70, height=70, fg_color="#FFEF77",
            corner_radius=16
        ).pack(side="left", padx=15, pady=15)

        # Центральная часть — информация
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, pady=15)

        ctk.CTkLabel(
            info_frame, text=f"{pet_name} ({pet_species})",
            font=("Nunito", 16, "bold"), text_color="#333333"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame, text=f"{type_label}: {value or '—'}",
            font=("Nunito", 13), text_color="#8A8A8A"
        ).pack(anchor="w")

        # Правая часть — дата
        ctk.CTkLabel(
            card, text=f"📅 {next_date}",
            font=("Nunito", 14, "bold"), text_color="#FEB2B1"
        ).pack(side="right", padx=20)