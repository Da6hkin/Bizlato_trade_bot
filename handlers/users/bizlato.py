from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline import bizlato_keyboard, back_keyboard
from keyboards.inline.callback_datas import set_callback
from loader import dp, bot
from aiogram import types

from states import AddAcc


@dp.message_handler(Text(equals="Настройки Bitzlato"))
async def bot_qiwi_menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="<b>Вы выбрали настройки Bitzlato</b>",
                           reply_markup=bizlato_keyboard)


@dp.callback_query_handler(set_callback.filter(service_name="bizlato"))
async def qiwi_setups(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    action = callback_data.get("action")
    print(action)
    if action == "add_acc":
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer(text="Введите данные Bitzlato Кошелька\n"
                                       "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                       "<i>personId - номер вашего кошелька без знака '+'\n"
                                       "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                  reply_markup=back_keyboard)
        await AddAcc.InputAcc.set()
