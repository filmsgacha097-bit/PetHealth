"""Экран справочника заболеваний.

Содержит класс CatalogFrame — экран со списком всех заболеваний
из справочника. Позволяет добавлять новые заболевания.
"""

import customtkinter as ctk

from ui.add_disease_to_catalog_dialog import AddDiseaseToCatalogDialog
import sys

class CatalogFrame(ctk.CTkFrame):
    """Экран справочника заболеваний.

    Отображает список заболеваний с описанием и видом животного.
    Позволяет добавить новое заболевание в справочник.

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        on_back (callable): Функция возврата на главный экран.
    """

    def __init__(self, master, db, on_back) -> None:
        """Инициализация экрана справочника.

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
        """Строит интерфейс справочника заболеваний."""
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            top_bar, text="← Назад",
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=120, height=40, command=self.on_back
        ).pack(side="left")

        ctk.CTkLabel(
            self, text="Справочник заболеваний",
            font=("Nunito", 24, "bold"), text_color="#333333"
        ).pack(pady=(10, 5))

        ctk.CTkButton(
            self, text="+ Добавить заболевание",
            fg_color="#FFEF77", hover_color="#FFE055",
            text_color="#333333", font=("Nunito", 12, "bold"),
            width=220, height=40, corner_radius=12,
            command=self._open_add_dialog
        ).pack(pady=(5, 15))

        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=30, pady=10)

        self._refresh()

    def _bind_mousewheel(self, widget) -> None:
        """Привязывает колёсико мыши к виджету и всем его дочерним элементам.

        Args:
            widget: Виджет, для которого нужно включить скролл.
        """
        # Windows / macOS
        widget.bind("<MouseWheel>", self._on_mousewheel)
        # Linux
        widget.bind("<Button-4>", lambda e: self._scroll(-1))
        widget.bind("<Button-5>", lambda e: self._scroll(1))

        # Рекурсивно для всех дочерних
        for child in widget.winfo_children():
            self._bind_mousewheel(child)

    def _on_mousewheel(self, event) -> None:
        """Обработчик колёсика для Windows/macOS."""
        self.list_frame._parent_canvas.yview_scroll(
            int(-1 * (event.delta / 120)), "units"
        )

    def _scroll(self, direction: int) -> None:
        """Обработчик колёсика для Linux.

        Args:
            direction (int): -1 вверх, 1 вниз.
        """
        self.list_frame._parent_canvas.yview_scroll(direction, "units")

    def _refresh(self) -> None:
        """Обновляет список заболеваний."""
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        diseases = self.db.get_diseases()

        if not diseases:
            ctk.CTkLabel(
                self.list_frame,
                text="Справочник пуст. Добавьте первое заболевание!",
                font=("Nunito", 14), text_color="#8A8A8A"
            ).pack(pady=30)
            return

        for disease in diseases:
            self._create_disease_card(disease)
                    # Привязываем скролл ко всем элементам
        self._bind_mousewheel(self.list_frame)

    def _create_disease_card(self, disease: tuple) -> None:
        """Создаёт карточку заболевания в списке.

        Args:
            disease (tuple): Кортеж из БД: (id, name, description, species).
        """
        dis_id, name, description, species = disease

        card = ctk.CTkFrame(
            self.list_frame, fg_color="#FFFFFF",
            corner_radius=16, height=110
        )
        card.pack(fill="x", pady=8, padx=5)
        card.pack_propagate(False)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        ctk.CTkLabel(
            info_frame, text=f"🩺 {name}",
            font=("Nunito", 16, "bold"), text_color="#333333"
        ).pack(anchor="w")

        if description:
            ctk.CTkLabel(
                info_frame, text=description,
                font=("Nunito", 12), text_color="#8A8A8A"
            ).pack(anchor="w")

        if species:
            ctk.CTkLabel(
                info_frame, text=f"Вид: {species}",
                font=("Nunito", 11), text_color="#BBE6FA"
            ).pack(anchor="w")

    def _open_add_dialog(self) -> None:
        """Открывает диалог добавления заболевания в справочник."""
        AddDiseaseToCatalogDialog(self, self.db, on_save=self._refresh)