import random
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import logging

TOKEN = config("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start', 'help'])
async def start_handler(message: types.Message):
    # if message.text == "/help":
    await message.answer(f"Салам алейкум брат {message.from_user.full_name}")


@dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_1 = InlineKeyboardButton("NEXT", callback_data="button_1")
    markup.add(button_1)

    question = "Какая страна создала дораму?"
    answers = [
        "Россия",
        "Япония",
        "Корея",
        "Кыргызстан",
        "АКШ",
        "Сам не знаю!",
    ]
    # await message.answer_poll()
    await bot.send_poll(
        chat_id=message.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        explanation="Иди учись",
        open_period=10,
        reply_markup=markup
    )


@dp.callback_query_handler(text="button_1")
async def quiz_2(call: types.CallbackQuery):
    question = "Какой фильм выйдет 18-мая 2023 года?"
    answers = [
        "Форсаж 9",
        "Форсаж 10",
        "Форсаж 11",
        "Какой фильм?",
        "Хз",
        "Флеш",
    ]
    await bot.send_poll(
        chat_id=call.from_user.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        explanation="Иди учись",
        open_period=10,
    )


@dp.message_handler(commands=['mem'])
async def send_meme(message: types.Message):
    something = [
        'smile',
        'fun',
        'funny'
    ]
    random_mem = random.choice(something)

    await bot.send_message(chat_id=message.from_user.id, text=random_mem)


@dp.message_handler()
async def echo_message(message):
    try:
        number = int(message.text)
        result = number ** 2
        await bot.send_message(chat_id=message.from_user.id, text=f'{result}')
    except ValueError:
        await bot.send_message(chat_id=message.from_user.id, text=f'{message.text}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
