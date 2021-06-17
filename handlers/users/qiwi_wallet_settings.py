from typing import Union, Text

import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard, bizlato_keyboard, back_keyboard, set_callback, bizlato_accs_keyboard
from loader import dp, bot, db
from aiogram import types
from states import QiwiSettings, AddAcc


@dp.message_handler(text="Настройки Qiwi")
async def bot_qiwi_menu(message: types.Message):
    user_id = message.from_user.id
    check_for_accs = await db.show_bizlato_accs(user_id)
    markup = await bizlato_accs_keyboard(check_for_accs)
    print(1)
    if len(check_for_accs) == 0:
        print(2)
        await message.answer(text="Сперва нужно создать аккаунт Bitzlato", reply_markup=markup)
        await AddAcc.ButtonAdd.set()
    else:
        await message.answer(text="Выберите аккаунт Bitzlato", reply_markup=markup)
        await QiwiSettings.InputBizlatoAcc.set()


@dp.callback_query_handler(state=QiwiSettings.InputBizlatoAcc)
async def select_bitzlato_acc(call: types.CallbackQuery, state=FSMContext):
    await call.answer(cache_time=30)
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    api_key = call.data
    await state.update_data(
        {
            "api_key": api_key,
            "user_id": call.from_user.id
        }
    )
    await call.message.answer(text="Вы выбрали настройки Qiwi", reply_markup=qiwi_keyboard)
    await QiwiSettings.InputOption.set()


@dp.callback_query_handler(set_callback.filter(service_name="qiwi"), state=QiwiSettings.InputOption)
async def choose_qiwi_option(call: types.CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer(cache_time=15)
    action = callback_data.get("action")
    if action == "add_wallet":
        await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                       "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                       "<i>personId - номер вашего кошелька без знака '+'\n"
                                       "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                  reply_markup=back_keyboard)
        await QiwiSettings.AddWallet.set()


# @dp.message_handler(state=QiwiSettings.AddWallet)
# async def input_qiwi_wallet(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
#     answer = type(message)
#     print(answer)
    # data = await state.get_data()
    # api_key = data.get("api_key")
    # if answer == "Отменить":
    #     await state.finish()
    #     await message.answer(text="Вы отменили действие", reply_markup=start_keyboard)
    #     await message.answer(text="Настройки QIWI", reply_markup=qiwi_keyboard)
    # else:
    #     list_answers = answer.split(":")
    #     if len(list_answers) == 2:
    #         await message.answer(text="<i>Проверяем аккаунт...</i>")
    #         accs = await db.check_qiwi_exists(answer)
    #         if accs[0]:
    #             await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
    #                                       "Попробуйте еще раз...", reply_markup=cancel_keyboard)
    #         elif get_profile(list_answers[1]) == list_answers[0]:
    #             answer += ":0:0"
    #             await db.create_qiwi_wallet(
    #                 bizlato_acc=api_key,
    #                 qiwi_wallets=answer
    #             )
    #             await state.finish()
    #             await message.answer(text="Аккаунт был успешно добавлен", reply_markup=start_keyboard)
    #             print(await db.select_all_account())
    #             await message.answer(text="Настройки Qiwi", reply_markup=qiwi_keyboard)
    #
    #         else:
    #             await message.answer(text="Проверьте правильность данных...\n"
    #                                       "Попробуйте еще раз", reply_markup=cancel_keyboard)
    #     else:
    #         await message.answer(text="Неправильные формат данных...\n"
    #                                   "Попробуйте еще раз", reply_markup=cancel_keyboard)
    #         await AddWallet.InputWallet.set()
