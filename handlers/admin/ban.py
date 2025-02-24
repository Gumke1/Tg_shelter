from aiogram import types, Router

from database import get_user, update_user_role, UserRole  # Import get_user
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class BanUser(StatesGroup):
    waiting_for_id = State()  # Changed state to waiting_for_id

@router.message(lambda message: message.text == "Блокировка 👤 🔒️")
async def ban_command(message: types.Message, state: FSMContext):
    """Handler for /ban command to start the process of banning a user."""
    user = get_user(message.from_user.id)

    if user and user.role == UserRole.ADMIN:
        await message.answer("Введите id пользователя, которого вы хотите заблокировать:")  # Changed prompt
        await state.set_state(BanUser.waiting_for_id)  # Changed state
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")

@router.message(BanUser.waiting_for_id)  # Changed state
async def process_user_id(message: types.Message, state: FSMContext):
    """Handler to get the user ID and ban the user."""
    try:
        user_id_to_ban = int(message.text)  # Get and parse the user ID as integer
        user_to_ban = get_user(user_id_to_ban)  # Search for user by telegram_id

        if user_to_ban:
            if update_user_role(user_to_ban.telegram_id, UserRole.BANNED):  # Ban by telegram_id
                await message.answer(f"Пользователь с id {user_id_to_ban} успешно заблокирован. ✅")
            else:
                await message.answer("Не удалось заблокировать пользователя. Попробуйте позже. ⚠️")
        else:
            await message.answer("Пользователь с таким ID не найден. ❓")

        await state.clear()

    except ValueError:
        await message.answer("Неверный формат ID пользователя. Введите целое число.")
        await state.clear()

def register_handlers(dp):
    dp.include_router(router)