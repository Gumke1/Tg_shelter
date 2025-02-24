import asyncio
import logging
import os
import uuid
from s3 import s3_photo
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import create_cat, CatGender, CatWoll
from database import get_user, UserRole
from config import BOT_TOKEN



# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()


class AddCat(StatesGroup):
    waiting_for_name = State()
    waiting_for_gender = State()
    waiting_for_age = State()
    waiting_for_color = State()
    waiting_for_wool = State()
    waiting_for_cat_tray = State()
    waiting_for_parasite = State()
    waiting_for_vacine = State()
    waiting_for_chipped = State()
    waiting_for_sterilized = State()
    waiting_for_passport = State()
    waiting_for_cost = State()
    waiting_for_identifier = State()
    waiting_for_description = State()
    waiting_for_photo = State()
    # ADDED: New state for photo


@router.message(lambda message: message.text == "Регистрация кошек 📝➕")
async def addcat_command(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    if user and user.role == UserRole.ADMIN:
        await message.answer("Введите имя кошки:")
        await state.set_state(AddCat.waiting_for_name)
    else:
        await message.answer("У вас недостаточно прав для выполнения этой команды. 🚫")


@router.message(AddCat.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите возраст кошки:")
    await state.set_state(AddCat.waiting_for_age)


@router.message(AddCat.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
    except ValueError:
        await message.answer("Некорректный возраст. Введите целое число.")
        return
    await state.update_data(age=age)
    await message.answer("Введите цвет кошки:")
    await state.set_state(AddCat.waiting_for_color)


@router.message(AddCat.waiting_for_color)
async def process_color(message: types.Message, state: FSMContext):
    await state.update_data(color=message.text)

    # Gender Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Мужской", callback_data="gender:male"),
            types.InlineKeyboardButton(text="Женский", callback_data="gender:female"),
        ]
    ])
    await message.answer("Выберите пол кошки:", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_gender)


@router.callback_query(AddCat.waiting_for_gender)
async def process_gender_callback(callback_query: types.CallbackQuery, state: FSMContext):
    gender = callback_query.data.split(":")[1]
    if gender == "male":
        cat_gender = CatGender.MALE
    elif gender == "female":
        cat_gender = CatGender.FEMALE
    else:
        await callback_query.answer("Ошибка при выборе пола.")
        return

    await state.update_data(gender=cat_gender)
    await callback_query.answer()  # Remove loading animation

    # Wool Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Пушистый", callback_data="wool:Пушистый"),
            types.InlineKeyboardButton(text="Гладкошерстный", callback_data="wool:Гладкошерстный"),
        ]
    ])
    await callback_query.message.answer("Выберите тип шерсти кошки:", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_wool)


@router.callback_query(AddCat.waiting_for_wool)
async def process_wool_callback(callback_query: types.CallbackQuery, state: FSMContext):
    wool = callback_query.data.split(":")[1]
    if wool == "Пушистый":
        cat_wool = CatWoll.SMOOTH_HAIRED
    elif wool == "Гладкошерстный":
        cat_wool = CatWoll.FLUFFY
    else:
        await callback_query.answer("Ошибка при выборе типа шерсти.")
        return

    await state.update_data(wool=cat_wool)
    await callback_query.answer()

    # Cat Tray Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="cat_tray:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="cat_tray:no"),
        ]
    ])
    await callback_query.message.answer("Приучен к лотку?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_cat_tray)


@router.callback_query(AddCat.waiting_for_cat_tray)
async def process_cat_tray_callback(callback_query: types.CallbackQuery, state: FSMContext):
    cat_tray = callback_query.data.split(":")[1]
    if cat_tray == "yes":
        cat_tray_bool = True
    elif cat_tray == "no":
        cat_tray_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return
    await state.update_data(cat_tray=cat_tray_bool)
    await callback_query.answer()

    # Parasite Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="parasite:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="parasite:no"),
        ]
    ])
    await callback_query.message.answer("Обработан от паразитов?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_parasite)


@router.callback_query(AddCat.waiting_for_parasite)
async def process_parasite_callback(callback_query: types.CallbackQuery, state: FSMContext):
    parasite = callback_query.data.split(":")[1]
    if parasite == "yes":
        parasite_bool = True
    elif parasite == "no":
        parasite_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return

    await state.update_data(parasite=parasite_bool)
    await callback_query.answer()

    # Vacine Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="vacine:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="vacine:no"),
        ]
    ])
    await callback_query.message.answer("Привит?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_vacine)


@router.callback_query(AddCat.waiting_for_vacine)
async def process_vacine_callback(callback_query: types.CallbackQuery, state: FSMContext):
    vacine = callback_query.data.split(":")[1]
    if vacine == "yes":
        vacine_bool = True
    elif vacine == "no":
        vacine_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return
    await state.update_data(vacine=vacine_bool)
    await callback_query.answer()

    # Chipped Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="chipped:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="chipped:no"),
        ]
    ])
    await callback_query.message.answer("Чипирован?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_chipped)


@router.callback_query(AddCat.waiting_for_chipped)
async def process_chipped_callback(callback_query: types.CallbackQuery, state: FSMContext):
    chipped = callback_query.data.split(":")[1]
    if chipped == "yes":
        chipped_bool = True
    elif chipped == "no":
        chipped_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return

    await state.update_data(chipped=chipped_bool)
    await callback_query.answer()

    # Sterilized Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="sterilized:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="sterilized:no"),
        ]
    ])
    await callback_query.message.answer("Стерилизован?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_sterilized)


@router.callback_query(AddCat.waiting_for_sterilized)
async def process_sterilized_callback(callback_query: types.CallbackQuery, state: FSMContext):
    sterilized = callback_query.data.split(":")[1]
    if sterilized == "yes":
        sterilized_bool = True
    elif sterilized == "no":
        sterilized_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return
    await state.update_data(sterilized=sterilized_bool)
    await callback_query.answer()

    # Passport Selection Keyboard
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Да", callback_data="passport:yes"),
            types.InlineKeyboardButton(text="Нет", callback_data="passport:no"),
        ]
    ])
    await callback_query.message.answer("Есть паспорт?", reply_markup=keyboard)
    await state.set_state(AddCat.waiting_for_passport)


@router.callback_query(AddCat.waiting_for_passport)
async def process_passport_callback(callback_query: types.CallbackQuery, state: FSMContext):
    passport = callback_query.data.split(":")[1]
    if passport == "yes":
        passport_bool = True
    elif passport == "no":
        passport_bool = False
    else:
        await callback_query.answer("Ошибка при выборе.")
        return

    await state.update_data(passport=passport_bool)
    await callback_query.answer()

    await callback_query.message.answer("Введите стоимость кошки:")
    await state.set_state(AddCat.waiting_for_cost)


@router.message(AddCat.waiting_for_cost)
async def process_cost(message: types.Message, state: FSMContext):
    try:
        cost = int(message.text)
    except ValueError:
        await message.answer("Некорректная стоимость. Введите целое число.")
        return
    await state.update_data(cost=cost)
    await message.answer("Пожалуйста придумай уникальный идентификатор для кошки")
    await state.set_state(AddCat.waiting_for_identifier)


@router.message(AddCat.waiting_for_identifier)
async def process_identifier(message: types.Message, state: FSMContext):
    await state.update_data(identifier=message.text)
    await message.answer("Введите описание кошки:")
    await state.set_state(AddCat.waiting_for_description)

@router.message(AddCat.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Пожалуйста, отправьте фотографию кошки:")
    await state.set_state(AddCat.waiting_for_photo)

@router.message(AddCat.waiting_for_photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext, bot: Bot):
    PHOTOS_DIR="photos"
    """Process the photo and get its file_id."""
    try:
        # 1. Download the photo from Telegram
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            downloaded_file = await bot.download_file(file_path)

             # 2. Create a unique filename and save locally
            filename = f"{uuid.uuid4()}.jpg"
            src = os.path.join(PHOTOS_DIR, filename) #Create path in photos directory
             # Ensure "photos" directory exists
            if not os.path.exists(PHOTOS_DIR):
                os.makedirs(PHOTOS_DIR)
            with open(src, "wb") as f:
                f.write(downloaded_file.getvalue())

            # 3. Upload the photo to S3
            try:
                s3_url = await s3_photo(src)
                if not s3_url:
                    await message.reply("Ошибка при загрузке на S3.  Пожалуйста, попробуйте еще раз позже.")
                    return #Store the photo URL in the data
                await state.update_data(photo_url=s3_url) #Удалили
                await message.reply(f"Фото успешно сохранено в папку {s3_url}") #Удалили

            except Exception as e:
                await message.reply(f"Ошибка при обработке фото: {e}")
                return
            finally:
                os.remove(src) # 4.Remove the local file Удалили удаление

        else:
            await message.reply("Это не фото!")
            return

    except Exception as e:
        await message.reply(f"Произошла ошибка при обработке фото: {str(e)}")
        return

    # 5.Retrieve all data and create cat
    data = await state.get_data()
    name = data.get("name")
    gender = data.get("gender")
    age = data.get("age")
    color = data.get("color")
    wool = data.get("wool")
    cat_tray = data.get("cat_tray")
    parasite = data.get("parasite")
    vacine = data.get("vacine")
    chipped = data.get("chipped")
    sterilized = data.get("sterilized")
    passport = data.get("passport")
    cost = data.get("cost")
    identifier = data.get("identifier")
    description = data.get("description")
    photo_url = data.get("photo_url") #Now we are saving photo_url

    cat_id = create_cat(name, gender, age, color, wool, cat_tray, parasite, vacine, chipped, sterilized, passport, cost,photo_url,identifier,description) #Returns cat_id
    if cat_id:
        await message.answer(f"Кот {name} успешно добавлен! ID кота: {identifier}")
        # You can now use s3_url to store the photo link with cat data
    else:
        await message.answer("Ошибка при добавлении кота.")

    await state.clear()

@router.message(AddCat.waiting_for_photo)
async def process_photo_invalid(message: types.Message, state: FSMContext):
    """Handles the case where the user sends something other than a photo."""
    await message.answer("Пожалуйста, отправьте фотографию кошки. Это необходимо для завершения регистрации.")

def register_handlers(dp):
    dp.include_router(router)