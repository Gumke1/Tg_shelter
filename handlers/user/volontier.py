from aiogram import types, Router
from aiogram.filters import Command
from database import create_application, ApplicationType, UserRole, get_user  # Create to the point

router = Router()


@router.message(lambda message: message.text == "Волонтерство 🙌")
async def volunteer_command(message: types.Message):
    user = get_user(message.from_user.id)
    if user and user.role != UserRole.BANNED:
        """Handles the /volunteer command."""
        user_id = message.from_user.id  # User is not needed
        cat_identifier = None

        if create_application(user_id=user_id, cat_identifier=cat_identifier,
                              application_type=ApplicationType.VOLUNTEER):
            await message.answer("Спасибо! Ваша заявка на волонтерство принята.")
        else:
            await message.answer("Произошла ошибка при подаче заявки на волонтерство.")
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")


def register_handlers(dp):
    dp.include_router(router)
