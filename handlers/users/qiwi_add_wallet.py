import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard
from loader import dp, bot
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


@dp.message_handler(state=AddWallet.InputWallet)
async def input_qiwi_wallet(message: types.Message, state=FSMContext):
    answer = message.text
    if answer == "Отменить":
        await state.finish()
        await message.answer(text="Вы отменили действие", reply_markup=start_keyboard)
        await message.answer(text="Настройки QIWI", reply_markup=qiwi_keyboard)

    else:
        list_answers = answer.split(":")
        if len(list_answers) == 2:
            await message.answer(text="<i>Проверяем кошелек...</i>")
            if get_profile(list_answers[1]) == list_answers[0]:
                await state.finish()
                await message.answer(text="Кошелек был проверен и добавлен в базу", reply_markup=start_keyboard)
                await message.answer(text="Настройки QIWI", reply_markup=qiwi_keyboard)

            else:
                await message.answer(text="Проверьте правильность данных...\n"
                                          "Попробуйте еще раз", reply_markup=cancel_keyboard)
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=cancel_keyboard)
            await AddWallet.InputWallet.set()
