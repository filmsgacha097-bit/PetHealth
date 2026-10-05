"""Точка входа приложения PetHealth.

Запускает единое окно приложения PetHealthApp,
внутри которого переключаются экраны:
авторизация → главный экран → карточка питомца и т.д.
"""

from ui.app import PetHealthApp


def main() -> None:
    """Запускает приложение PetHealth."""
    app = PetHealthApp()
    app.mainloop()


if __name__ == "__main__":
    main()