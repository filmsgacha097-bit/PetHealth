"""Модуль формирования PDF-отчёта о питомце.

Создаёт PDF-файл с полной информацией о питомце: основные данные,
записи о здоровье, история болезней. Файл можно распечатать
или отдать ветеринару.

Для поддержки кириллицы используется шрифт DejaVu Sans,
который лежит в assets/fonts/.
"""

import os
from datetime import datetime
from fpdf import FPDF


# Путь к шрифту с поддержкой кириллицы
FONT_PATH = "assets/fonts/DejaVuSans.ttf"
FONT_BOLD_PATH = "assets/fonts/DejaVuSans-Bold.ttf"
FONT_ITALIC_PATH = "assets/fonts/DejaVuSans-Oblique.ttf"


class PetPDF(FPDF):
    """Класс PDF-документа с шапкой и подвалом."""

    def header(self) -> None:
        """Шапка каждой страницы."""
        self.set_font("DejaVu", "", 16)
        self.set_text_color(254, 178, 177)
        self.cell(0, 10, "PetHealth — Медицинская карта",
                  ln=True, align="C")
        self.set_font("DejaVu", "", 10)
        self.set_text_color(138, 138, 138)
        self.cell(0, 6, "Дневник здоровья питомца",
                  ln=True, align="C")
        self.ln(5)

    def footer(self) -> None:
        """Подвал каждой страницы."""
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(138, 138, 138)
        self.cell(0, 10, f"Страница {self.page_no()}", align="C")


def _write_wrapped(pdf: FPDF, text: str) -> None:
    """Записывает текст в PDF с переносом строк.

    Args:
        pdf (FPDF): Документ.
        text (str): Текст для записи.
    """
    max_len = 70
    lines = []
    current = ""

    for word in text.split(" "):
        while len(word) > max_len:
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:max_len])
            word = word[max_len:]

        if len(current) + len(word) + 1 <= max_len:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    for line in lines:
        pdf.cell(0, 6, line, ln=True)


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
    # Подключаем шрифт с кириллицей
    pdf.add_font("DejaVu", "", FONT_PATH)
    pdf.add_page()
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(51, 51, 51)

    # --- Данные питомца ---
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 8, "Информация о питомце", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.cell(0, 6, f"Кличка: {name}", ln=True)
    pdf.cell(0, 6, f"Вид: {species}", ln=True)
    pdf.cell(0, 6, f"Дата рождения: {birth_date or '—'}", ln=True)
    _write_wrapped(pdf, f"Заметки: {notes or '—'}")
    pdf.ln(5)

    # --- Записи о здоровье ---
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 8, "Записи о здоровье", ln=True)
    pdf.set_font("DejaVu", "", 10)

    records = db.get_records(pet_id)
    if not records:
        pdf.cell(0, 6, "Записей нет", ln=True)
    else:
        type_ru = {
            "vaccine": "Вакцинация",
            "parasite": "Обработка",
            "weight": "Взвешивание",
            "note": "Заметка",
        }
        for rec in records:
            _, _, rec_type, date, value, next_date = rec
            type_label = type_ru.get(rec_type, rec_type)
            line = f"{type_label}: {value or '—'} ({date})"
            if next_date:
                line += f" — следующая: {next_date}"
            _write_wrapped(pdf, line)
    pdf.ln(5)

    # --- История болезней ---
    pdf.set_font("DejaVu", "", 13)
    pdf.cell(0, 8, "История болезней", ln=True)
    pdf.set_font("DejaVu", "", 10)

    pet_diseases = db.get_pet_diseases(pet_id)
    if not pet_diseases:
        pdf.cell(0, 6, "Заболеваний нет", ln=True)
    else:
        diseases = {d[0]: d[1] for d in db.get_diseases()}

        for pd in pet_diseases:
            (_, _, disease_id, date_start, date_end,
             status, treatment, notes) = pd
            disease_name = diseases.get(disease_id, f"#{disease_id}")
            line = f"{disease_name} — начало: {date_start}"
            if date_end:
                line += f", окончание: {date_end}"
            line += f", статус: {status}"
            if treatment:
                line += f", лечение: {treatment}"
            _write_wrapped(pdf, line)

    # --- Подпись ---
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(138, 138, 138)
    pdf.cell(
        0, 6,
        f"Сформировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        ln=True
    )

    # --- Сохраняем ---
    if output_path is None:
        safe_name = "".join(
            c if c.isalnum() or c in "-_" else "_" for c in name
        ) or "pet"
        output_path = f"{safe_name}_medical_card.pdf"

    pdf.output(output_path)
    return os.path.abspath(output_path)

    pdf.add_font("DejaVu", "B", FONT_BOLD_PATH)
    pdf.add_font("DejaVu", "", FONT_ITALIC_PATH)