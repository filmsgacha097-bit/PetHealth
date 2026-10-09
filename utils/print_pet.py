"""Модуль формирования PDF-отчёта о питомце.

Содержит функцию generate_pet_pdf, которая создаёт PDF-файл
с полной информацией о питомце: основные данные, записи о здоровье,
история болезней. Файл можно распечатать или отдать ветеринару.

Все русские символы транслитерируются в латиницу, эмодзи удаляются,
чтобы fpdf2 со стандартными шрифтами мог отрисовать текст.
"""

import os
import re
from datetime import datetime
from fpdf import FPDF


# Таблица транслитерации
TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "е": "e", "ё": "e", "ж": "zh", "з": "z", "и": "i",
    "й": "y", "к": "k", "л": "l", "м": "m", "н": "n",
    "о": "o", "п": "p", "р": "r", "с": "s", "т": "t",
    "у": "u", "ф": "f", "х": "h", "ц": "ts", "ч": "ch",
    "ш": "sh", "щ": "sch", "ъ": "", "ы": "y", "ь": "",
    "э": "e", "ю": "yu", "я": "ya",
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
    "Е": "E", "Ё": "E", "Ж": "Zh", "З": "Z", "И": "I",
    "Й": "Y", "К": "K", "Л": "L", "М": "M", "Н": "N",
    "О": "O", "П": "P", "Р": "R", "С": "S", "Т": "T",
    "У": "U", "Ф": "F", "Х": "H", "Ц": "Ts", "Ч": "Ch",
    "Ш": "Sh", "Щ": "Sch", "Ъ": "", "Ы": "Y", "Ь": "",
    "Э": "E", "Ю": "Yu", "Я": "Ya",
}


def _safe_text(text) -> str:
    """Преобразует текст в безопасный для PDF.

    Удаляет эмодзи, длинные тире, кавычки-ёлочки и другие
    не-ASCII символы, которые fpdf2 не может отрисовать.

    Args:
        text: Любой объект (строка, число, None).

    Returns:
        str: Текст только из ASCII-символов.
    """
    if text is None:
        return "-"
    text = str(text)

    # Заменяем частые не-ASCII символы на ASCII-аналоги
    replacements = {
        "—": "-",   # длинное тире
        "–": "-",   # короткое тире
        "«": '"',   # кавычка-ёлочка открывающая
        "»": '"',   # кавычка-ёлочка закрывающая
        "“": '"',   # двойная кавычка открывающая
        "”": '"',   # двойная кавычка закрывающая
        "‘": "'",   # одинарная кавычка открывающая
        "’": "'",   # одинарная кавычка закрывающая
        "…": "...",  # многоточие
        "№": "N",   # номер
        "•": "-",   # буллит
    }

    result = []
    for ch in text:
        if ch in replacements:
            result.append(replacements[ch])
        elif ch in TRANSLIT:
            result.append(TRANSLIT[ch])
        elif ord(ch) < 128:
            result.append(ch)
        else:
            result.append(" ")

    safe = "".join(result)
    # Сжимаем повторяющиеся пробелы
    safe = re.sub(r"\s+", " ", safe).strip()
    return safe if safe else "-"


def _write_wrapped(pdf: FPDF, text: str) -> None:
    """Записывает текст в PDF, разбивая на короткие строки.

    Не использует multi_cell (он вызывает ошибку при нехватке места),
    а вручную режет текст на строки по 70 символов.

    Args:
        pdf (FPDF): Документ.
        text (str): Текст для записи.
    """
    # Разбиваем текст на короткие строки по 70 символов
    max_len = 70
    lines = []
    current = ""

    for word in text.split(" "):
        # Если слово само длиннее max_len — режем его
        while len(word) > max_len:
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:max_len])
            word = word[max_len:]

        # Пробуем добавить слово в текущую строку
        if len(current) + len(word) + 1 <= max_len:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    # Пишем каждую строку через cell
    for line in lines:
        pdf.cell(0, 6, line, ln=True)


class PetPDF(FPDF):
    """Класс PDF-документа с шапкой и подвалом."""

    def header(self) -> None:
        """Шапка каждой страницы."""
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(254, 178, 177)
        self.cell(0, 10, "PetHealth", ln=True, align="C")
        self.ln(5)

    def footer(self) -> None:
        """Подвал каждой страницы."""
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(138, 138, 138)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def generate_pet_pdf(db, pet_id: int, output_path: str = None) -> str:
    """Создаёт PDF-отчёт о питомце.

    Args:
        db (DatabaseManager): Менеджер базы данных.
        pet_id (int): ID питомца.
        output_path (str): Путь для сохранения PDF.
            Если None — имя формируется автоматически.

    Returns:
        str: Абсолютный путь к созданному PDF-файлу.

    Raises:
        ValueError: Если питомец с таким ID не найден.
    """
    pets = db.get_all_pets()
    pet = None
    for p in pets:
        if p[0] == pet_id:
            pet = p
            break

    if pet is None:
        raise ValueError(f"Питомец с ID {pet_id} не найден")

    _, name, species, birth_date, photo_path, notes = pet

    pdf = PetPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(51, 51, 51)

    # --- Данные питомца ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Pet information", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Name: {_safe_text(name)}", ln=True)
    pdf.cell(0, 6, f"Species: {_safe_text(species)}", ln=True)
    pdf.cell(0, 6, f"Birth date: {_safe_text(birth_date)}", ln=True)
    _write_wrapped(pdf, f"Notes: {_safe_text(notes)}")
    pdf.ln(5)

    # --- Записи о здоровье ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Health records", ln=True)
    pdf.set_font("Helvetica", "", 10)

    records = db.get_records(pet_id)
    if not records:
        pdf.cell(0, 6, "No records", ln=True)
    else:
        for rec in records:
            _, _, rec_type, date, value, next_date = rec
            line = (
                f"{_safe_text(rec_type)}: {_safe_text(value)} "
                f"({_safe_text(date)})"
            )
            if next_date:
                line += f" - next: {_safe_text(next_date)}"
            _write_wrapped(pdf, line)
    pdf.ln(5)

    # --- История болезней ---
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Disease history", ln=True)
    pdf.set_font("Helvetica", "", 10)

    pet_diseases = db.get_pet_diseases(pet_id)
    if not pet_diseases:
        pdf.cell(0, 6, "No diseases", ln=True)
    else:
        diseases = {d[0]: d[1] for d in db.get_diseases()}

        for pd in pet_diseases:
            (_, _, disease_id, date_start, date_end,
             status, treatment, notes) = pd
            disease_name = diseases.get(disease_id, f"#{disease_id}")
            line = f"{_safe_text(disease_name)} - {_safe_text(date_start)}"
            if date_end:
                line += f" - {_safe_text(date_end)}"
            line += f" - status: {_safe_text(status)}"
            if treatment:
                line += f" - treatment: {_safe_text(treatment)}"
            _write_wrapped(pdf, line)

    # --- Подпись ---
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(138, 138, 138)
    pdf.cell(
        0, 6,
        f"Generated: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        ln=True
    )

    # --- Сохраняем ---
    if output_path is None:
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", name) or "pet"
        output_path = f"{safe_name}_medical_card.pdf"

    pdf.output(output_path)
    return os.path.abspath(output_path)