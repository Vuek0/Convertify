"""
Основное приложение Flask.
"""
import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from services.converter import convert_image, get_supported_formats

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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
        # Сохраняем временный файл
        unique_id = uuid.uuid4().hex
        ext = os.path.splitext(file.filename)[1]
        filename = f"{unique_id}{ext}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Конвертируем
        pdf_bytes, mime_type, ext = convert_image(filepath, output_format)

        # Удаляем временный файл
        os.remove(filepath)

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


# Для локальной разработки
if __name__ == '__main__':
    app.run(debug=True)


# Для Vercel (serverless handler)
def handler(request):
    return app(request.environ, lambda *args: None)
