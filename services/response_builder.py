"""
Построение HTTP ответов для Flask.
"""
import io
from urllib.parse import quote
from flask import Response, send_file
from typing import Optional


def create_file_response(
    file_bytes: bytes,
    mimetype: str,
    filename: str,
    as_attachment: bool = True
) -> Response:
    """
    Создаёт HTTP ответ с файлом.

    Args:
        file_bytes: Байты файла
        mimetype: MIME тип файла
        filename: Имя файла для скачивания
        as_attachment: Скачивать файл или отображать в браузере

    Returns:
        Flask Response объект
    """
    response = send_file(
        io.BytesIO(file_bytes),
        mimetype=mimetype,
        as_attachment=as_attachment,
        download_name=filename
    )

    # Добавляем заголовок с правильной кодировкой для кириллицы (RFC 5987)
    encoded_filename = quote(filename.encode('utf-8'))
    response.headers['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'

    return response


def create_json_response(data: dict, status: int = 200) -> Response:
    """
    Создаёт HTTP ответ с JSON.

    Args:
        data: Словарь данных
        status: HTTP статус код

    Returns:
        Flask Response объект
    """
    from flask import jsonify
    return jsonify(data), status


def create_error_response(message: str, status: int = 400) -> Response:
    """
    Создаёт HTTP ответ с ошибкой.

    Args:
        message: Сообщение об ошибке
        status: HTTP статус код

    Returns:
        Flask Response объект
    """
    return create_json_response({'error': message}, status)


def create_success_response(message: Optional[str] = None, data: Optional[dict] = None, status: int = 200) -> Response:
    """
    Создаёт HTTP ответ с успехом.

    Args:
        message: Сообщение об успехе (опционально)
        data: Дополнительные данные (опционально)
        status: HTTP статус код

    Returns:
        Flask Response объект
    """
    response_data = {'success': True}
    if message:
        response_data['message'] = message
    if data:
        response_data['data'] = data
    
    return create_json_response(response_data, status)
