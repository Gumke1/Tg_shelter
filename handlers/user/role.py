from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import update_user_role, UserRole


router = Router()

class ChangeRole(StatesGroup):
    waiting_for_key = State()


@router.message(Command("role"))
async def role_command(message: types.Message, state: FSMContext):
    """Обработчик команды /role."""
    await state.clear()
    await message.answer("Введите ключ администратора:")
    await state.set_state(ChangeRole.waiting_for_key)

@router.message(ChangeRole.waiting_for_key)
async def process_key(message: types.Message, state: FSMContext):
    """Обработчик ввода ключа."""
    key = message.text
    telegram_id = message.from_user.id

    if key == "123":  # Замените на свой реальный ключ
        if update_user_role(telegram_id, UserRole.ADMIN, key_active=True):
            await message.answer("Роль успешно изменена на Администратор!")
        else:
            await message.answer("Не удалось изменить роль. Попробуйте позже.")
    else:
        await message.answer("Неверный ключ.")

    await state.clear()

def register_handlers(dp):
    dp.include_router(router)