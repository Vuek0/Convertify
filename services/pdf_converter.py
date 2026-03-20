"""
Конвертация PDF в изображения и DOCX.
"""
import io
import fitz  # PyMuPDF
from pdf2docx import Converter as PDF2DocxConverter

from .config import PDF_RENDER_ZOOM


def convert_pdf_to_image(pdf_path: str, output_format: str, page_number: int = 0) -> tuple[bytes, str, str]:
    """
    Конвертирует PDF в изображение.

    Args:
        pdf_path: Путь к PDF файлу
        output_format: Целевой формат ('png' или 'jpeg')
        page_number: Номер страницы (0-based)

    Returns:
        Кортеж (байты файла, MIME тип, расширение)

    Raises:
        ValueError: Если формат не поддерживается
    """
    if output_format not in ['png', 'jpeg']:
        raise ValueError(f"PDF можно конвертировать только в PNG или JPEG")

    doc = fitz.open(pdf_path)

    # Проверяем номер страницы
    if page_number >= len(doc):
        page_number = 0

    page = doc[page_number]

    # Рендерим страницу в изображение с зумом
    zoom = PDF_RENDER_ZOOM
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img_data = pix.tobytes(output_format.upper())

    doc.close()

    mime_type = 'image/png' if output_format == 'png' else 'image/jpeg'
    ext = '.png' if output_format == 'png' else '.jpg'

    return img_data, mime_type, ext


def convert_pdf_to_docx(pdf_path: str) -> tuple[bytes, str, str]:
    """
    Конвертирует PDF в DOCX (Word документ).

    Args:
        pdf_path: Путь к PDF файлу

    Returns:
        Кортеж (байты файла, MIME тип, расширение)
    """
    buffer = io.BytesIO()

    # Конвертируем PDF в DOCX
    cv = PDF2DocxConverter(pdf_path)
    cv.convert(buffer)
    cv.close()

    buffer.seek(0)
    return buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'
