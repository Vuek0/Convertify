"""
Сервис конвертации изображений в различные форматы.
Использует reportlab для PDF и Pillow для остальных форматов.
"""
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


SUPPORTED_FORMATS = {
    'pdf': {'mime': 'application/pdf', 'ext': '.pdf'},
    'png': {'mime': 'image/png', 'ext': '.png'},
    'jpeg': {'mime': 'image/jpeg', 'ext': '.jpg'},
    'webp': {'mime': 'image/webp', 'ext': '.webp'},
    'ico': {'mime': 'image/x-icon', 'ext': '.ico'},
    'tiff': {'mime': 'image/tiff', 'ext': '.tiff'},
}


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
    
    # Открываем изображение
    img = Image.open(image_path)
    
    # Создаем буфер для вывода
    buffer = io.BytesIO()
    
    if output_format == 'pdf':
        # Конвертация в PDF с помощью reportlab
        img_rgb = img.convert('RGB')
        width, height = img.size
        
        pdf = canvas.Canvas(buffer, pagesize=(width, height))
        
        # Сохраняем изображение во временный буфер
        img_buffer = io.BytesIO()
        img_rgb.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Добавляем изображение в PDF с высоким качеством
        pdf.drawImage(ImageReader(img_buffer), 0, 0, width=width, height=height)
        pdf.save()
        
    elif output_format == 'jpeg':
        img = img.convert('RGB')
        img.save(buffer, "JPEG", quality=95, optimize=True)
        
    elif output_format == 'webp':
        img.save(buffer, "WEBP", quality=95, method=6)
        
    elif output_format == 'ico':
        img = img.convert('RGB')
        img.save(buffer, "ICO")
        
    elif output_format == 'tiff':
        img.save(buffer, "TIFF", compression='tiff_lzw')
        
    else:
        # PNG и другие форматы
        img.save(buffer, output_format.upper(), optimize=True)
    
    buffer.seek(0)
    
    return buffer.getvalue(), format_info['mime'], format_info['ext']


def get_supported_formats() -> list[dict]:
    """Возвращает список поддерживаемых форматов."""
    return [
        {'id': 'pdf', 'name': 'PDF', 'description': 'Документ PDF (reportlab)'},
        {'id': 'png', 'name': 'PNG', 'description': 'Изображение PNG'},
        {'id': 'jpeg', 'name': 'JPEG', 'description': 'Изображение JPG'},
        {'id': 'webp', 'name': 'WebP', 'description': 'Изображение WebP'},
        {'id': 'ico', 'name': 'ICO', 'description': 'Иконка'},
        {'id': 'tiff', 'name': 'TIFF', 'description': 'Изображение TIFF'},
    ]
