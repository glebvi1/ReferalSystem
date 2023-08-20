import time

from users.models import User
from users.services.generate_code import generate_auth_code


def verify_auth_code(auth_code: str, user_id: int) -> bool:
    """Функция проверки кода авторизации"""
    user = User.objects.get(id=user_id)
    if user.auth_code is None:
        return True
    if user.auth_code != auth_code:
        return False

    user.auth_code = None
    user.save()

    return True


def check_phone_number(phone_number: str) -> bool:
    """Проверка номера телефона"""
    if len(phone_number) == 12:
        return phone_number[:2] == "+7" and phone_number[1:].isdigit()
    elif len(phone_number) == 11:
        return phone_number[0] == "8" and phone_number.isdigit()


def refactor_phone_number(phone_number: str) -> str:
    """Преобразовывает номер телефона к формату: 8..."""
    if len(phone_number) == 12:
        return "8" + phone_number[2:]
    return phone_number


def assign_auth_code(user: User) -> None:
    """Присвоение кода авторизации пользователя. Задержка сервера на 2 секунды"""
    user.auth_code = generate_auth_code()
    user.save()
    time.sleep(2)
