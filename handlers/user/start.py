from aiogram import types, Router
from aiogram.filters import Command
from keyboards import user_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """Handles the /start command, providing general information about the cat shelter."""
    welcome_message = (
        "🏡🐾 *«Лёхин Дом»* - приют для кошек в г. Екатеринбург! 🐾🏡\n\n"
        "✨ Мы помогаем бездомным котикам найти заботливых хозяев и уютный дом.+\n\n"
        "🥰 На сегодня, более *3000* котиков обрели свой дом благодаря нам! 💖\n\n"
        "✅ Все наши котики здоровы, привиты и стерилизованы.\n\n"
        " 😻 У каждого есть ветпаспорт\n\n"
        "📞 Хотите взять котика? Пишите в бота!:\n\n"  # Added command for donation info
        "Спасибо за вашу доброту и поддержку! ❤️"
    )
    await message.answer(welcome_message, reply_markup=user_keyboard())

def register_handlers(dp):
    dp.include_router(router)