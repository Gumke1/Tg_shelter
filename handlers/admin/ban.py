from aiogram import types, Router
from aiogram.filters import Command
from database import get_user, update_user_role, UserRole, get_user_by_username  # Import get_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class BanUser(StatesGroup):
    waiting_for_username = State()  # Изменили состояние

@router.message(Command("ban"))
async def ban_command(message: types.Message, state: FSMContext):
    """Обработчик команды /ban для запуска процесса блокировки пользователя."""
    user = get_user(message.from_user.id)

    if user and user.role == UserRole.ADMIN:
        await message.answer("Введите username пользователя, которого вы хотите заблокировать:")  # Изменили текст
        await state.set_state(BanUser.waiting_for_username)  # Изменили состояние
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")

@router.message(BanUser.waiting_for_username)  # Изменили состояние
async def process_username(message: types.Message, state: FSMContext):
    """Обработчик для получения username пользователя и блокировки."""
    username_to_ban = message.text
    user_to_ban = get_user_by_username(username_to_ban)  # Ищем пользователя по username
    print(user_to_ban)
    if user_to_ban:
        if update_user_role(user_to_ban.telegram_id, UserRole.BANNED):  # Блокируем по telegram_id
            await message.answer(f"Пользователь с username @{username_to_ban} успешно заблокирован. ✅")
        else:
            await message.answer("Не удалось заблокировать пользователя. Попробуйте позже. ⚠️")
    else:
        await message.answer("Пользователь с таким username не найден. ❓")

    await state.clear()


def register_handlers(dp):
    dp.include_router(router)