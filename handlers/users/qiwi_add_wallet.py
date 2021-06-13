import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard
from loader import dp, bot, db
from aiogram import types
from states import AddWallet


def get_profile(api_access_token):
    s7 = requests.Session()
    s7.headers['Accept'] = 'application/json'
    s7.headers['authorization'] = 'Bearer ' + api_access_token
    p = s7.get(
        'https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    if p.status_code == 200:
        return str(p.json()["contractInfo"]["contractId"])
    else:
        return 0


@dp.callback_query_handler(state=AddWallet.InputBizlatoAcc)
async def select_bitzlato_acc(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=30)
    api_key = call.data
    await state.update_data(
        {
            "api_key": api_key
        }
    )
    await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>")
    await AddWallet.InputWallet.set()


@dp.message_handler(state=AddWallet.InputWallet)
async def input_qiwi_wallet(message: types.Message, state=FSMContext):
    answer = message.text
    data = await state.get_data()
    api_key = data.get("api_key")
    if answer == "Отменить":
        await state.finish()
        await message.answer(text="Вы отменили действие", reply_markup=start_keyboard)
        await message.answer(text="Настройки QIWI", reply_markup=qiwi_keyboard)
    else:
        list_answers = answer.split(":")
        if len(list_answers) == 2:
            await message.answer(text="<i>Проверяем аккаунт...</i>")
            accs = await db.check_qiwi_exists(answer)
            if accs[0]:
                await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                          "Попробуйте еще раз...", reply_markup=cancel_keyboard)
            elif get_profile(list_answers[1]) == list_answers[0]:
                await message.answer(text="Проверьте правильность данных...\n"
                                          "Попробуйте еще раз", reply_markup=cancel_keyboard)
            else:
                await db.create_qiwi_wallet(
                    bizlato_acc=api_key,
                    qiwi_wallets=answer
                )
                await state.finish()
                await message.answer(text="Аккаунт был успешно добавлен", reply_markup=start_keyboard)
                await message.answer(text="Настройки Qiwi", reply_markup=qiwi_keyboard)
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=cancel_keyboard)
            await AddWallet.InputWallet.set()

