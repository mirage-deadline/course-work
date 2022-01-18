from distutils.cmd import Command
from os import stat
from aiogram import types
from aiogram.dispatcher import FSMContext
from states.predict_state import Prediction
from aiogram.dispatcher.filters import Command
from loader import dp


@dp.message_handler(Command('predict'))
async def help_message(message: types.Message):
    await message.answer('Введите стихотворение для проверки схожести с другими авторами стихов')
    await Prediction.Q1.set()


@dp.message_handler(state=Prediction.Q1)
async def predict_text_author(message: types.Message, state: FSMContext):

    await message.answer(f'Greet {message.text}')