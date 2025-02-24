from aiogram import types, Router, Bot
from database import get_take_applications #Import applications
from database import get_user, update_user_role, UserRole
router = Router()

@router.message(lambda message: message.text == "Заявки 📝 👀")
async def viewapplications_command(message: types.Message, bot: Bot):
    """Displays the 'take' applications to the admin."""
    user = get_user(message.from_user.id)
    if user and user.role == UserRole.ADMIN:
        applications = get_take_applications()

        if not applications:
            await message.answer("Нет активных заявок на взятие котов.")
            return

        for app in applications:
            user = get_user(app.user_id)

            if app.application_type.value == "take":
                await message.answer(f"Заявка ID: {app.id}\n"
                                     f"Пользователь ID: {app.user_id}\n"
                                     f"Имя пользователя {user.first_name}\n"
                                     f"Фамилия пользователя: {user.last_name}\n"
                                     f"Идентификатор кота: {app.cat_identifier}\n"  # Change details
                                     f"Тип заявки: {app.application_type.value}\n"  # Change details
                                     f"Дата подачи: {app.application_date}")
            elif app.application_type.value == "volunteer":
                await message.answer(f"Заявка ID: {app.id}\n"
                                     f"Пользователь ID: {app.user_id}\n"
                                     f"Имя пользователя {user.first_name}\n"
                                     f"Фамилия пользователя: {user.last_name}\n"
                                     f"Тип заявки: {app.application_type.value}\n"  # Change details
                                     f"Дата подачи: {app.application_date}")
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")
def register_handlers(dp):
    dp.include_router(router)