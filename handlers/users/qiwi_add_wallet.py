from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.inline import qiwi_keyboard
from keyboards.inline.bizlato_keyboards import bizlato_accs_keyboard
from keyboards.inline.callback_datas import set_callback
from loader import dp, bot, db
from aiogram import types
from states import QiwiSettings
from states.bizlato_states import AddAcc


def get_profile(api_access_token):
    s7 = requests.Session()
    s7.headers['Accept'] = 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    p = s7.get(
        'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    print("GO")
    if p.status_code == 200:
        return str(p.json()["contractInfo"]["contractId"])
    else:
        return 0
    # await call.message.answer(f"Вы выбрали qiwi.{action}")


@dp.message_handler(state=QiwiSettings.AddWallet)
@dp.callback_query_handler(state=QiwiSettings.AddWallet)
async def input_qiwi_wallet(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    answer = type(message)
    if answer == types.CallbackQuery:
        if answer.data == "back":





# async def list_bitzlato_accounts(message: Union[types.Message, types.CallbackQuery], **kwargs):

# add_wallet
# set_limit
# choose_wallets
# delete_wallet
