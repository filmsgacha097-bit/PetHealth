"""Экран авторизации приложения PetHealth.

Содержит класс LoginFrame — экран входа в систему.
Авторизация учебная (демонстрационная): логин и пароль
проверяются по константам в коде, без хранения в БД.

Это фрейм (CTkFrame), который встраивается в главное окно
PetHealthApp и переключается через него.
"""

import customtkinter as ctk
from tkinter import messagebox
from ui.lottie_label import LottieLabel


# Учебные учётные данные (демонстрация авторизации)
DEMO_LOGIN = "admin"
DEMO_PASSWORD = "admin"


class LoginFrame(ctk.CTkFrame):
    """Экран авторизации пользователя.

    Встраивается в главное окно. После успешного входа
    вызывается callback on_login, который переключает экран.

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
        # Карточка по центру
        card = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=24,
            width=440, height=520
        )   
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Заголовок
        ctk.CTkLabel(
            card, text="🐾 PetHealth",
            font=("Nunito", 32, "bold"), text_color="#FEB2B1"
        ).pack(pady=(40, 5))

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
        self.entry_password.pack(pady=(0, 25))

        # Enter в любом поле — вход
        self.entry_login.bind("<Return>", lambda e: self._login())
        self.entry_password.bind("<Return>", lambda e: self._login())

        # Кнопка "Войти"
        ctk.CTkButton(
            card, text="Войти", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 14, "bold"),
            corner_radius=12, command=self._login
        ).pack(pady=(0, 15))

        # Ссылка "Зарегистрироваться"
        self.link_register = ctk.CTkLabel(
            card, text="Нет аккаунта? Зарегистрироваться",
            font=("Nunito", 12), text_color="#BBE6FA", cursor="hand2"
        )
        self.link_register.pack(pady=(0, 30))
        self.link_register.bind(
            "<Button-1>",
            lambda e: self.master.show_register()
        )

    def _login(self) -> None:
        """Проверяет логин и пароль. При успехе вызывает on_login."""
        login = self.entry_login.get().strip()
        password = self.entry_password.get().strip()

        if not login or not password:
            messagebox.showerror("Ошибка", "Заполните логин и пароль")
            return

        if login == DEMO_LOGIN and password == DEMO_PASSWORD:
            self.on_login()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")