"""
Основное приложение Flask для Convertify.
"""
import os
import uuid
import tempfile
from flask import Flask, render_template, request, send_file, jsonify
from services.converter import convert_image, get_supported_formats

# Создаём Flask приложение
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB лимит


@app.route('/')
def index():
    """Главная страница с формой загрузки."""
    formats = get_supported_formats()
    return render_template('index.html', formats=formats, error=None)


@app.route('/robots.txt')
def robots():
    """Файл robots.txt для поисковиков."""
    return send_file('static/robots.txt', mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    """Sitemap для поисковиков."""
    return send_file('static/sitemap.xml', mimetype='text/xml')


@app.route('/convert', methods=['POST'])
def convert():
    """Эндпоинт для конвертации изображения."""
    if 'image' not in request.files:
        return jsonify({'error': 'Файл не загружен'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'Файл не выбран'}), 400

    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return jsonify({'error': 'Поддерживаются только PNG, JPG, JPEG'}), 400

    output_format = request.form.get('format', 'pdf')

    try:
        # Используем временную директорию (для Vercel это /tmp)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            temp_path = tmp_file.name

        # Конвертируем
        pdf_bytes, mime_type, ext = convert_image(temp_path, output_format)

        # Удаляем временный файл
        os.remove(temp_path)

        # Формируем имя выходного файла
        output_filename = os.path.splitext(file.filename)[0] + ext

        return send_file(
            __import__('io').BytesIO(pdf_bytes),
            mimetype=mime_type,
            as_attachment=True,
            download_name=output_filename
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Точка входа для Vercel Serverless Functions
def vercel_app(environ, start_response):
    """WSGI handler для Vercel."""
    return app(environ, start_response)


# Для локальной разработки
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
