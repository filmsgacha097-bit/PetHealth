"""Экран восстановления пароля приложения PetHealth.

Восстановление проходит в три шага:
1. Пользователь вводит логин.
2. Отвечает на секретный вопрос.
3. Вводит новый пароль.

Это учебная (демонстрационная) авторизация — без хранения
паролей в базе данных, в соответствии с ТЗ.
"""

import customtkinter as ctk
from tkinter import messagebox

from ui.icons import create_logo
from ui import auth


class ResetPasswordFrame(ctk.CTkFrame):
    """Экран восстановления пароля.

    Attributes:
        on_back (callable): Функция возврата на экран авторизации.
    """

    def __init__(self, master, on_back) -> None:
        """Инициализация экрана восстановления пароля.

        Args:
            master: Родительское окно (PetHealthApp).
            on_back (callable): Функция возврата на авторизацию.
        """
        super().__init__(master, fg_color="#F7F4EB")
        self.on_back = on_back

        # Шаг восстановления: 1 — логин, 2 — ответ, 3 — новый пароль
        self.step = 1
        self.verified_login = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Строит интерфейс экрана восстановления."""
        # Карточка по центру
        self.card = ctk.CTkFrame(
            self, fg_color="#FFFFFF", corner_radius=24,
            width=440, height=620
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        # Логотип
        create_logo(
            self.card, "PetHealth", size=36,
            text_color="#FEB2B1", font_size=32
        ).pack(pady=(30, 5))

        # Контент (меняется в зависимости от шага)
        self.content = ctk.CTkFrame(self.card, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=40)

        self._build_step_1()

    def _clear_content(self) -> None:
        """Очищает содержимое карточки."""
        for widget in self.content.winfo_children():
            widget.destroy()

    def _build_step_1(self) -> None:
        """Шаг 1: ввод логина."""
        self._clear_content()

        ctk.CTkLabel(
            self.content, text="Восстановление пароля",
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.content, text="Введите логин от аккаунта",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self.content, text="Логин",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w")
        self.entry_login = ctk.CTkEntry(
            self.content, placeholder_text="Введите логин",
            width=320, height=44, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_login.pack(pady=(0, 20))
        self.entry_login.bind("<Return>", lambda e: self._check_login())

        ctk.CTkButton(
            self.content, text="Далее", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self._check_login
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            self.content, text="← Назад", width=320, height=40,
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self.on_back
        ).pack()

    def _check_login(self) -> None:
        """Проверяет логин и переходит к секретному вопросу."""
        login = self.entry_login.get().strip()
        if not login:
            messagebox.showerror("Ошибка", "Введите логин")
            return
        if login != auth.CURRENT_LOGIN:
            messagebox.showerror("Ошибка", "Пользователь с таким логином не найден")
            return
        self.verified_login = login
        self._build_step_2()

    def _build_step_2(self) -> None:
        """Шаг 2: ответ на секретный вопрос."""
        self._clear_content()

        ctk.CTkLabel(
            self.content, text="Секретный вопрос",
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(pady=(10, 20))

        ctk.CTkLabel(
            self.content, text=auth.get_secret_question(),
            font=("Nunito", 13), text_color="#8A8A8A",
            wraplength=320, justify="center"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self.content, text="Ответ",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w")
        self.entry_answer = ctk.CTkEntry(
            self.content, placeholder_text="Введите ответ",
            width=320, height=44, fg_color="#F7F4EB",
            border_color="#BBE6FA", corner_radius=12
        )
        self.entry_answer.pack(pady=(0, 20))
        self.entry_answer.bind("<Return>", lambda e: self._check_secret())

        ctk.CTkButton(
            self.content, text="Проверить", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self._check_secret
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            self.content, text="← Назад", width=320, height=40,
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self._build_step_1
        ).pack()

    def _check_secret(self) -> None:
        """Проверяет ответ на секретный вопрос."""
        answer = self.entry_answer.get().strip()
        if not answer:
            messagebox.showerror("Ошибка", "Введите ответ")
            return
        if not auth.check_secret(self.verified_login, answer):
            messagebox.showerror("Ошибка", "Неверный ответ на секретный вопрос")
            return
        self._build_step_3()

    def _build_step_3(self) -> None:
        """Шаг 3: ввод нового пароля."""
        self._clear_content()

        ctk.CTkLabel(
            self.content, text="Новый пароль",
            font=("Nunito", 18, "bold"), text_color="#333333"
        ).pack(pady=(10, 20))

        ctk.CTkLabel(
            self.content, text="Придумайте новый пароль",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            self.content, text="Новый пароль",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w")
        self.entry_new = ctk.CTkEntry(
            self.content, placeholder_text="Новый пароль",
            show="*", width=320, height=44,
            fg_color="#F7F4EB", border_color="#BBE6FA", corner_radius=12
        )
        self.entry_new.pack(pady=(0, 15))

        ctk.CTkLabel(
            self.content, text="Повторите пароль",
            font=("Nunito", 12), text_color="#8A8A8A"
        ).pack(anchor="w")
        self.entry_new2 = ctk.CTkEntry(
            self.content, placeholder_text="Повторите пароль",
            show="*", width=320, height=44,
            fg_color="#F7F4EB", border_color="#BBE6FA", corner_radius=12
        )
        self.entry_new2.pack(pady=(0, 20))
        self.entry_new2.bind("<Return>", lambda e: self._save_new_password())

        ctk.CTkButton(
            self.content, text="Сохранить", width=320, height=44,
            fg_color="#FEB2B1", hover_color="#FFB1CB",
            text_color="#FFFFFF", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self._save_new_password
        ).pack(pady=(0, 15))

        ctk.CTkButton(
            self.content, text="← Назад", width=320, height=40,
            fg_color="#F7F4EB", border_color="#BBE6FA", border_width=1,
            text_color="#333333", font=("Nunito", 12, "bold"),
            corner_radius=12, command=self._build_step_2
        ).pack()

    def _save_new_password(self) -> None:
        """Сохраняет новый пароль и возвращает на авторизацию."""
        new_pass = self.entry_new.get().strip()
        new_pass2 = self.entry_new2.get().strip()

        if not new_pass or not new_pass2:
            messagebox.showerror("Ошибка", "Заполните оба поля")
            return
        if new_pass != new_pass2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        if len(new_pass) < 4:
            messagebox.showerror("Ошибка", "Пароль должен быть не короче 4 символов")
            return

        auth.reset_password(new_pass)
        messagebox.showinfo(
            "Готово",
            "Пароль успешно изменён.\nВойдите с новым паролем."
        )
        self.on_back()