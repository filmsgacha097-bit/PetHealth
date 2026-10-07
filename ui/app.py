"""Главное окно приложения PetHealth.

Содержит класс PetHealthApp — единое окно, внутри которого
переключаются экраны (фреймы): авторизация, регистрация,
главный экран, карточка питомца и т.д.

Реализует паттерн MVC: приложение — контроллер,
фреймы — представления, DatabaseManager — модель.
"""

import customtkinter as ctk
from database_manager import DatabaseManager


class PetHealthApp(ctk.CTk):
    """Главное окно приложения PetHealth.

    Единое окно, внутри которого переключаются экраны-фреймы.
    Отвечает за навигацию между экранами и хранит общие ресурсы
    (менеджер базы данных, текущего пользователя).

    Attributes:
        db (DatabaseManager): Менеджер базы данных.
        current_frame (ctk.CTkFrame): Текущий отображаемый экран.
    """

    def __init__(self) -> None:
        """Инициализация главного окна приложения."""
        super().__init__()

        self.title("PetHealth")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.configure(fg_color="#F7F4EB")

        # Менеджер базы данных — общий для всего приложения
        self.db = DatabaseManager("pets.db")

        # Текущий фрейм
        self.current_frame = None

        # Показываем экран авторизации
        self.show_login()

    def show_frame(self, frame_class, **kwargs) -> None:
        """Универсальный метод переключения экранов.

        Удаляет текущий фрейм и создаёт новый.

        Args:
            frame_class: Класс фрейма для отображения.
            **kwargs: Параметры, передаваемые во фрейм.
        """
        # Удаляем текущий фрейм
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Создаём новый фрейм
        self.current_frame = frame_class(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self) -> None:
        """Показывает экран авторизации."""
        from ui.login_frame import LoginFrame
        self.show_frame(LoginFrame, on_login=self.show_main)

    def show_register(self) -> None:
        """Показывает экран регистрации."""
        from ui.register_frame import RegisterFrame
        self.show_frame(RegisterFrame, on_back=self.show_login)

    def show_main(self) -> None:
        """Показывает главный экран со списком питомцев."""
        from ui.main_frame import MainFrame
        self.show_frame(MainFrame, db=self.db, on_logout=self.show_login)
    
    def show_pet_card(self, pet_id: int) -> None:
        """Показывает карточку питомца.

        Args:
            pet_id (int): ID питомца.
        """
        from ui.pet_card_frame import PetCardFrame
        self.show_frame(
            PetCardFrame,
            db=self.db,
            pet_id=pet_id,
            on_back=self.show_main
        )

    def show_catalog(self) -> None:
        """Показывает справочник заболеваний."""
        from ui.catalog_frame import CatalogFrame
        self.show_frame(CatalogFrame, db=self.db, on_back=self.show_main)
        
    def on_close(self) -> None:
        """Корректное закрытие приложения."""
        self.db.close()
        self.destroy()