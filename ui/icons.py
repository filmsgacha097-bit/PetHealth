"""Загрузчик иконок для приложения PetHealth.

Загружает PNG-иконки питомцев и других элементов из папки assets/icons.
Кэширует загруженные иконки, чтобы не загружать одну и ту же иконку дважды.
"""

import os
import customtkinter as ctk
from PIL import Image


# Путь к папке с иконками
ICONS_DIR = "assets/icons"

# Кэш загруженных иконок
_cache = {}


def get_icon(name: str, size: int = 48) -> ctk.CTkImage:
    """Загружает иконку по имени.

    Args:
        name (str): Имя иконки без расширения (например, "cat").
        size (int): Размер иконки в пикселях.

    Returns:
        ctk.CTkImage: Иконка для использования в интерфейсе.
        Если файл не найден — возвращает None.
    """
    key = f"{name}_{size}"
    if key in _cache:
        return _cache[key]

    path = os.path.join(ICONS_DIR, f"{name}.png")
    if not os.path.exists(path):
        return None

    pil_image = Image.open(path).convert("RGBA")
    ctk_image = ctk.CTkImage(
        light_image=pil_image,
        dark_image=pil_image,
        size=(size, size)
    )
    _cache[key] = ctk_image
    return ctk_image


def get_species_icon(species: str, size: int = 48) -> ctk.CTkImage:
    """Возвращает иконку по виду животного.

    Args:
        species (str): Название вида (например, "Кошка").
        size (int): Размер иконки.

    Returns:
        ctk.CTkImage: Иконка питомца.
    """
    species_lower = species.lower()

    if "кош" in species_lower or "кот" in species_lower:
        icon_name = "cat"
    elif "собак" in species_lower or "пёс" in species_lower or "пес" in species_lower:
        icon_name = "dog"
    elif "грызун" in species_lower or "хомяк" in species_lower or "мыш" in species_lower:
        icon_name = "hamster"
    elif "попугай" in species_lower or "птиц" in species_lower:
        icon_name = "parrot"
    else:
        icon_name = "pet"

    return get_icon(icon_name, size=size)


def create_logo(master, text: str = "PetHealth",
                size: int = 32, text_color: str = "#FEB2B1",
                font_size: int = 24) -> ctk.CTkFrame:
    """Создаёт логотип: иконка лапки + название.

    Args:
        master: Родительский виджет.
        text (str): Текст логотипа.
        size (int): Размер иконки.
        text_color (str): Цвет текста.
        font_size (int): Размер шрифта.

    Returns:
        ctk.CTkFrame: Фрейм с иконкой и текстом.
    """
    frame = ctk.CTkFrame(master, fg_color="transparent")

    icon = get_icon("pet", size=size)
    if icon:
        icon_label = ctk.CTkLabel(frame, text="", image=icon)
        icon_label.pack(side="left", padx=(0, 8))

    text_label = ctk.CTkLabel(
        frame, text=text,
        font=("Nunito", font_size, "bold"),
        text_color=text_color
    )
    text_label.pack(side="left")

    return frame