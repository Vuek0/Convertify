"""
Логика форматов: получение поддерживаемых и доступных форматов.
"""
from typing import List, Dict

from .config import SUPPORTED_FORMATS
from .validators import get_input_type


def get_supported_formats() -> List[Dict[str, str]]:
    """
    Возвращает список всех поддерживаемых выходных форматов.
    
    Returns:
        Список словарей с информацией о форматах
    """
    return [
        {'id': 'pdf', 'name': 'PDF', 'description': 'Документ PDF'},
        {'id': 'png', 'name': 'PNG', 'description': 'Изображение PNG'},
        {'id': 'jpeg', 'name': 'JPEG', 'description': 'Изображение JPG'},
        {'id': 'webp', 'name': 'WebP', 'description': 'Изображение WebP'},
        {'id': 'ico', 'name': 'ICO', 'description': 'Иконка'},
        {'id': 'tiff', 'name': 'TIFF', 'description': 'Изображение TIFF'},
        {'id': 'docx', 'name': 'DOCX', 'description': 'Документ Word'},
    ]


def get_available_output_formats(input_type: str) -> List[Dict[str, str]]:
    """
    Возвращает доступные форматы для данного типа входного файла.
    
    Args:
        input_type: Тип файла ('image', 'pdf', 'docx')
        
    Returns:
        Список доступных выходных форматов
    """
    if input_type == 'image':
        return [
            {'id': 'pdf', 'name': 'PDF', 'description': 'Документ PDF'},
            {'id': 'png', 'name': 'PNG', 'description': 'Изображение PNG'},
            {'id': 'jpeg', 'name': 'JPEG', 'description': 'Изображение JPG'},
            {'id': 'webp', 'name': 'WebP', 'description': 'Изображение WebP'},
            {'id': 'ico', 'name': 'ICO', 'description': 'Иконка'},
            {'id': 'tiff', 'name': 'TIFF', 'description': 'Изображение TIFF'},
        ]
    elif input_type == 'pdf':
        return [
            {'id': 'png', 'name': 'PNG', 'description': 'Изображение PNG'},
            {'id': 'jpeg', 'name': 'JPEG', 'description': 'Изображение JPG'},
            {'id': 'docx', 'name': 'DOCX', 'description': 'Документ Word'},
        ]
    elif input_type == 'docx':
        return [
            {'id': 'pdf', 'name': 'PDF', 'description': 'Документ PDF'},
            {'id': 'png', 'name': 'PNG', 'description': 'Изображение PNG'},
            {'id': 'jpeg', 'name': 'JPEG', 'description': 'Изображение JPG'},
        ]
    else:
        return []


def get_formats_for_file(filename: str) -> Dict:
    """
    Возвращает информацию о форматах для конкретного файла.
    
    Args:
        filename: Имя файла
        
    Returns:
        Словарь с типом файла и доступными форматами
    """
    input_type = get_input_type(filename)
    return {
        'input_type': input_type,
        'formats': get_available_output_formats(input_type)
    }


def is_valid_output_format(input_type: str, output_format: str) -> bool:
    """
    Проверяет, можно ли конвертировать данный тип файла в указанный формат.
    
    Args:
        input_type: Тип входного файла
        output_format: Целевой формат
        
    Returns:
        True если конвертация возможна
    """
    available = get_available_output_formats(input_type)
    return any(fmt['id'] == output_format for fmt in available)
