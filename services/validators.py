"""
Валидация файлов и входных данных.
"""
import os
from typing import Optional, Tuple

from .config import INPUT_FORMATS, ALL_INPUT_EXTENSIONS, MAX_FILE_SIZE_BYTES


def get_file_extension(filename: str) -> str:
    """
    Получает расширение файла в нижнем регистре.
    
    Args:
        filename: Имя файла
        
    Returns:
        Расширение файла (например, '.png')
    """
    return '.' + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def get_input_type(filename: str) -> str:
    """
    Определяет тип файла по расширению.
    
    Args:
        filename: Имя файла
        
    Returns:
        Тип файла: 'image', 'pdf', 'docx' или 'unknown'
    """
    ext = get_file_extension(filename)
    
    if ext in INPUT_FORMATS['image']:
        return 'image'
    elif ext in INPUT_FORMATS['pdf']:
        return 'pdf'
    elif ext in INPUT_FORMATS['docx']:
        return 'docx'
    else:
        return 'unknown'


def is_supported_extension(filename: str) -> bool:
    """
    Проверяет, поддерживается ли расширение файла.
    
    Args:
        filename: Имя файла
        
    Returns:
        True если расширение поддерживается
    """
    return get_file_extension(filename) in ALL_INPUT_EXTENSIONS


def validate_file_size(file_size: int) -> Tuple[bool, Optional[str]]:
    """
    Проверяет размер файла.
    
    Args:
        file_size: Размер файла в байтах
        
    Returns:
        Кортеж (успешно, сообщение об ошибке)
    """
    if file_size > MAX_FILE_SIZE_BYTES:
        return False, f"Файл слишком большой. Максимум {MAX_FILE_SIZE_BYTES // 1024 // 1024} МБ"
    return True, None


def validate_file(filename: str, file_size: int) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Комплексная валидация файла.
    
    Args:
        filename: Имя файла
        file_size: Размер файла в байтах
        
    Returns:
        Кортеж (успешно, тип файла, сообщение об ошибке)
    """
    # Проверка расширения
    if not is_supported_extension(filename):
        return False, None, f"Неподдерживаемый формат. Разрешены: {', '.join(ALL_INPUT_EXTENSIONS)}"
    
    # Проверка размера
    size_valid, size_error = validate_file_size(file_size)
    if not size_valid:
        return False, None, size_error
    
    # Определение типа
    input_type = get_input_type(filename)
    
    return True, input_type, None


def sanitize_filename(filename: str) -> str:
    """
    Очищает имя файла от опасных символов.
    
    Args:
        filename: Исходное имя файла
        
    Returns:
        Безопасное имя файла
    """
    # Базовая санитизация
    filename = os.path.basename(filename)  # Удаляем пути
    filename = filename.strip()  # Удаляем пробелы по краям
    
    # Заменяем опасные символы
    dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename
