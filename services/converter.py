"""
Основной модуль конвертации файлов.
Объединяет все конвертеры и предоставляет единый интерфейс.
"""
from .image_converter import convert_image
from .pdf_converter import convert_pdf_to_image, convert_pdf_to_docx
from .docx_converter import convert_docx_to_pdf, convert_docx_to_image
from .validators import get_input_type


def convert_file(input_path: str, input_type: str, output_format: str) -> tuple[bytes, str, str]:
    """
    Универсальная функция конвертации файлов.

    Args:
        input_path: Путь к входному файлу
        input_type: Тип файла ('image', 'pdf', 'docx')
        output_format: Целевой формат

    Returns:
        Кортеж (байты файла, MIME тип, расширение)

    Raises:
        ValueError: Если конвертация невозможна
    """
    if input_type == 'image':
        return convert_image(input_path, output_format)
    
    elif input_type == 'pdf':
        if output_format == 'docx':
            return convert_pdf_to_docx(input_path)
        elif output_format in ['png', 'jpeg']:
            return convert_pdf_to_image(input_path, output_format)
        else:
            raise ValueError(f"PDF можно конвертировать в PNG, JPEG или DOCX")
    
    elif input_type == 'docx':
        if output_format == 'pdf':
            return convert_docx_to_pdf(input_path)
        elif output_format in ['png', 'jpeg']:
            return convert_docx_to_image(input_path, output_format)
        else:
            raise ValueError(f"DOCX можно конвертировать в PDF, PNG или JPEG")
    
    else:
        raise ValueError(f"Неподдерживаемый тип файла: {input_type}")


def convert_file_auto(input_path: str, output_format: str) -> tuple[bytes, str, str]:
    """
    Конвертирует файл с автоматическим определением типа.

    Args:
        input_path: Путь к входному файлу
        output_format: Целевой формат

    Returns:
        Кортеж (байты файла, MIME тип, расширение)
    """
    import os
    filename = os.path.basename(input_path)
    input_type = get_input_type(filename)
    
    if input_type == 'unknown':
        raise ValueError(f"Неподдерживаемый формат файла: {filename}")
    
    return convert_file(input_path, input_type, output_format)
