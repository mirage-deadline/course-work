from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from keyboards.default import reply_keybord
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/predict - Предсказать автора текста")
    
    await message.answer("\n".join(text), reply_markup=reply_keybord.help_keybord())
