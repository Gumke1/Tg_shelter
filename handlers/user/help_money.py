from aiogram import types, Router
from keyboards import user_keyboard

router = Router()

@router.message(lambda message: message.text == "Помочь приюту ❤️")  # Using Text filter instead of Command
async def help_shelter(message: types.Message):
    """Sends the shelter's bank card details and a message of gratitude."""
    bank_card_details = (
        "💰 Вы можете помочь приюту финансово, перечислив средства по следующим реквизитам:\n\n"
        "БФ ЛЁХИН ДОМ\n"
        "ИНН 6671116766 КПП 667101001\n"
        "р/с 40701810616540000570\n"
        "БИК 046577674\n"
        "Уральский Банк ПАО СБЕРБАНК РОССИИ\n"
        "Назначение платежа: благотворительный взнос\n\n"
        "🔗 Номер регистрации заявления: *№ 4789524381*\n\n"
        "Спасибо за вашу щедрость и помощь нашим котикам! 🐾❤️"
    )
    await message.answer(bank_card_details)

def register_handlers(dp):
    dp.include_router(router)