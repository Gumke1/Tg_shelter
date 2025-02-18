from aiogram import types, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import validators
from utils.misc import is_valid_phone_number
from database import create_user

# Создаем роутер (необходимо для регистрации обработчиков)
router = Router()

# Определяем состояния
class Registration(StatesGroup):
    name = State()
    email = State()
    phone = State()

@router.message(Command('register'))
async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(Registration.name)

# Обработчик состояния name
@router.message(Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(Registration.email)

# Обработчик состояния email
@router.message(Registration.email)
async def process_email(message: types.Message, state: FSMContext):
    if validators.email(message.text):
        await state.update_data(email=message.text)
        await message.answer("Введите ваш телефон:")
        await state.set_state(Registration.phone)
    else:
        await message.answer("Некорректный email. Пожалуйста, введите его снова:")

# Обработчик состояния phone
@router.message(Registration.phone)
async def process_phone(message: types.Message, state: FSMContext):
    if is_valid_phone_number(message.text):  # Проверяем номер телефона
        await state.update_data(phone=message.text)

        # Получаем данные из FSM
        data = await state.get_data()
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")


        user = create_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, email, phone,)

        if user:
            await message.answer(f"Регистрация завершена:\nИмя: {name}\nEmail: {email}\nТелефон: {phone}")
        else:
            await message.answer("Ошибка при регистрации. Попробуйте позже.")

        # Сбрасываем состояние
        await state.clear()
    else:
        await message.answer("Некорректный номер телефона. Пожалуйста, введите его снова:")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)