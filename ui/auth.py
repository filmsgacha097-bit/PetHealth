"""Учебная авторизация PetHealth.

Хранит логин, пароль и секретный вопрос в памяти.
Пароль можно изменить через функцию reset_password.
"""

CURRENT_LOGIN = "admin"
CURRENT_PASSWORD = "admin"
SECRET_QUESTION = "Кличка вашего первого питомца?"
SECRET_ANSWER = "мурка"


def check_login(login: str, password: str) -> bool:
    """Проверяет логин и пароль."""
    return login == CURRENT_LOGIN and password == CURRENT_PASSWORD


def check_secret(login: str, answer: str) -> bool:
    """Проверяет логин и ответ на секретный вопрос."""
    return login == CURRENT_LOGIN and answer.strip().lower() == SECRET_ANSWER.lower()


def reset_password(new_password: str) -> None:
    """Сбрасывает пароль."""
    global CURRENT_PASSWORD
    CURRENT_PASSWORD = new_password


def get_secret_question() -> str:
    """Возвращает секретный вопрос.

    Returns:
        str: Текст секретного вопроса.
    """
    return SECRET_QUESTION