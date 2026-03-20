"""
Конвертация DOCX в PDF и изображения.
"""
import io
import os
import tempfile
from docx import Document
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from .font_manager import font_manager
from .pdf_converter import convert_pdf_to_image


def convert_docx_to_pdf(docx_path: str) -> tuple[bytes, str, str]:
    """
    Конвертирует DOCX в PDF с поддержкой кириллицы.
    Использует кэшированный шрифт Roboto.
    """
    doc = Document(docx_path)
    buffer = io.BytesIO()
    pdf_doc = SimpleDocTemplate(buffer, pagesize=A4)
    
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    story = []

    # Получаем стиль с кэшированным шрифтом
    cyrillic_style = font_manager.get_cyrillic_style(styles)

    # Добавляем параграфы
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            p = Paragraph(paragraph.text, cyrillic_style)
            story.append(p)
            story.append(Spacer(1, 6))

    # Добавляем таблицы
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            if any(row_data):
                table_data.append(row_data)

        if table_data:
            t = Table(table_data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#EEEEEE'),
                ('GRID', (0, 0), (-1, -1), 1, '#000000'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

    pdf_doc.build(story)
    buffer.seek(0)
    return buffer.getvalue(), 'application/pdf', '.pdf'


def convert_docx_to_image(docx_path: str, output_format: str) -> tuple[bytes, str, str]:
    """
    Конвертирует DOCX в изображение (через PDF).
    """
    if output_format not in ['png', 'jpeg']:
        raise ValueError(f"DOCX можно конвертировать только в PNG или JPEG")

    # Сначала конвертируем в PDF
    pdf_bytes, _, _ = convert_docx_to_pdf(docx_path)

    # Сохраняем PDF во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_pdf:
        tmp_pdf.write(pdf_bytes)
        tmp_pdf_path = tmp_pdf.name

    try:
        # Конвертируем PDF в изображение
        img_data, mime_type, ext = convert_pdf_to_image(tmp_pdf_path, output_format, page_number=0)
    finally:
        os.remove(tmp_pdf_path)

    return img_data, mime_type, ext
