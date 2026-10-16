import uuid


def generate_user_data():
    uid = uuid.uuid4().hex[:10]
    return {
        "email": f"test_{uid}@yandex.ru",
        "password": "Password123",
        "name": f"User_{uid}",
    }

# def generate_user_data():
#     """
#     Возвращает словарь с данными тестового пользователя.
#     Пользователь создан заранее через API.
#     """
#     return {
#         "email": "mroizo@mail.ru",
#         "password": "password",
#         "name": "Quentin Dupieux"
#     }
