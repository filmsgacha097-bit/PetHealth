"""Экран авторизации приложения PetHealth.

Содержит класс LoginFrame — экран входа в систему.
Авторизация учебная (демонстрационная): логин и пароль
проверяются через модуль auth.
"""

import customtkinter as ctk
from tkinter import messagebox

from ui.lottie_label import LottieLabel
from ui.icons import create_logo
from ui import auth


class LoginFrame(ctk.CTkFrame):
    """Экран авторизации пользователя.

    Attributes:
        on_login (callable): Функция, вызываемая после успешного входа.
    """

    def __init__(self, master, on_login) -> None:
        """Инициализация экрана авторизации.

        Args:
            master: Родительское окно (PetHealthApp).
            on_login (callable): Функция перехода на главный экран.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.on_login = on_login

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс формы авторизации."""
        card = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=24,
            width=440, height=650
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Логотип
        create_logo(
            card, "PetHealth", size=36,
            text_color="#FEB2B1", font_size=32
        ).pack(pady=(30, 5))

        # Подзаголовок
        ctk.CTkLabel(
            card, text="Войдите в свой аккаунт",
            font=("Nunito", 14), text_color="#8A8A8A"
        ).pack(pady=(0, 10))

        # Lottie-анимация
        try:
            lottie = LottieLabel(
                card, "assets/pet_animation.json",
                size=(150, 150), duration=50
            )
            lottie.pack(pady=(0, 15))
        except Exception:
            pass

        # Поле "Логин"
        ctk.CTkLabel(
            card, text="Логин",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w", padx=60)
        self.entry_login = ctk.CTkEntry(
            card, placeholder_text="Введите логин",
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
            card, placeholder_text="Введите пароль",
            show="*", width=320, height=44,
            fg_color="#F7F4EB", border_color="#BBE6FA", corner_radius=12
        )
        self.entry_password.pack(pady=(0, 20))

        # Enter в любом поле — вход
        self.entry_login.bind("<Return>", lambda e: self._login())
        self.entry_password.bind("<Return>", lambda e: self._login())

        # Кнопка "Войти"
        ctk.CTkButton(
            card, text="Войти", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 14, "bold"),
            corner_radius=12, command=self._login
        ).pack(pady=(0, 12))

        # Ссылка "Забыли пароль?"
        link_forgot = ctk.CTkLabel(
            card, text="Забыли пароль?",
            font=("Nunito", 12), text_color="#FFB1CB", cursor="hand2"
        )
        link_forgot.pack()
        link_forgot.bind(
            "<Button-1>",
            lambda e: self.master.show_reset_password()
        )

        # Ссылка "Зарегистрироваться"
        link_register = ctk.CTkLabel(
            card, text="Нет аккаунта? Зарегистрироваться",
            font=("Nunito", 12), text_color="#BBE6FA", cursor="hand2"
        )
        link_register.pack(pady=(10, 20))
        link_register.bind(
            "<Button-1>",
            lambda e: self.master.show_register()
        )

    def _login(self) -> None:
        """Проверяет логин и пароль через auth."""
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()

        if not login or not password:
            messagebox.showerror("Ошибка", "Заполните логин и пароль")
            return

        if auth.check_login(login, password):
            self.on_login()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")