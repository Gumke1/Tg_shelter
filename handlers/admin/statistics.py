from aiogram import types, Router
from aiogram.types import Message

from sqlalchemy import func
from database import get_session, User, Cat, UserRole, get_user  # Import get_user and UserRole

router = Router()


@router.message(lambda message: message.text == "Статистика 📊 📈")
async def stat_command(message: types.Message):
    user = get_user(message.from_user.id)
    if user and user.role == UserRole.ADMIN:
        """Обработчик команды /stat для вывода статистики."""
        session = get_session()
        try:
            # Получаем пользователя из базы данных
            user = get_user(message.from_user.id)

            if user and user.role == UserRole.ADMIN:  # Проверяем, есть ли пользователь и является ли он админом
                # Получаем количество пользователей
                user_count = session.query(func.count(User.id)).scalar()

                # Получаем количество кошек
                cat_count = session.query(func.count(Cat.id)).scalar()

                # Формируем сообщение со статистикой
                message_text = f"📊 Статистика:\n\n👥 Количество пользователей: {user_count}\n🐈 Количество кошек: {cat_count}"

                # Отправляем сообщение пользователю
                await message.answer(message_text)
            else:
                await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")
        except Exception as e:
            print(f"Ошибка при получении статистики: {e}")
            await message.answer("Не удалось получить статистику. Попробуйте позже. ⚠️")
        finally:
            session.close()
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")


def register_handlers(dp):
    dp.include_router(router)
