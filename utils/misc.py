import re




def is_valid_phone_number(phone_number): #Проверка номера
    pattern = r"^\+?[1-9]\d{1,14}$"
    return bool(re.match(pattern, phone_number))
