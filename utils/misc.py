import re


def greet_user(first_name):
    """Приветствует пользователя по имени."""
    return f"Привет, {first_name}!"


def format_date(date):
    """Форматирует дату в удобочитаемый формат."""
    return date.strftime("%d.%m.%Y %H:%M:%S")


def is_valid_phone_number(phone_number):
    pattern = r"^\+?[1-9]\d{1,14}$"
    return bool(re.match(pattern, phone_number))
