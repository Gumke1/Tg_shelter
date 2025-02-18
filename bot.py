
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # Добавлен импорт

# Импортируем роутеры
from handlers import start, register, role, help,statistics,ban
from config import BOT_TOKEN

# Создаем экземпляр бота
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)) # Изменено

# Создаем хранилище (MemoryStorage для примера, используйте Redis или другое для production)
storage = MemoryStorage()

# Создаем диспетчер
dp = Dispatcher(storage=storage)

# Регистрируем роутеры
register.register_handlers(dp)
start.register_handlers(dp)
help.register_handlers(dp)
role.register_handlers(dp)
statistics.register_handlers(dp)
ban.register_handlers(dp)

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()

