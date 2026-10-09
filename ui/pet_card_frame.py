"""Экран карточки питомца.

Содержит класс PetCardFrame — экран с подробной информацией
о питомце: фото, кличка, вид, дата рождения, записи о здоровье,
история болезней.

Это фрейм (CTkFrame), который встраивается в главное окно
PetHealthApp и переключается через него.
"""
import os
import sys
import subprocess

import customtkinter as ctk
from tkinter import messagebox

from ui.add_record_dialog import AddRecordDialog
from ui.add_disease_dialog import AddDiseaseDialog

from ui.icons import get_species_icon
from utils.print_pet import generate_pet_pdf


class PetCardFrame(ctk.CTkFrame):
    """Экран карточки питомца.

    Отображает информацию о питомце и предоставляет доступ
    к записям о здоровье и истории болезней.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        pet_id (int): ID питомца.
        on_back (callable): Функция возврата на главный экран.
    """

    def __init__(self, master, db, pet_id: int, on_back) -> None:
        """Инициализация экрана карточки питомца.

        Args:
            master: Родительское окно (PetHealthApp).
            db (DatabaseManager): Менеджер базы данных.
            pet_id (int): ID питомца.
            on_back (callable): Функция возврата на главный экран.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.db = db
        self.pet_id = pet_id
        self.on_back = on_back

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс карточки питомца."""
        pets = self.db.get_all_pets()
        pet = None
        for p in pets:
            if p[0] == self.pet_id:
                pet = p
                break

        if pet is None:
            ctk.CTkLabel(
                self, text="Питомец не найден",
                font=("Nunito", 20), text_color="#333333"
            ).pack(pady=50)
            return

        pet_id, name, species, birth_date, photo_path, notes = pet

        # Верхняя панель с кнопкой "Назад"
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            top_bar, text="← Назад",
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=120, height=40, command=self.on_back
        ).pack(side="left")

        # Основная область — две колонки
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)

        # ===== Левая колонка — информация о питомце =====
        left = ctk.CTkFrame(
            content, fg_color="#FFFFFF", corner_radius=24, width=380
        )
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        icon = get_species_icon(species, size=128)

        ctk.CTkLabel(
            left, text="",
            width=160, height=160, fg_color="#BBE6FA",
            corner_radius=24, image=icon
        ).pack(pady=(30, 15))

        ctk.CTkLabel(
            left, text=name,
            font=("Nunito", 28, "bold"), text_color="#333333"
        ).pack()

        ctk.CTkLabel(
            left, text=species,
            font=("Nunito", 16), text_color="#8A8A8A"
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            left, text=f"Дата рождения: {birth_date or '—'}",
            font=("Nunito", 14), text_color="#333333"
        ).pack()

        ctk.CTkLabel(
            left, text=f"Заметки: {notes or '—'}",
            font=("Nunito", 14), text_color="#8A8A8A",
            wraplength=340, justify="center"
        ).pack(pady=(0, 20))

                # Кнопки внизу левой колонки
        buttons_frame = ctk.CTkFrame(left, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))

        ctk.CTkButton(
            buttons_frame, text="Распечатать",
            fg_color="#FFEF77", hover_color="#FFE055",
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=180, height=40, command=self._print_pet
        ).pack(pady=(0, 8))

        ctk.CTkButton(
            buttons_frame, text="Удалить питомца",
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            width=180, height=40, command=self._delete_pet
        ).pack()

        # ===== Правая колонка — записи и болезни =====
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        # --- Записи о здоровье ---
        records_card = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=24)
        records_card.pack(fill="both", expand=True, pady=(0, 10))

        records_header = ctk.CTkFrame(records_card, fg_color="transparent")
        records_header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            records_header, text="Записи о здоровье",
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(side="left")

        ctk.CTkButton(
            records_header, text="+ Добавить запись",
            fg_color="#FFEF77", hover_color="#FFE055",
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=160, height=36,
            command=self._open_add_record
        ).pack(side="right")

        records = self.db.get_records(self.pet_id)
        if not records:
            ctk.CTkLabel(
                records_card, text="Записей пока нет",
                font=("Nunito", 14), text_color="#8A8A8A"
            ).pack(pady=20)
        else:
            for rec in records:
                self._create_record_row(records_card, rec)

        # --- История болезней ---
        diseases_card = ctk.CTkFrame(right, fg_color="#FFFFFF", corner_radius=24)
        diseases_card.pack(fill="both", expand=True, pady=(10, 0))

        diseases_header = ctk.CTkFrame(diseases_card, fg_color="transparent")
        diseases_header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            diseases_header, text="История болезней",
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(side="left")

        ctk.CTkButton(
            diseases_header, text="+ Добавить заболевание",
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            width=200, height=36,
            command=self._open_add_disease
        ).pack(side="right")

        pet_diseases = self.db.get_pet_diseases(self.pet_id)
        if not pet_diseases:
            ctk.CTkLabel(
                diseases_card, text="Заболеваний пока нет",
                font=("Nunito", 14), text_color="#8A8A8A"
            ).pack(pady=20)
        else:
            for pd in pet_diseases:
                self._create_disease_row(diseases_card, pd)

    def _create_record_row(self, parent, record: tuple) -> None:
        """Создаёт строку с записью о здоровье.

        Args:
            parent: Родительский фрейм.
            record (tuple): Кортеж из БД.
        """
        rec_id, _, rec_type, date, value, next_date = record

        row = ctk.CTkFrame(parent, fg_color="#F7F4EB", corner_radius=10, height=50)
        row.pack(fill="x", padx=20, pady=4)
        row.pack_propagate(False)

        emoji_map = {
            "vaccine": "💉",
            "parasite": "💊",
            "weight": "⚖️",
            "note": "📝",
        }
        emoji = emoji_map.get(rec_type, "📌")

        ctk.CTkLabel(
            row, text=f"{emoji} {rec_type}: {value or '—'} — {date}",
            font=("Nunito", 13), text_color="#333333"
        ).pack(side="left", padx=15)

    def _create_disease_row(self, parent, pd: tuple) -> None:
        """Создаёт строку с записью о болезни.

        Args:
            parent: Родительский фрейм.
            pd (tuple): Кортеж из БД.
        """
        pd_id, _, disease_id, date_start, date_end, status, treatment, notes = pd

        row = ctk.CTkFrame(parent, fg_color="#F7F4EB", corner_radius=10, height=50)
        row.pack(fill="x", padx=20, pady=4)
        row.pack_propagate(False)

        ctk.CTkLabel(
            row, text=f"🩺 Болезнь #{disease_id} — {date_start} — {status}",
            font=("Nunito", 13), text_color="#333333"
        ).pack(side="left", padx=15)

        ctk.CTkLabel(
            row, text=treatment or "—",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(side="right", padx=15)

    def _open_add_record(self) -> None:
        """Открывает диалог добавления записи о здоровье."""
        AddRecordDialog(
            self, self.db, self.pet_id,
            on_save=self._refresh
        )

    def _refresh(self) -> None:
        """Обновляет экран карточки питомца (после изменений)."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()

    def _open_add_disease(self) -> None:
        """Открывает диалог добавления заболевания."""
        AddDiseaseDialog(
            self, self.db, self.pet_id,
            on_save=self._refresh
        )

    def _delete_pet(self) -> None:
        """Удаляет питомца после подтверждения и возвращает на главный экран."""
        if messagebox.askyesno("Подтверждение", "Удалить питомца?"):
            self.db.delete_pet(self.pet_id)
            self.on_back()
    
    def _print_pet(self) -> None:
        """Создаёт PDF-отчёт о питомце и открывает его."""
        try:
            path = generate_pet_pdf(self.db, self.pet_id)
            messagebox.showinfo(
                "Готово",
                f"PDF-отчёт сохранён:\n{path}"
            )
            # Пытаемся открыть PDF системным просмотрщиком
            try:
                if os.name == "nt":  # Windows
                    os.startfile(path)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", path], check=False)
                else:  # Linux
                    subprocess.run(["xdg-open", path], check=False)
            except Exception:
                pass  # Если не удалось открыть — не критично
        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось создать PDF:\n{e}"
            )