"""
Конфигурация приложения и константы.
"""
import os

# ==================== ЛИМИТЫ ====================
MAX_FILE_SIZE_MB = 16
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# ==================== ФОРМАТЫ ====================
# Поддерживаемые выходные форматы
SUPPORTED_FORMATS = {
    'pdf': {'mime': 'application/pdf', 'ext': '.pdf'},
    'png': {'mime': 'image/png', 'ext': '.png'},
    'jpeg': {'mime': 'image/jpeg', 'ext': '.jpg'},
    'webp': {'mime': 'image/webp', 'ext': '.webp'},
    'ico': {'mime': 'image/x-icon', 'ext': '.ico'},
    'tiff': {'mime': 'image/tiff', 'ext': '.tiff'},
    'docx': {'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'ext': '.docx'},
}

# Поддерживаемые входные форматы
INPUT_FORMATS = {
    'image': ['.png', '.jpg', '.jpeg'],
    'pdf': ['.pdf'],
    'docx': ['.docx'],
}

# Все поддерживаемые расширения для валидации
ALL_INPUT_EXTENSIONS = tuple(ext for formats in INPUT_FORMATS.values() for ext in formats)

# ==================== ПУТИ ====================
# Директория проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Директории
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

# Шрифты
FONT_ROBOTO = os.path.join(FONTS_DIR, 'Roboto-Regular.ttf')

# ==================== НАСТРОЙКИ КОНВЕРТАЦИИ ====================
# Настройки изображений
IMAGE_JPEG_QUALITY = 95
IMAGE_WEBP_QUALITY = 95
IMAGE_TIFF_COMPRESSION = 'tiff_lzw'

# Настройки PDF
PDF_PAGE_SIZE = 'A4'
PDF_FONT_SIZE = 11
PDF_LINE_HEIGHT = 14

# Настройки рендеринга PDF в изображения
PDF_RENDER_ZOOM = 2.0

# ==================== VERCEL ====================
# Проверка среды выполнения
IS_VERCEL = os.environ.get('VERCEL', 'false').lower() == 'true'

# Временная директория для Vercel
TEMP_DIR = '/tmp' if IS_VERCEL else None
