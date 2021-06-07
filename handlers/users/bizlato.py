from aiogram.dispatcher.filters import Text
from keyboards.inline import bizlato_keyboard
from loader import dp, bot
from aiogram import types


@dp.message_handler(Text(equals="Настройки Bizlato"))
async def bot_qiwi_menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Вы выбрали настройки Bizlato", reply_markup=bizlato_keyboard)
