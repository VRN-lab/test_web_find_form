import re
from tinydb import TinyDB
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
db = TinyDB('db.json')

templates = db.table('templates')

data = [
    {
        "name": "Form template name 1",
        "field_email": "email",
        "field_phone": "phone"
    },
    {
        "name": "Form template name 2",
        "field_text": "text",
        "field_date": "date"
    }
]


if not templates:
    for record in data:
        templates.insert(record)


def get_field_type(value):
    """
    Создаем функцию для определения типа поля по значению
    """
    try:
        datetime.strptime(value, '%d.%m.%Y')
        return 'date'
    except ValueError:
        pass
    try:
        datetime.strptime(value, '%Y-%m-%d')
        return 'date'
    except ValueError:
        pass
    if re.match(r'\+7 \d{3} \d{3} \d{2} \d{2}', value):
        return 'phone'
    if re.match(r'[^@]+@[^@]+\.[^@]+', value):
        return 'email'
    return 'text'


def find_template(data, templates):
    """
    Создаем функцию для поиска подходящего шаблона формы по данным из запроса
    """
    for template in templates:
        name = template['name']
        match = True
        for field_name, field_type in template.items():
            if field_name == 'name':
                continue
            if not any(
                get_field_type(value) == field_type for value in data.values()
            ):
                match = False
                break
            if not any(
                key == field_name for key in data.keys()
            ):
                match = False
                break
        if match:
            return name
    return None


def handle_post_request():
    """
    Создаем функцию для обработки POST запроса по url /get_form
    """
    data_str = request.data.decode()
    try:
        data = dict(item.split('=') for item in data_str.split('&'))
    except ValueError:
        return jsonify(
            {'error': 'Недопустимый формат данных'}
        )
    template_name = find_template(data, templates)
    if template_name:
        return jsonify({'template_name': template_name})
    else:
        field_types = {
            f'f_name{i+1}': get_field_type(field_value)
            for i, field_value in enumerate(data.values())
        }
    return jsonify(field_types)


@app.route('/get_form', methods=['POST'])
def get_form():
    """
    Обрабатываем запросы по url /get_form
    с помощью функции handle_post_request
    """
    return handle_post_request()


if __name__ == '__main__':
    app.run()
