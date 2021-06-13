from typing import Union

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline import qiwi_keyboard
from keyboards.inline.bizlato_keyboards import bizlato_accs_keyboard
from keyboards.inline.callback_datas import set_callback
from loader import dp, bot, db
from aiogram import types

from states import AddWallet
from states.bizlato_states import AddAcc


@dp.message_handler(Text(equals="Настройки Qiwi"))
async def bot_qiwi_menu(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text="Вы выбрали настройки QIWI", reply_markup=qiwi_keyboard)


@dp.callback_query_handler(set_callback.filter(service_name="qiwi"))
async def qiwi_setups(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    action = callback_data.get("action")
    user_id = call.from_user.id
    if action == "add_wallet":
        check_for_accs = await db.show_bizlato_accs(user_id)
        if len(check_for_accs) == 0:
            markup = await bizlato_accs_keyboard(check_for_accs)
            await call.message.answer(text="Сперва нужно создать аккаунт Bitzlato", reply_markup=markup)
            await AddAcc.ButtonAdd.set()
        else:
            markup = await bizlato_accs_keyboard(check_for_accs)
            await call.message.answer(text="Выберите аккаунт Bitzlato", reply_markup=markup)
            await AddWallet.InputBizlatoAcc.set()
    # await call.message.answer(f"Вы выбрали qiwi.{action}")

# async def list_bitzlato_accounts(message: Union[types.Message, types.CallbackQuery], **kwargs):

# add_wallet
# set_limit
# choose_wallets
# delete_wallet
