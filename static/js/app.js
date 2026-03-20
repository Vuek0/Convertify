/**
 * Основная логика интерфейса конвертера.
 */

/**
 * Переводы (глобальный объект)
 */
const translations = {
    ru: {
        "hero.title": "Конвертер файлов",
        "hero.subtitle": "Быстро и бесплатно конвертируйте PNG, JPG, PDF, DOCX в любые форматы",
        "features.instant": "Мгновенно",
        "features.safe": "Безопасно",
        "features.free": "Без регистрации",
        "upload.title": "Перетащите файл сюда",
        "upload.hint": "или кликните для выбора (PNG, JPG, JPEG, PDF, DOCX)<br>Максимальный размер: 16 МБ",
        "form.label": "Формат вывода",
        "formats.pdf": "PDF — Документ PDF",
        "formats.png": "PNG — Изображение PNG",
        "formats.jpeg": "JPEG — Изображение JPG",
        "formats.webp": "WebP — Изображение WebP",
        "formats.ico": "ICO — Иконка",
        "formats.tiff": "TIFF — Изображение TIFF",
        "formats.docx": "DOCX — Документ Word",
        "button.convert": "Конвертировать",
        "button.converting": "Конвертирование в",
        "error.conversion": "Ошибка конвертации"
    },
    en: {
        "hero.title": "File Converter",
        "hero.subtitle": "Quickly and freely convert PNG, JPG, PDF, DOCX to any format",
        "features.instant": "Instant",
        "features.safe": "Secure",
        "features.free": "No registration",
        "upload.title": "Drop file here",
        "upload.hint": "or click to select (PNG, JPG, JPEG, PDF, DOCX)<br>Max size: 16 MB",
        "form.label": "Output format",
        "formats.pdf": "PDF — PDF Document",
        "formats.png": "PNG — PNG Image",
        "formats.jpeg": "JPEG — JPG Image",
        "formats.webp": "WebP — WebP Image",
        "formats.ico": "ICO — Icon",
        "formats.tiff": "TIFF — TIFF Image",
        "formats.docx": "DOCX — Word Document",
        "button.convert": "Convert",
        "button.converting": "Converting to",
        "error.conversion": "Conversion error"
    },
    uz: {
        "hero.title": "Fayl Konvertori",
        "hero.subtitle": "PNG, JPG, PDF, DOCX fayllarini istalgan formatga tez va bepul o'giring",
        "features.instant": "Tez",
        "features.safe": "Xavfsiz",
        "features.free": "Ro'yxatdan o'tish shart emas",
        "upload.title": "Faylni bu yerga tashlang",
        "upload.hint": "yoki tanlash uchun bosing (PNG, JPG, JPEG, PDF, DOCX)<br>Maksimal hajm: 16 MB",
        "form.label": "Chiqish formati",
        "formats.pdf": "PDF — PDF Hujjati",
        "formats.png": "PNG — PNG Rasm",
        "formats.jpeg": "JPEG — JPG Rasm",
        "formats.webp": "WebP — WebP Rasm",
        "formats.ico": "ICO — Ikonka",
        "formats.tiff": "TIFF — TIFF Rasm",
        "formats.docx": "DOCX — Word Hujjati",
        "button.convert": "Konvertatsiya",
        "button.converting": "Konvertatsiya qilinmoqda",
        "error.conversion": "Konvertatsiya xatosi"
    }
};

// Вспомогательная функция для получения перевода
function getTranslation(key, defaultText) {
    const lang = localStorage.getItem('lang') || 'ru';
    if (translations[lang] && translations[lang][key]) {
        return translations[lang][key];
    }
    return defaultText;
}

// Инициализация при загрузке
window.addEventListener('load', function() {
    initIntro();
    initThemeToggle();
    initLanguage();
    initUploadZone();
    initFilePreview();
    initFormSubmit();
    initCustomSelect();
    resetButtonState();
});

/**
 * Intro анимация
 */
function initIntro() {
    const introOverlay = document.getElementById('introOverlay');
    if (introOverlay) {
        setTimeout(() => {
            introOverlay.remove();
        }, 2000);
    }
}

/**
 * Мультиязычность
 */
function initLanguage() {
    const savedLang = localStorage.getItem('lang') || 'ru';
    setLanguage(savedLang);

    const langBtn = document.getElementById('langBtn');
    const langDropdown = document.getElementById('langDropdown');
    const langOptions = document.querySelectorAll('.lang-option');

    // Клик по кнопке языка
    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        langDropdown.classList.toggle('open');
    });

    // Выбор языка
    langOptions.forEach(option => {
        option.addEventListener('click', () => {
            const lang = option.dataset.lang;
            setLanguage(lang);
            localStorage.setItem('lang', lang);
            langDropdown.classList.remove('open');
        });
    });

    // Закрытие при клике вне
    document.addEventListener('click', () => {
        langDropdown.classList.remove('open');
    });
}

function setLanguage(lang) {
    // Обновляем текст кнопки
    document.getElementById('currentLang').textContent = lang.toUpperCase();

    // Обновляем все элементы с data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (translations[lang] && translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });

    // Обновляем select value
    const formatSelect = document.getElementById('formatSelect');
    const selectedValue = document.getElementById('selectValue');
    if (formatSelect && selectedValue) {
        const currentFormat = formatSelect.value;
        const key = `formats.${currentFormat}`;
        if (translations[lang] && translations[lang][key]) {
            selectedValue.textContent = translations[lang][key];
        }
    }
}

/**
 * Переключатель темы
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    const sunIcon = themeToggle.querySelector('.sun-icon');
    const moonIcon = themeToggle.querySelector('.moon-icon');
    const html = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme, sunIcon, moonIcon);

    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcons(newTheme, sunIcon, moonIcon);
    });
}

function updateThemeIcons(theme, sunIcon, moonIcon) {
    if (theme === 'dark') {
        sunIcon.style.display = 'none';
        moonIcon.style.display = 'block';
    } else {
        sunIcon.style.display = 'block';
        moonIcon.style.display = 'none';
    }
}

/**
 * Зона загрузки файлов
 */
function initUploadZone() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');

    uploadZone.addEventListener('click', () => fileInput.click());

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            updateFilePreview();
        }
    });
}

/**
 * Предпросмотр файла
 */
function initFilePreview() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', updateFilePreview);

    const removeBtn = document.getElementById('removeBtn');
    removeBtn.addEventListener('click', () => {
        fileInput.value = '';
        document.getElementById('filePreview').classList.remove('show');
        document.getElementById('convertBtn').disabled = true;
    });
}

function updateFilePreview() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = formatFileSize(file.size);
        document.getElementById('filePreview').classList.add('show');
        document.getElementById('convertBtn').disabled = false;
        
        // Обновляем доступные форматы на основе типа файла
        updateAvailableFormats(file.name);
    } else {
        document.getElementById('filePreview').classList.remove('show');
        document.getElementById('convertBtn').disabled = true;
    }
}

/**
 * Обновление доступных форматов на основе типа файла
 */
async function updateAvailableFormats(filename) {
    try {
        const response = await fetch(`/api/formats?filename=${encodeURIComponent(filename)}`);
        const data = await response.json();
        
        const selectOptions = document.getElementById('selectOptions');
        const formatSelect = document.getElementById('formatSelect');
        const selectValue = document.getElementById('selectValue');
        
        if (!selectOptions || !formatSelect) return;
        
        // Сохраняем текущий выбранный формат если возможно
        const currentFormat = formatSelect.value;
        
        // Очищаем текущие опции
        selectOptions.innerHTML = '';
        
        // Добавляем новые опции
        data.formats.forEach((format, index) => {
            const option = document.createElement('div');
            option.className = 'select-option';
            option.dataset.value = format.id;
            option.textContent = `${format.name} — ${format.description}`;
            
            if (index === 0) {
                option.classList.add('selected');
                formatSelect.value = format.id;
                if (selectValue) {
                    selectValue.textContent = option.textContent;
                }
            }
            
            selectOptions.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error fetching formats:', error);
    }
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' Б';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' КБ';
    return (bytes / (1024 * 1024)).toFixed(1) + ' МБ';
}

/**
 * Отправка формы
 */
function initFormSubmit() {
    document.getElementById('convertForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const fileInput = document.getElementById('fileInput');
        const formatSelect = document.getElementById('formatSelect');
        const convertBtn = document.getElementById('convertBtn');

        if (!fileInput.files[0]) {
            return;
        }

        // Проверка размера файла (16MB лимит)
        const file = fileInput.files[0];
        const maxSize = 16 * 1024 * 1024; // 16MB
        if (file.size > maxSize) {
            showError('Файл слишком большой. Максимальный размер: 16 МБ (ограничение Vercel)');
            return;
        }

        convertBtn.disabled = true;
        const selectedFormat = formatSelect.value;
        const convertingText = getTranslation('button.converting', 'Converting to');
        convertBtn.innerHTML = `<span class="spinner"></span>${convertingText} ${selectedFormat.toUpperCase()}...`;

        const formData = new FormData(this);

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });

            // Проверяем, является ли ответ JSON
            const contentType = response.headers.get('content-type');
            
            if (!response.ok) {
                if (contentType && contentType.includes('application/json')) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Ошибка конвертации');
                } else if (response.status === 413) {
                    throw new Error('Файл слишком большой. Максимальный размер: 16 МБ');
                } else if (response.status === 504) {
                    throw new Error('Превышено время ожидания. Попробуйте файл меньшего размера');
                } else {
                    throw new Error(`Ошибка сервера: ${response.status}`);
                }
            }

            const blob = await response.blob();
            
            // Проверяем, не является ли blob ошибкой
            if (blob.type.includes('text/html')) {
                throw new Error('Ошибка сервера. Попробуйте позже');
            }

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            const filename = response.headers.get('Content-Disposition')
                ? response.headers.get('Content-Disposition').split('filename=')[1].replace(/"/g, '')
                : `converted.${selectedFormat}`;

            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            resetButtonState();
        } catch (error) {
            showError(error.message);
            resetButtonState();
        }
    });
}

/**
 * Показ ошибки на странице
 */
function showError(message) {
    // Удаляем существующие ошибки
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }

    // Создаём новый элемент ошибки
    const errorEl = document.createElement('div');
    errorEl.className = 'error-message';
    errorEl.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <path d="M12 8v4M12 16h.01"/>
        </svg>
        <span>${message}</span>
        <button class="error-close" onclick="this.parentElement.remove()">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
        </button>
    `;

    // Вставляем после hero секции
    const hero = document.querySelector('.hero');
    hero.insertAdjacentElement('afterend', errorEl);

    // Авто-скрытие через 10 секунд
    setTimeout(() => {
        if (errorEl.parentElement) {
            errorEl.style.opacity = '0';
            errorEl.style.transform = 'translateY(-10px)';
            setTimeout(() => errorEl.remove(), 300);
        }
    }, 10000);
}

function resetButtonState() {
    const convertBtn = document.getElementById('convertBtn');
    const filePreview = document.getElementById('filePreview');
    const fileInput = document.getElementById('fileInput');

    convertBtn.disabled = true;
    convertBtn.innerHTML = '<span class="btn-text">Конвертировать</span>';
    filePreview.classList.remove('show');
    fileInput.value = '';
}

/**
 * Кастомный select с анимацией
 */
function initCustomSelect() {
    const customSelect = document.getElementById('customSelect');
    const selectTrigger = document.getElementById('selectTrigger');
    const selectOptions = document.getElementById('selectOptions');
    const selectValue = document.getElementById('selectValue');
    const formatSelect = document.getElementById('formatSelect');

    // Закрытие при клике вне select
    document.addEventListener('click', (e) => {
        if (!customSelect.contains(e.target)) {
            closeSelect();
        }
    });

    // Клик по триггеру
    selectTrigger.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleSelect();
    });

    // Клик по опциям (event delegation)
    selectOptions.addEventListener('click', (e) => {
        const option = e.target.closest('.select-option');
        if (!option || !selectOptions.contains(option)) return;
        
        const value = option.dataset.value;
        const text = option.textContent;

        // Обновляем значение
        selectValue.textContent = text;
        formatSelect.value = value;

        // Обновляем выделение
        selectOptions.querySelectorAll('.select-option').forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');

        closeSelect();
    });

    function toggleSelect() {
        const isOpen = selectOptions.classList.contains('open');
        if (isOpen) {
            closeSelect();
        } else {
            openSelect();
        }
    }

    function openSelect() {
        selectTrigger.classList.add('active');
        selectOptions.classList.add('open');
    }

    function closeSelect() {
        selectTrigger.classList.remove('active');
        selectOptions.classList.remove('open');
    }

    // Инициализация выбранного значения
    const currentValue = formatSelect.value;
    const selectedOption = selectOptions.querySelector(`.select-option[data-value="${currentValue}"]`);
    if (selectedOption) {
        selectValue.textContent = selectedOption.textContent;
        selectedOption.classList.add('selected');
    }
}
