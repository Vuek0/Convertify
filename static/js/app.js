/**
 * Основная логика интерфейса конвертера.
 */

/**
 * Переводы (глобальный объект)
 */
const translations = {
    ru: {
        "hero.title": "Конвертер изображений",
        "hero.subtitle": "Быстро и бесплатно конвертируйте PNG, JPG, JPEG в любые форматы",
        "features.instant": "Мгновенно",
        "features.safe": "Безопасно",
        "features.free": "Без регистрации",
        "upload.title": "Перетащите файл сюда",
        "upload.hint": "или кликните для выбора (PNG, JPG, JPEG)<br>Максимальный размер: 16 МБ",
        "form.label": "Формат вывода",
        "formats.pdf": "PDF — Документ PDF",
        "formats.png": "PNG — Изображение PNG",
        "formats.jpeg": "JPEG — Изображение JPG",
        "formats.webp": "WebP — Изображение WebP",
        "formats.ico": "ICO — Иконка",
        "formats.tiff": "TIFF — Изображение TIFF",
        "button.convert": "Конвертировать",
        "button.converting": "Конвертирование в",
        "error.conversion": "Ошибка конвертации"
    },
    en: {
        "hero.title": "Image Converter",
        "hero.subtitle": "Quickly and freely convert PNG, JPG, JPEG to any format",
        "features.instant": "Instant",
        "features.safe": "Secure",
        "features.free": "No registration",
        "upload.title": "Drop file here",
        "upload.hint": "or click to select (PNG, JPG, JPEG)<br>Max size: 16 MB",
        "form.label": "Output format",
        "formats.pdf": "PDF — PDF Document",
        "formats.png": "PNG — PNG Image",
        "formats.jpeg": "JPEG — JPG Image",
        "formats.webp": "WebP — WebP Image",
        "formats.ico": "ICO — Icon",
        "formats.tiff": "TIFF — TIFF Image",
        "button.convert": "Convert",
        "button.converting": "Converting to",
        "error.conversion": "Conversion error"
    },
    uz: {
        "hero.title": "Rasm Konverteri",
        "hero.subtitle": "PNG, JPG, JPEG rasmlarini istalgan formatga tez va bepul o'giring",
        "features.instant": "Tez",
        "features.safe": "Xavfsiz",
        "features.free": "Ro'yxatdan o'tish shart emas",
        "upload.title": "Faylni bu yerga tashlang",
        "upload.hint": "yoki tanlash uchun bosing (PNG, JPG, JPEG)<br>Maksimal hajm: 16 MB",
        "form.label": "Chiqish formati",
        "formats.pdf": "PDF — PDF Hujjati",
        "formats.png": "PNG — PNG Rasm",
        "formats.jpeg": "JPEG — JPG Rasm",
        "formats.webp": "WebP — WebP Rasm",
        "formats.ico": "ICO — Ikonka",
        "formats.tiff": "TIFF — TIFF Rasm",
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
    } else {
        document.getElementById('filePreview').classList.remove('show');
        document.getElementById('convertBtn').disabled = true;
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

            if (!response.ok) {
                const errorData = await response.json();
                const errorText = getTranslation('error.conversion', 'Conversion error');
                throw new Error(errorData.error || errorText);
            }

            const blob = await response.blob();
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
            alert('Ошибка: ' + error.message);
            resetButtonState();
        }
    });
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
    const options = document.querySelectorAll('.select-option');

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

    // Клик по опции
    options.forEach((option) => {
        option.addEventListener('click', () => {
            const value = option.dataset.value;
            const text = option.textContent;

            // Обновляем значение
            selectValue.textContent = text;
            formatSelect.value = value;

            // Обновляем выделение
            options.forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');

            closeSelect();
        });
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
    const selectedOption = document.querySelector(`.select-option[data-value="${currentValue}"]`);
    if (selectedOption) {
        selectValue.textContent = selectedOption.textContent;
        selectedOption.classList.add('selected');
    }
}
