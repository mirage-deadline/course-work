from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.markdown import hlink

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    link = hlink('GIT', 'https://github.com/mirage-deadline/course-work')
    await message.answer(f'''Привет, {message.from_user.full_name}! Данный бот создан для предсказывания авторства стихов.\n
Модели обучались на произведениях следующих авторах:
<b>Александр Блок, Александр Пушкин, Анна Ахматова,
Афанасий Фет, Валерий Брюсов, Владимир Маяковский,
Игорь Северянин, Константин Бальмонт, Марина Цветаева</b>
Исходный текст проекта можно посмотреть на {link}.''')
