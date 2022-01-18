import os
import pickle
import warnings
from distutils.cmd import Command
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.predict_state import Prediction
from utils import prepare_text


warnings.filterwarnings('ignore')



@dp.message_handler(Command('predict'))
async def help_message(message: types.Message):
    await message.answer('Введите стихотворение для проверки схожести с другими авторами стихов')
    await Prediction.Q1.set()


@dp.message_handler(state=Prediction.Q1)
async def predict_text_author(message: types.Message, state: FSMContext):
    author = predict_by_logreg(message.text)
    author2 = predict_by_svm(message.text)
    await message.answer(f'''Логистическая регрессия предсказывает, что автор данного текста 
<b>{author}</b>.\nSVD предсказывает, что автор данного текста <b>{author2}</b>
''')
    await state.finish()


def predict_by_logreg(text: str) -> str:
    text = prepare_text.make_correct(text)
    logreg = pickle.load(open(os.path.join('ML', 'models', 'logistic.sav'), 'rb'))
    return ''.join(logreg.predict([text]))


def predict_by_svm(text: str) -> str:
    text = prepare_text.make_correct(text)
    logreg = pickle.load(open(os.path.join('ML', 'models', 'svm.sav'), 'rb'))
    return ''.join(logreg.predict([text]))
