from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот.")

def register_handlers(dp):
    dp.include_router(router) #