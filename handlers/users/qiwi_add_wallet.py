from typing import Union

import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from keyboards.default import start_keyboard
from keyboards.inline import qiwi_keyboard, back_keyboard
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


@dp.message_handler(state=QiwiSettings.AddWallet)
@dp.callback_query_handler(state=QiwiSettings.AddWallet)
async def input_qiwi_wallet(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    answer_type = type(message)
    if answer_type == types.CallbackQuery:
        if message.data == "back":
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Вы отменили добавление кошелька", reply_markup=start_keyboard)
            await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
            await QiwiSettings.InputOption.set()
        else:
            await message.answer()
    elif answer_type == types.Message:
        data = await state.get_data()
        api_key = data.get("api_key")
        answer = message.text

        print("answer", answer)
        list_answers = answer.split(":")
        if len(list_answers) == 2:
            await message.answer(text="<i>Проверяем аккаунт...</i>")
            wallet = answer + ":0:0"
            accs = await db.check_qiwi_exists(wallet)

            wallets = await db.show_wallets(api_key)
            if accs[0]:
                await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                          "Попробуйте еще раз...", reply_markup=back_keyboard)
                await QiwiSettings.InputWallet.set()
            elif get_profile(list_answers[1]) == list_answers[0]:
                if len(wallets[0]) > 0:
                    await db.add_qiwi_wallet(
                        bizlato_api_key=api_key,
                        qiwi_wallets=wallet
                    )
                    await message.answer(text="<i>Аккаунт был успешно добавлен</i>", reply_markup=start_keyboard)
                    print(await db.select_all_account())
                    await message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
                    await QiwiSettings.InputOption.set()
                else:
                    answer += ":0:0"
                    await db.create_qiwi_wallet(
                        bizlato_api_key=api_key,
                        qiwi_wallets=answer
                    )
                    await message.answer(text="<i>Аккаунт был успешно добавлен</i>", reply_markup=start_keyboard)
                    print(await db.select_all_account())
                    await message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
                    await QiwiSettings.InputOption.set()

            else:
                await message.answer(text="Проверьте правильность данных...\n"
                                          "Попробуйте еще раз", reply_markup=back_keyboard)
                await QiwiSettings.AddWallet.set()
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=back_keyboard)
            await QiwiSettings.AddWallet.set()

# async def list_bitzlato_accounts(message: Union[types.Message, types.CallbackQuery], **kwargs):

# add_wallet
# set_limit
# choose_wallets
# delete_wallet
