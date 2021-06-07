from aiogram.dispatcher.filters import Text
from keyboards.inline import qiwi_keyboard
from keyboards.inline.callback_datas import set_callback
from loader import dp, bot
from aiogram import types

@dp.message_handler(Text(equals="Настройки Qiwi"))
async def bot_qiwi_menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,text="Вы выбрали настройки QIWI",reply_markup=qiwi_keyboard)

