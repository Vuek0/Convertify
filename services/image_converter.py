"""
Конвертация изображений в различные форматы.
Lazy импорты и оптимизированная работа с памятью.
"""
import io
from typing import TYPE_CHECKING

from .config import (
    SUPPORTED_FORMATS,
    IMAGE_JPEG_QUALITY,
    IMAGE_WEBP_QUALITY,
    IMAGE_TIFF_COMPRESSION,
)

# Lazy импорты — загружаются только при использовании
if TYPE_CHECKING:
    from PIL import Image


def _get_pil_image(image_path: str):
    """Ленивый импорт PIL."""
    from PIL import Image
    return Image.open(image_path)


def _get_canvas():
    """Ленивый импорт reportlab canvas."""
    from reportlab.pdfgen import canvas
    return canvas


def _get_image_reader():
    """Ленивый импорт ImageReader."""
    from reportlab.lib.utils import ImageReader
    return ImageReader


def convert_image(image_path: str, output_format: str) -> tuple[bytes, str, str]:
    """
    Конвертирует изображение в указанный формат.
    Оптимизированная работа с памятью.
    """
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Неподдерживаемый формат: {output_format}")

    format_info = SUPPORTED_FORMATS[output_format]
    
    # Открываем изображение и сразу загружаем в память
    img = _get_pil_image(image_path)
    img.load()  # Принудительная загрузка — освобождает файловый дескриптор
    
    buffer = io.BytesIO()

    if output_format == 'pdf':
        _convert_to_pdf(img, buffer)
    elif output_format == 'jpeg':
        _convert_to_jpeg(img, buffer)
    elif output_format == 'webp':
        _convert_to_webp(img, buffer)
    elif output_format == 'ico':
        _convert_to_ico(img, buffer)
    elif output_format == 'tiff':
        _convert_to_tiff(img, buffer)
    else:  # png
        _convert_to_png(img, buffer)

    # Освобождаем память
    del img
    
    buffer.seek(0)
    return buffer.getvalue(), format_info['mime'], format_info['ext']


def _convert_to_pdf(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в PDF. Оптимизировано для памяти."""
    img_rgb = img.convert('RGB')
    width, height = img.size
    
    canvas_cls = _get_canvas()
    pdf = canvas_cls.Canvas(buffer, pagesize=(width, height))
    
    # Сохраняем в промежуточный буфер
    img_buffer = io.BytesIO()
    img_rgb.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    ImageReader = _get_image_reader()
    pdf.drawImage(ImageReader(img_buffer), 0, 0, width=width, height=height)
    pdf.save()
    
    # Освобождаем память
    del img_rgb, img_buffer


def _convert_to_jpeg(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в JPEG."""
    img = img.convert('RGB')
    img.save(buffer, "JPEG", quality=IMAGE_JPEG_QUALITY, optimize=True)


def _convert_to_webp(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в WebP."""
    img.save(buffer, "WEBP", quality=IMAGE_WEBP_QUALITY, method=6)


def _convert_to_ico(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в ICO."""
    img = img.convert('RGB')
    img.save(buffer, "ICO")


def _convert_to_tiff(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в TIFF."""
    img.save(buffer, "TIFF", compression=IMAGE_TIFF_COMPRESSION)


def _convert_to_png(img, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в PNG."""
    img.save(buffer, "PNG", optimize=True)
