# admin_handlers.py
from keyboards import admin_keyboard
from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from database import get_session, User  # Импортируем Session и модель User из database.py
from sqlalchemy import select
import logging
from database import UserRole
from database import get_user

router = Router()


class NewsForm(StatesGroup):
    text = State()





@router.message(lambda message: message.text == "Отправить новость 📢 ➕")
async def start_news_sending(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user and user.role == UserRole.ADMIN:
        await message.answer("Введите текст новости:")
        await state.set_state(NewsForm.text)
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")

@router.message(NewsForm.text)
async def process_news_text(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(text=message.text)
    data = await state.get_data()
    news_text = data["text"]

    db = None
    try:
        user = get_user(message.from_user.id)
        if user and user.role == UserRole.ADMIN:
            db = get_session()
            if db is None:
                logging.error("Не удалось получить сессию базы данных.")
                await message.answer("Произошла ошибка при работе с базой данных.")
                return

            query = select(User.telegram_id).where(User.role == UserRole.USER)
            result = db.execute(query)
            print(result)
            user_ids = result.scalars().all()  # Используем scalars().all()
            print(user_ids, 1)
            for user_id in user_ids:
                try:
                    await bot.send_message(chat_id=user_id, text=news_text)
                    print(user_ids)
                except Exception as e:
                    logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

            await message.answer("Новость отправлена всем пользователям.")
        else:
            await message.answer("У вас недостаточно прав")

    except Exception as e:
        logging.exception("Произошла ошибка при получении списка пользователей или отправке новостей.")
        await message.answer("Произошла ошибка при отправке новости.")
    finally:
        if db:
            db.close()


def register_handlers(dp):
    dp.include_router(router)
