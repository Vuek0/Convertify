"""
Основное приложение Flask для Convertify.
Содержит только маршруты (routes). Бизнес-логика вынесена в services.
"""
from flask import Flask, render_template, request, send_file

from services import (
    # Форматы
    get_supported_formats,
    get_available_output_formats,
    get_formats_for_file,
    is_valid_output_format,
    
    # Валидация
    validate_file,
    get_input_type,
    
    # Обработка файлов
    save_uploaded_file,
    delete_file,
    generate_output_filename,
    
    # Конвертация
    convert_file,
    
    # HTTP ответы
    create_file_response,
    create_error_response,
    create_json_response,
    
    # Конфигурация
    MAX_FILE_SIZE_BYTES,
)


# Создаём Flask приложение
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_BYTES


@app.route('/')
def index():
    """Главная страница с формой загрузки."""
    formats = get_supported_formats()
    return render_template('index.html', formats=formats)


@app.route('/api/formats', methods=['GET'])
def api_formats():
    """API для получения доступных форматов на основе типа файла."""
    filename = request.args.get('filename', '')
    formats_data = get_formats_for_file(filename)
    return create_json_response(formats_data)


@app.route('/robots.txt')
def robots():
    """Файл robots.txt для поисковиков."""
    return send_file('static/robots.txt', mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    """Sitemap для поисковиков."""
    return send_file('static/sitemap.xml', mimetype='text/xml')


@app.route('/privacy')
def privacy():
    """Страница политики конфиденциальности."""
    return render_template('privacy.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Эндпоинт для конвертации файла."""
    temp_path = None
    
    try:
        # Проверка наличия файла
        if 'image' not in request.files:
            return create_error_response('Файл не загружен', 400)
        
        file = request.files['image']
        
        if not file.filename:
            return create_error_response('Файл не выбран', 400)
        
        # Валидация файла
        is_valid, input_type, error = validate_file(file.filename, len(file.stream.read()))
        file.stream.seek(0)  # Сбрасываем поток для последующего чтения
        
        if not is_valid:
            return create_error_response(error, 400)
        
        # Получение формата вывода
        output_format = request.form.get('format', 'pdf')
        
        # Проверка допустимости формата
        if not is_valid_output_format(input_type, output_format):
            return create_error_response(f"Невозможно конвертировать в {output_format}", 400)
        
        # Сохранение файла
        temp_path, original_filename = save_uploaded_file(file)
        
        # Конвертация
        result_bytes, mime_type, ext = convert_file(temp_path, input_type, output_format)
        
        # Генерация имени выходного файла
        output_filename = generate_output_filename(original_filename, ext)
        
        # Возврат файла
        return create_file_response(result_bytes, mime_type, output_filename)
        
    except ValueError as e:
        return create_error_response(str(e), 400)
    except Exception as e:
        return create_error_response(f"Ошибка конвертации: {str(e)}", 500)
    finally:
        # Гарантированное удаление временного файла
        if temp_path:
            delete_file(temp_path)


# Точка входа для Vercel Serverless Functions
def vercel_app(environ, start_response):
    """WSGI handler для Vercel."""
    return app(environ, start_response)


# Для локальной разработки
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
