from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

class QuizState(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    results = State()

quiz_data = {
    "question1": {
        "question": "🤔 Что ты предпочитаешь?",
        "options": {
            "lazy": "😴 Спать",
            "playful": "😼 Играть",
            "calm": "🧘 Медитировать",
            "adventurous": "🗺️ Исследовать"
        }
    },
    "question2": {
        "question": "😾 Как реагируешь на людей?",
        "options": {
            "shy": "🙈 Прячусь",
            "curious": "👀 Смотрю",
            "grumpy": "🦹 Шиплю",
            "friendly": "😽 Мурлыкаю"
        }
    },
    "question3": {
        "question": "😻 Любимый деликатес?",
        "options": {
            "greedy": "🐟 Рыбка",
            "chill": "🌿 Мята",
            "classic": "🥛 Молоко",
            "gourmet": "🍣 Экзотика"
        }
    },
    "question4": {
        "question": "🏡 Любимое место?",
        "options": {
            "comfy": "💺 Кресло",
            "observant": "🪜 Шкаф",
            "simple": "📦 Коробка",
            "foodie": "🍕 Кухня"
        }
    },
    "question5": {
        "question": "🤨 Что о правилах?",
        "options": {
            "rebellious": "😈 Ломать!",
            "obedient": "😇 Слушаюсь",
            "clueless": "❓ Что?",
            "bossy": "👑 Я прав!"
        }
    }
}

cat_descriptions = {
    "lazy": "😴 Ты ленивый котик! 🎉 Тебе нравится нежиться на солнышке, сладко спать и не утруждать себя лишними движениями. Твоя жизнь - это оазис релакса и безмятежности. Другие котики завидуют твоей способности отключаться от суеты и наслаждаться каждым моментом покоя. Помни: иногда лучший способ провести день - это ничего не делать!",
    "playful": "😼 Ты игривый кот! 🎉 Энергия бьет ключом, и ты всегда готов к новым приключениям и шалостям. Лазерная указка, мячик, перышко - все это вызывает в тебе бурю восторга! Ты заражаешь своим позитивом окружающих и никогда не даешь заскучать. Твоя жизнерадостность - это твой главный козырь!",
    "calm": "🧘 Ты спокойный кот! 🎉 Ты ценишь гармонию, тишину и умиротворение. Медитация - твое второе имя! В любой ситуации ты сохраняешь хладнокровие и рассудительность. Твоя мудрость помогает другим котикам находить ответы на сложные вопросы. Ты - настоящий гуру кошачьего мира!",
    "adventurous": "🗺️ Ты кот-путешественник! 🎉 Не боишься неизведанного, всегда готов исследовать новые территории и открывать неизведанные горизонты. Заброшенные коробки, высокие шкафы, таинственные подвалы - все это вызывает в тебе неподдельный интерес! Твоя смелость и жажда приключений вдохновляют других котиков на подвиги!",
    "shy": "🙈 Ты застенчивый кот! 🎉 Ты предпочитаешь наблюдать за миром издалека, не привлекая к себе лишнего внимания. Твоя скромность и нежность покоряют сердца. Ты - настоящий ценитель уюта и комфорта, и тебе нужно время, чтобы раскрыться перед другими котиками. Но когда ты доверяешь кому-то, твоя преданность не знает границ!",
    "curious": "👀 Ты любопытный кот! 🎉 Тебе всегда интересно, что происходит вокруг, и ты не можешь устоять перед искушением заглянуть в каждый уголок. Твой ум и интерес к деталям поражают! Ты - настоящий детектив кошачьего мира, всегда готовый разгадать любую загадку. Твоя жажда знаний делает тебя незаменимым членом любой команды!",
    "grumpy": "🦹 Ты сердитый кот! 🎉 Но в глубине души ты очень добрый и ранимый. Твоя независимость и сила характера вызывают уважение. Ты не любишь, когда тебя трогают без спроса, и всегда готов дать отпор обидчикам. Но если ты кого-то полюбишь, то будешь верен ему до конца!",
    "friendly": "😽 Ты дружелюбный кот! 🎉 Ты всегда рад новым друзьям и легко находишь общий язык с другими котиками. Твоя общительность и любовь к людям делают тебя душой компании. Ты - настоящий миротворец, всегда готовый прийти на помощь и поддержать в трудную минуту!",
    "greedy": "🐟 Ты жадный кот! 🎉 Ты всегда ищешь вкусняшки и не можешь устоять перед лакомствами. Твоя любовь к еде заразительна! Ты - настоящий гурман кошачьего мира, знающий толк в хорошей еде. Твоя способность наслаждаться каждым кусочком вдохновляет других котиков ценить простые радости жизни!",
    "chill": "🌿 Ты расслабленный кот! 🎉 Ты наслаждаешься жизнью и не переживаешь по пустякам. Твой пофигизм вдохновляет! Ты умеешь отключаться от проблем и находить радость в мелочах. Твоя способность сохранять спокойствие в любой ситуации делает тебя незаменимым другом!",
    "classic": "🥛 Ты классический кот! 🎉 Ты ценишь традиции, уют и элегантность. Твоя изысканность и хорошие манеры восхищают! Ты - настоящий аристократ кошачьего мира, знающий толк в хорошем воспитании. Твоя любовь к порядку и гармонии делает тебя образцом для подражания!",
    "gourmet": "🍣 Ты кот-гурман! 🎉 Ты обожаешь изысканные блюда и разбираешься в деликатесах. Твой вкус и умение наслаждаться жизнью поражают! Ты - настоящий ценитель высокой кухни, знающий толк в хороших продуктах. Твоя способность превращать обычный обед в праздник вдохновляет других котиков на гастрономические подвиги!",
    "comfy": "💺 Ты уютный кот! 🎉 Ты любишь тепло, комфорт и мягкие подушки. Твоя мягкость и желание обниматься согревают сердца. Ты - настоящий мастер создания уютной атмосферы, знающий толк в хорошем отдыхе. Твоя способность расслабляться и наслаждаться жизнью делает тебя незаменимым другом!",
    "observant": "🪜 Ты наблюдательный кот! 🎉 Ты видишь все вокруг и ничего не упускаешь из виду. Твоя внимательность и аналитический склад ума впечатляют! Ты - настоящий детектив кошачьего мира, всегда готовый разгадать любую загадку. Твоя способность замечать детали делает тебя незаменимым помощником!",
    "simple": "📦 Ты простой кот! 🎉 Тебе не нужны излишества, чтобы быть счастливым. Твоя непритязательность и умение радоваться мелочам вдохновляют! Ты - настоящий философ кошачьего мира, знающий толк в простых радостях жизни. Твоя способность находить счастье в малом делает тебя образцом для подражания!",
    "foodie": "🍕 Ты кот-гурман! 🎉 Для тебя еда – это настоящее искусство. Твоя любовь к кулинарии и вкусным блюдам захватывает! Ты - настоящий шеф-повар кошачьего мира, знающий толк в хороших продуктах. Твоя способность создавать кулинарные шедевры вдохновляет других котиков на гастрономические эксперименты!",
    "rebellious": "😈 Ты бунтарский кот! 🎉 Ты не признаешь авторитетов и делаешь все по-своему. Твоя смелость и независимость вызывают восхищение! Ты - настоящий революционер кошачьего мира, всегда готовый бороться за свои права. Твоя способность идти против течения вдохновляет других котиков на подвиги!",
    "obedient": "😇 Ты послушный кот! 🎉 Ты всегда следуешь правилам и радуешь хозяев. Твоя дисциплинированность и ответственность впечатляют! Ты - настоящий ангел кошачьего мира, всегда готовый помочь и поддержать. Твоя способность слушаться и выполнять задания делает тебя незаменимым помощником!",
    "clueless": "❓ Ты наивный кот! 🎉 Ты не всегда понимаешь, что происходит вокруг. Твоя непосредственность и чистота души умиляют. Ты - настоящий ребенок кошачьего мира, всегда готовый к играм и забавам. Твоя способность удивляться и радоваться мелочам делает тебя незаменимым другом!",
    "bossy": "👑 Ты властный кот! 🎉 Ты всегда знаешь, чего хочешь, и добиваешься своего. Твоя уверенность и настойчивость впечатляют! Ты - настоящий лидер кошачьего мира, всегда готовый взять на себя ответственность. Твоя способность руководить и организовывать делает тебя незаменимым членом любой команды!"
}

@router.message(lambda message: message.text == "Какой ты кот?🤨")
async def start_quiz(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question1)
    await send_question(message, state, "question1")

async def send_question(message: types.Message, state: FSMContext, question_key: str):
    """Sends a question to the user with inline keyboard options."""
    data = quiz_data[question_key]
    builder = InlineKeyboardBuilder()
    buttons = []
    for trait, option_text in data["options"].items():
        buttons.append(types.InlineKeyboardButton(text=option_text, callback_data=f"quiz:{question_key}:{trait}"))

    # Divide the buttons into chunks of 2
    for i in range(0, len(buttons), 2):
        builder.row(*buttons[i:i + 2])  # Add a row with up to 2 buttons

    await message.answer(data["question"], reply_markup=builder.as_markup())

@router.callback_query(lambda c: c.data.startswith("quiz:"))
async def process_answer(callback_query: types.CallbackQuery, state: FSMContext):
    """Processes the user's answer and sends the next question or results."""
    data = callback_query.data.split(":")
    question_key = data[1]
    trait = data[2]

    # Store the answer in the state
    user_data = await state.get_data()
    if 'traits' not in user_data:
        user_data['traits'] = {}
    user_data['traits'][question_key] = trait
    await state.set_data(user_data)

    # Determine the next question or show results
    if question_key == "question1":
        await state.set_state(QuizState.question2)
        await send_question(callback_query.message, state, "question2")
    elif question_key == "question2":
        await state.set_state(QuizState.question3)
        await send_question(callback_query.message, state, "question3")
    elif question_key == "question3":
        await state.set_state(QuizState.question4)
        await send_question(callback_query.message, state, "question4")
    elif question_key == "question4":
        await state.set_state(QuizState.question5)
        await send_question(callback_query.message, state, "question5")
    elif question_key == "question5":
        await state.set_state(QuizState.results)
        await show_results(callback_query.message, state)

    await callback_query.answer()  # Acknowledge the callback query

async def show_results(message: types.Message, state: FSMContext):
    """Calculates the user's cat type and displays the results."""
    user_data = await state.get_data()
    traits = user_data.get("traits", {})

    # Count trait occurrences
    trait_counts = {}
    for question_key, trait in traits.items():
        trait_counts[trait] = trait_counts.get(trait, 0) + 1

    # Determine the dominant cat type
    if trait_counts:
        dominant_cat_type = max(trait_counts, key=trait_counts.get)
    else:
        dominant_cat_type = "unknown"  # Handle case of no answers

    # Get cat description
    if dominant_cat_type != "unknown":
        description = cat_descriptions[dominant_cat_type]
    else:
        description = "Не удалось определить ваш тип котика. Попробуйте пройти тест еще раз!"

    # Display results
    result_message = f"🎉 Ты - {dominant_cat_type}! 🎉\n\n{description}"
    await message.answer(result_message)

    # Clear the state
    await state.clear()

def register_handlers(dp):
    dp.include_router(router)