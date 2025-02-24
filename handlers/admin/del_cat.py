from aiogram import types, Router
from database import get_user, UserRole
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_cat_by_identifier, delete_cat  # Import delete_cat

router = Router()


class DeleteCat(StatesGroup):
    waiting_for_identifier = State()
    confirmation = State()


@router.message(lambda message: message.text == "Удалить котика📝➖")
async def deletecat_command(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user and user.role == UserRole.ADMIN:
        await message.answer("Введите identifier кота, которого вы хотите удалить:")
        await state.set_state(DeleteCat.waiting_for_identifier)
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")


@router.message(DeleteCat.waiting_for_identifier)
async def process_identifier(message: types.Message, state: FSMContext):
    identifier = message.text
    cat = get_cat_by_identifier(identifier)

    if cat:
        await state.update_data(cat_id=cat.id)  # Store the cat's ID
        # Create confirmation keyboard
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Да", callback_data="confirm:yes"),
                types.InlineKeyboardButton(text="Нет", callback_data="confirm:no"),
            ]
        ])
        await message.answer(f"Вы уверены, что хотите удалить кота {cat.name} (id: {cat.id})?", reply_markup=keyboard)
        await state.set_state(DeleteCat.confirmation)
    else:
        await message.answer("Кот с таким identifier не найден.")
        await state.clear()


@router.callback_query(DeleteCat.confirmation)
async def process_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    confirmation = callback_query.data.split(":")[1]
    data = await state.get_data()
    cat_id = data.get("cat_id")
    await callback_query.answer()  # Remove loading animation
    if confirmation == "yes":
        if delete_cat(cat_id):
            await callback_query.message.answer("Кот успешно удален из базы данных.")
        else:
            await callback_query.message.answer("Ошибка при удалении кота.")
    else:
        await callback_query.message.answer("Удаление отменено.")

    await state.clear()


def register_handlers(dp):
    dp.include_router(router)
