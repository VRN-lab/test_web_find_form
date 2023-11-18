import requests

url = 'http://127.0.0.1:5000/get_form'

test_data = [
    'user_name=John&user_email=john@example.com&user_phone=+7 123 456 78 90',
    'order_date=2021-09-23&order_id=123456&order_amount=1000',
    'lead_name=Jane&lead_email=jane@example.com&lead_source=website',
    'feedback_text=I like this app&feedback_rating=5',
    'name=John&field_email=john@example.com&field_phone=+7 123 456 78 90'
]

for data in test_data:
    response = requests.post(url, data=data)
    print(f'Входные данные: {data}')
    if response.text:
        try:
            response_data = response.json()
            print(f'Ответ: {response_data}')
            if 'template_name' in response_data:
                print(
                    f'Подходящий шаблон: {response_data["template_name"]}'
                )
        except ValueError:
            print(
                'Ошибка декодирования: ответ не является допустимым для JSON'
            )
            print('Фактический ответ: ' + response.text)
    else:
        print('Пустой ответ')
    print()
