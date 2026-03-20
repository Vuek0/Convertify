"""
Конвертация изображений в различные форматы.
"""
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from .config import (
    SUPPORTED_FORMATS,
    IMAGE_JPEG_QUALITY,
    IMAGE_WEBP_QUALITY,
    IMAGE_TIFF_COMPRESSION,
)


def convert_image(image_path: str, output_format: str) -> tuple[bytes, str, str]:
    """
    Конвертирует изображение в указанный формат.

    Args:
        image_path: Путь к исходному изображению
        output_format: Целевой формат (pdf, png, jpeg, webp, ico, tiff)

    Returns:
        Кортеж (байты файла, MIME тип, расширение)

    Raises:
        ValueError: Если формат не поддерживается
    """
    if output_format not in SUPPORTED_FORMATS:
        raise ValueError(f"Неподдерживаемый формат: {output_format}")

    format_info = SUPPORTED_FORMATS[output_format]
    img = Image.open(image_path)
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

    buffer.seek(0)
    return buffer.getvalue(), format_info['mime'], format_info['ext']


def _convert_to_pdf(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в PDF."""
    img_rgb = img.convert('RGB')
    width, height = img.size
    
    pdf = canvas.Canvas(buffer, pagesize=(width, height))
    
    # Сохраняем в промежуточный буфер
    img_buffer = io.BytesIO()
    img_rgb.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    pdf.drawImage(ImageReader(img_buffer), 0, 0, width=width, height=height)
    pdf.save()


def _convert_to_jpeg(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в JPEG."""
    img = img.convert('RGB')
    img.save(buffer, "JPEG", quality=IMAGE_JPEG_QUALITY, optimize=True)


def _convert_to_webp(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в WebP."""
    img.save(buffer, "WEBP", quality=IMAGE_WEBP_QUALITY, method=6)


def _convert_to_ico(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в ICO."""
    img = img.convert('RGB')
    img.save(buffer, "ICO")


def _convert_to_tiff(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в TIFF."""
    img.save(buffer, "TIFF", compression=IMAGE_TIFF_COMPRESSION)


def _convert_to_png(img: Image.Image, buffer: io.BytesIO) -> None:
    """Конвертирует изображение в PNG."""
    img.save(buffer, "PNG", optimize=True)
