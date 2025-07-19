import logging
from aiogram import Bot, Dispatcher, types, executor
from utils import get_movie_results, generate_verification_link, verify_user, send_movie_file

API_TOKEN = "8032468458:AAHa43tmVZgJvaprKNynTlG63x2-wGztGRQ"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("👋 Welcome to Rozibot!\nSend me a movie name to get started.")


@dp.message_handler()
async def movie_search_handler(message: types.Message):
    movie_name = message.text.strip()
    results = get_movie_results(movie_name)

    if not results:
        await message.reply("😔 No results found.")
        return

    keyboard = types.InlineKeyboardMarkup()
    for idx, movie in enumerate(results, 1):
        keyboard.add(types.InlineKeyboardButton(
            text=f"{idx}. {movie['title']} ({movie['quality']})",
            callback_data=f"movie_{idx}"
        ))

    await message.reply("🔍 Choose your movie:", reply_markup=keyboard)
    dp.middleware.setup_movie_cache[message.from_user.id] = results  # temporary store for user


@dp.callback_query_handler(lambda c: c.data.startswith("movie_"))
async def movie_callback_handler(callback_query: types.CallbackQuery):
    idx = int(callback_query.data.split("_")[1]) - 1
    user_id = callback_query.from_user.id
    movie = dp.middleware.setup_movie_cache[user_id][idx]

    shortlink = generate_verification_link(user_id, movie["file_id"])
    await bot.send_message(
        user_id,
        f"🔗 Click to verify: {shortlink}\n\nOnce verified, send /verified"
    )


@dp.message_handler(commands=["verified"])
async def verified_handler(message: types.Message):
    user_id = message.from_user.id
    verified, file_id = verify_user(user_id)

    if verified:
        await send_movie_file(bot, message.chat.id, file_id)
    else:
        await message.reply("❌ Verification failed. Please try again.")
