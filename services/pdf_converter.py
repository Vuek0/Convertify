"""
Конвертация PDF в изображения и DOCX.
Lazy импорты для ускорения загрузки модуля.
"""
import io
from typing import TYPE_CHECKING

from .config import PDF_RENDER_ZOOM

# Lazy импорты — загружаются только при использовании
if TYPE_CHECKING:
    import fitz
    from pdf2docx import Converter as PDF2DocxConverter


def _get_fitz():
    """Ленивый импорт PyMuPDF."""
    import fitz  # PyMuPDF
    return fitz


def _get_pdf2docx():
    """Ленивый импорт pdf2docx."""
    from pdf2docx import Converter as PDF2DocxConverter
    return PDF2DocxConverter


def convert_pdf_to_image(pdf_path: str, output_format: str, page_number: int = 0) -> tuple[bytes, str, str]:
    """
    Конвертирует PDF в изображение.
    """
    if output_format not in ['png', 'jpeg']:
        raise ValueError(f"PDF можно конвертировать только в PNG или JPEG")

    fitz = _get_fitz()
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
    """
    buffer = io.BytesIO()
    PDF2DocxConverter = _get_pdf2docx()

    # Конвертируем PDF в DOCX
    cv = PDF2DocxConverter(pdf_path)
    cv.convert(buffer)
    cv.close()

    buffer.seek(0)
    return buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx'
