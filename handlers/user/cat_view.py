from aiogram import types, Router, Bot
from aiogram.filters import Command, StateFilter  # Imported StateFilter to filter class
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_cat, get_all_cat_ids, create_application, ApplicationType, get_user, \
    UserRole  # Import get_cat, all by id
import logging

router = Router()
logging.basicConfig(level=logging.INFO)


class ViewCats(StatesGroup):
    viewing = State()


def bool_to_text(value: bool) -> str:
    """Converts boolean to Да/Нет."""
    return "Да" if value else "Нет"


async def display_cat(message: types.Message, cat_id: int, state: FSMContext, bot: Bot):
    """Displays the cat's information."""
    cat = get_cat(cat_id)

    if not cat:
        await message.answer("Кот не найден.")
        return

    text = f"🐾 Имя: {cat.name}\n" \
           f"🚻 Пол: {cat.gender.value}\n" \
           f"🎂 Возраст: {cat.age}\n" \
           f"🎨 Цвет: {cat.color}\n" \
           f"🧶 Шерсть: {cat.wool.value}\n" \
           f"🚽 Приучен к лотку: {bool_to_text(cat.cat_tray)}\n" \
           f"🐛 Паразиты: {bool_to_text(cat.parasite)}\n" \
           f"💉 Привит: {bool_to_text(cat.vacine)}\n" \
           f"📡 Чипирован: {bool_to_text(cat.chipped)}\n" \
           f"✂️ Стерилизован: {bool_to_text(cat.sterilized)}\n" \
           f"🛂 Паспорт: {bool_to_text(cat.passport)}\n" \
           f"💰 Стоимость: {cat.cost}\n" \
           f"📝 Описание: {cat.description}\n" \
           f"🆔 Идентификатор: {cat.identifier}\n" \
           f"🖼️ Фото: {cat.photo_url}"

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="⬅️", callback_data=f"nav:prev:{cat_id}"),
            types.InlineKeyboardButton(text="Хочу взять!", callback_data=f"take:{cat_id}"),
            types.InlineKeyboardButton(text="➡️", callback_data=f"nav:next:{cat_id}")
        ]
    ])
    try:
        await bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=message.message_id,
                                    reply_markup=keyboard)
    except Exception as e:
        logging.error(f"Error editing message: {e}")
        await message.answer(text, reply_markup=keyboard)  # If this error happens, send a new message
    await state.update_data(current_cat_id=cat_id)


@router.message(lambda message: message.text == "Посмотреть котиков 👁️‍🗨️")
async def viewcats_command(message: types.Message, state: FSMContext, bot: Bot):
    """Starts the cat viewing process."""
    user = get_user(message.from_user.id)
    if user and user.role != UserRole.BANNED:
        cat_ids = get_all_cat_ids()

        if not cat_ids:
            await message.answer("В базе данных нет котов.")
            return

        first_cat_id = cat_ids[0]  # Display the first cat

        await display_cat(message, first_cat_id, state, bot)  # Pass bot

        await state.set_state(ViewCats.viewing)
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")


@router.callback_query(StateFilter(ViewCats.viewing))
@router.callback_query(StateFilter(ViewCats.viewing))
async def navigate_cats(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Handles navigation between cats and "take" requests."""
    callback_data = callback_query.data
    message = callback_query.message  # Get message id
    if callback_data.startswith("nav:"):
        action, direction, cat_id = callback_data.split(":")
        cat_id = int(cat_id)

        cat_ids = get_all_cat_ids()
        try:
            current_index = cat_ids.index(cat_id)
        except ValueError:
            logging.warning(f"Cat ID {cat_id} not found in cat_ids: {cat_ids}")
            await callback_query.answer("Кот не найден, возможно он был удален.")
            await state.clear()
            return

        if direction == "next":
            new_index = (current_index + 1) % len(cat_ids)
        elif direction == "prev":
            new_index = (current_index - 1) % len(cat_ids)

        new_cat_id = cat_ids[new_index]
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            logging.exception("Failed to delete the message")  # Report when delete did not work

        await display_cat(callback_query.message, new_cat_id, state, bot)
        await callback_query.answer()  # Remove loading animation
    elif callback_data.startswith("take:"):
        action, cat_id = callback_data.split(":")  # It needs id
        cat_id = int(cat_id)
        cat = get_cat(cat_id)  # Get cat
        if cat:  # Get identifier
            # Handle "take" request
            if create_application(callback_query.from_user.id, cat.identifier, ApplicationType.TAKE):  # Save cat
                await callback_query.answer("Ваша заявка принята!")
            else:
                await callback_query.answer("Произошла ошибка при подаче заявки.")
    else:
        logging.warning(f"Unknown callback {callback_data}")
        await callback_query.answer("Unknown callback action")


def register_handlers(dp):
    dp.include_router(router)
