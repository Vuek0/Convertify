"""
Services package for Convertify.
Модули для обработки файлов, конвертации и валидации.
"""

# Конфигурация
from .config import (
    MAX_FILE_SIZE_MB,
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_FORMATS,
    INPUT_FORMATS,
    ALL_INPUT_EXTENSIONS,
    BASE_DIR,
    FONTS_DIR,
    FONT_ROBOTO,
    IS_VERCEL,
)

# Менеджер шрифтов (кэширование)
from .font_manager import font_manager

# Валидация
from .validators import (
    get_file_extension,
    get_input_type,
    is_supported_extension,
    validate_file_size,
    validate_file,
    sanitize_filename,
)

# Форматы
from .formats import (
    get_supported_formats,
    get_available_output_formats,
    get_formats_for_file,
    is_valid_output_format,
)

# Конвертация
from .converter import (
    convert_file,
    convert_file_auto,
)

# Обработка файлов
from .file_handler import (
    save_uploaded_file,
    delete_file,
    cleanup_files,
    generate_output_filename,
)

# HTTP ответы
from .response_builder import (
    create_file_response,
    create_json_response,
    create_error_response,
    create_success_response,
)


__all__ = [
    # Config
    'MAX_FILE_SIZE_MB',
    'MAX_FILE_SIZE_BYTES',
    'SUPPORTED_FORMATS',
    'INPUT_FORMATS',
    'ALL_INPUT_EXTENSIONS',
    'BASE_DIR',
    'FONTS_DIR',
    'FONT_ROBOTO',
    'IS_VERCEL',
    
    # Font Manager
    'font_manager',
    
    # Validators
    'get_file_extension',
    'get_input_type',
    'is_supported_extension',
    'validate_file_size',
    'validate_file',
    'sanitize_filename',
    
    # Formats
    'get_supported_formats',
    'get_available_output_formats',
    'get_formats_for_file',
    'is_valid_output_format',
    
    # Converter
    'convert_file',
    'convert_file_auto',
    
    # File handler
    'save_uploaded_file',
    'delete_file',
    'cleanup_files',
    'generate_output_filename',
    
    # Response builder
    'create_file_response',
    'create_json_response',
    'create_error_response',
    'create_success_response',
]
