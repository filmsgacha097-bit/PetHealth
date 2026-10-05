"""Экран регистрации приложения PetHealth.

Содержит класс RegisterFrame — экран создания нового аккаунта.
Регистрация учебная (демонстрационная): данные не сохраняются в БД.

Это фрейм (CTkFrame), который встраивается в главное окно
PetHealthApp и переключается через него.
"""

import customtkinter as ctk
from tkinter import messagebox


class RegisterFrame(ctk.CTkFrame):
    """Экран регистрации нового пользователя.

    Встраивается в главное окно. По кнопке «Уже есть аккаунт? Войти»
    вызывается callback on_back, который возвращает на экран авторизации.

    Attributes:
        on_back (callable): Функция возврата на экран авторизации.
    """

    def __init__(self, master, on_back) -> None:
        """Инициализация экрана регистрации.

        Args:
            master: Родительское окно (PetHealthApp).
            on_back (callable): Функция возврата на экран авторизации.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.on_back = on_back

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы регистрации."""
        # Карточка по центру
        card = ctk.CTkFrame(
        self, fg_color="#FFFFFF", corner_radius=24,
        width=440, height=580
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Заголовок
        ctk.CTkLabel(
            card, text="🐾 PetHealth",
            font=("Nunito", 32, "bold"), text_color="#FEB2B1"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            card, text="Создайте новый аккаунт",
            font=("Nunito", 14), text_color="#8A8A8A"
        ).pack(pady=(0, 20))

        # Поле "Логин"
        ctk.CTkLabel(
            card, text="Логин",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=60)
        self.entry_login = ctk.CTkEntry(
            card, placeholder_text="Придумайте логин",
            width=320, height=44, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_login.pack(pady=(0, 15))

        # Поле "Пароль"
        ctk.CTkLabel(
            card, text="Пароль",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=60)
        self.entry_password = ctk.CTkEntry(
            card, placeholder_text="Придумайте пароль",
            show="*", width=320, height=44,
            fg_color="#F7F4EB", border_color="#BBE6FA", corner_radius=12
        )
        self.entry_password.pack(pady=(0, 15))

        # Поле "Повторите пароль"
        ctk.CTkLabel(
            card, text="Повторите пароль",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=60)
        self.entry_password2 = ctk.CTkEntry(
            card, placeholder_text="Повторите пароль",
            show="*", width=320, height=44,
            fg_color="#F7F4EB", border_color="#BBE6FA", corner_radius=12
        )
        self.entry_password2.pack(pady=(0, 25))

        # Кнопка "Зарегистрироваться"
        ctk.CTkButton(
            card, text="Зарегистрироваться", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 14, "bold"),
            corner_radius=12, command=self._do_register
        ).pack(pady=(0, 15))

        # Ссылка "Уже есть аккаунт? Войти"
        link_login = ctk.CTkLabel(
            card, text="Уже есть аккаунт? Войти",
            font=("Nunito", 12), text_color="#BBE6FA", cursor="hand2"
        )
        link_login.pack(pady=(0, 30))
        link_login.bind("<Button-1>", lambda e: self.on_back())

    def _do_register(self) -> None:
        """Проверяет корректность данных и «регистрирует» пользователя."""
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()
        password2 = self.entry_password2.get().strip()

        if not login or not password or not password2:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        if password != password2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return

        messagebox.showinfo(
            "Успех",
            "Регистрация прошла успешно!\nТеперь войдите с этими данными."
        )
        self.on_back()