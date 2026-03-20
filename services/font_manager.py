"""
Менеджер шрифтов с кэшированием.
Регистрирует шрифты один раз при первом использовании.
"""
import os
from typing import Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle

from .config import FONT_ROBOTO


class FontManager:
    """Управление шрифтами с ленивой загрузкой и кэшированием."""
    
    _initialized = False
    _cyrillic_style: Optional[ParagraphStyle] = None
    
    @classmethod
    def initialize(cls) -> None:
        """
        Инициализирует шрифты (ленивая загрузка).
        Вызывается один раз при первом использовании.
        """
        if cls._initialized:
            return
        
        try:
            if os.path.exists(FONT_ROBOTO):
                pdfmetrics.registerFont(TTFont('Roboto', FONT_ROBOTO))
                print(f"Font registered: {FONT_ROBOTO}")
            else:
                print(f"Warning: Font not found: {FONT_ROBOTO}")
        except Exception as e:
            print(f"Warning: Font registration error: {e}")
        
        cls._initialized = True
    
    @classmethod
    def get_cyrillic_style(cls, base_styles) -> ParagraphStyle:
        """
        Получает стиль параграфа с поддержкой кириллицы.
        
        Args:
            base_styles: Менеджер стилей reportlab
            
        Returns:
            Стиль параграфа с кириллическим шрифтом
        """
        cls.initialize()
        
        if cls._cyrillic_style is None:
            from reportlab.lib.styles import getSampleStyleSheet
            
            try:
                if os.path.exists(FONT_ROBOTO):
                    cls._cyrillic_style = ParagraphStyle(
                        'CyrillicNormal',
                        parent=base_styles['Normal'],
                        fontName='Roboto',
                        fontSize=11,
                        leading=14
                    )
                else:
                    cls._cyrillic_style = base_styles['Normal']
            except Exception:
                cls._cyrillic_style = base_styles['Normal']
        
        return cls._cyrillic_style
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Проверяет, инициализированы ли шрифты."""
        return cls._initialized


# Глобальный экземпляр
font_manager = FontManager()
