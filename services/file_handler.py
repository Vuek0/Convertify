"""
Обработка файлов: загрузка, сохранение, удаление.
"""
import os
import tempfile
from typing import Optional, Tuple
from werkzeug.datastructures import FileStorage

from .config import TEMP_DIR, IS_VERCEL
from .validators import sanitize_filename


def save_uploaded_file(file: FileStorage, suffix: Optional[str] = None) -> Tuple[str, str]:
    """
    Сохраняет загруженный файл во временную директорию.

    Args:
        file: Загруженный файл (werkzeug FileStorage)
        suffix: Расширение файла (по умолчанию определяется из имени)

    Returns:
        Кортеж (путь к файлу, оригинальное имя файла)
    """
    original_filename = file.filename or 'unnamed'
    safe_filename = sanitize_filename(original_filename)
    
    # Определяем расширение
    if suffix is None:
        suffix = os.path.splitext(safe_filename)[1] or '.tmp'
    elif not suffix.startswith('.'):
        suffix = '.' + suffix

    # Создаём временный файл
    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
        dir=TEMP_DIR if IS_VERCEL else None
    )
    
    try:
        file.save(temp_file.name)
        temp_path = temp_file.name
    finally:
        temp_file.close()

    return temp_path, safe_filename


def delete_file(file_path: str) -> bool:
    """
    Удаляет файл с диска.

    Args:
        file_path: Путь к файлу

    Returns:
        True если файл удалён, False если файл не существовал
    """
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except OSError:
            return False
    return False


def cleanup_files(*file_paths: str) -> None:
    """
    Удаляет несколько файлов, игнорируя ошибки.

    Args:
        file_paths: Пути к файлам для удаления
    """
    for path in file_paths:
        delete_file(path)


def get_file_extension(filename: str) -> str:
    """
    Получает расширение файла из имени.

    Args:
        filename: Имя файла

    Returns:
        Расширение файла (например, '.pdf')
    """
    _, ext = os.path.splitext(filename)
    return ext.lower() if ext else '.tmp'


def generate_output_filename(original_filename: str, extension: str) -> str:
    """
    Генерирует имя выходного файла.

    Args:
        original_filename: Оригинальное имя файла
        extension: Новое расширение

    Returns:
        Имя выходного файла
    """
    # Удаляем старое расширение
    name_without_ext = os.path.splitext(original_filename)[0]
    
    # Добавляем новое
    if not extension.startswith('.'):
        extension = '.' + extension
    
    return f"{name_without_ext}{extension}"
