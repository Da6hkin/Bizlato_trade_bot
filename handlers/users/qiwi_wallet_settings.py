from typing import Union, Text

import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard, bizlato_keyboard, back_keyboard, set_callback, bizlato_accs_keyboard, \
    qiwi_wallets_keyboard, useless_wallets_keyboard

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
        await message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
        await message.answer(text="<b>Сперва нужно создать аккаунт Bitzlato</b>", reply_markup=markup)
        await AddAcc.ButtonAdd.set()
    else:
        await message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
        await message.answer(text="<b>Выберите аккаунт Bitzlato</b>", reply_markup=markup)
        await QiwiSettings.InputBizlatoAcc.set()


@dp.callback_query_handler(state=QiwiSettings.InputBizlatoAcc)
async def select_bitzlato_acc(call: types.CallbackQuery, state=FSMContext):
    check_bizlato = await state.get_data()
    print(check_bizlato)
    have_acc = check_bizlato.get("already_have_acc")
    callback_data = call.data
    print(have_acc)
    print(callback_data)
    api_keys = await db.show_bizlato_keys(callback_data)
    if callback_data == "back" and have_acc:
        bitzlato_acc = check_bizlato.get("api_key")
        email = await db.show_email(bitzlato_acc)
        await state.reset_data()

        await state.update_data(
            {
                "api_key": bitzlato_acc,
                "user_id": call.from_user.id
            }
        )
        new_data = await state.get_data()
        print("Change Acc Back", new_data)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text=f"Вы работаете с аккаунтом <b>{email[0]}</b>", reply_markup=start_keyboard)
        await call.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()

    elif callback_data == "back" and have_acc is None:
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Вы вернулись назад", reply_markup=start_keyboard)
    elif len(api_keys[0]) > 0:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        acc_email = call.data
        acc_api = await db.show_bizlato_keys(acc_email)
        await state.update_data(
            {

                "api_key": acc_api[0][0],
                "user_id": call.from_user.id
            }
        )
        await call.message.answer(text=f"Вы работаете с аккаунтом <b>{acc_email}</b>", reply_markup=start_keyboard)
        await call.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await QiwiSettings.InputBizlatoAcc.set()


@dp.message_handler(state=QiwiSettings.InputOption)
@dp.callback_query_handler(state=QiwiSettings.InputOption)
async def choose_qiwi_option(call: Union[types.CallbackQuery, types.Message], state=FSMContext):
    answer_type = type(call)
    data = await state.get_data()
    print("Input_Option -", data)
    api_key = data.get("api_key")
    user_id = data.get("user_id")
    if answer_type == types.CallbackQuery:
        await call.answer()
        call_data = call.data.split(':')
        if len(call_data) == 3 and call_data[1] == "qiwi":
            action = call_data[2]
            if action == "add_wallet":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                               "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                               "<i>personId - номер вашего кошелька без знака '+'\n"
                                               "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                          reply_markup=back_keyboard)
                await QiwiSettings.AddWallet.set()
            elif action == "delete_wallet":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                check_for_qiwi = await db.show_wallets(api_key)
                print(check_for_qiwi)
                markup = await qiwi_wallets_keyboard(check_for_qiwi)
                if check_for_qiwi[0] is None or len(check_for_qiwi[0]) == 0:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Сперва нужно создать Qiwi кошелек</b>")
                    await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                              reply_markup=back_keyboard)
                    await QiwiSettings.AddWallet.set()
                else:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Выберите кошелек который хотите удалить</b>",
                                              reply_markup=markup)
                    await QiwiSettings.DeleteWallet.set()
            elif action == "show_wallets":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                check_for_qiwi = await db.show_wallets(api_key)
                print(check_for_qiwi)
                markup = await qiwi_wallets_keyboard(check_for_qiwi)
                if check_for_qiwi[0] is None or len(check_for_qiwi[0]) == 0:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Сперва нужно создать Qiwi кошелек</b>")
                    await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                              reply_markup=back_keyboard)
                    await QiwiSettings.AddWallet.set()
                else:
                    return_string = "Qiwi Кошельки:\n<b>Кошелек : Лимит\n</b>"
                    for wallet in check_for_qiwi[0]:
                        wallet_data = wallet.split(":")
                        wallet_string = f"{wallet_data[0]} : {wallet_data[3]}\n"
                        return_string += wallet_string
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text=return_string,
                                              reply_markup=back_keyboard)
                    await QiwiSettings.ShowWallets.set()
            elif action == "set_limit":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                check_for_qiwi = await db.show_wallets(api_key)
                print(check_for_qiwi)
                if check_for_qiwi[0] is None or len(check_for_qiwi[0]) == 0:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Сперва нужно создать Qiwi кошелек</b>")
                    await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                              reply_markup=back_keyboard)
                    await QiwiSettings.AddWallet.set()
                else:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="Укажите <b>лимит</b> в формате числа более единицы:",
                                              reply_markup=back_keyboard)
                    await QiwiSettings.InputLimit.set()
            elif action == "useless_wallets":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                check_for_qiwi = await db.show_wallets(api_key)
                if check_for_qiwi[0] is None or len(check_for_qiwi[0]) == 0:
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Сперва нужно создать Qiwi кошелек</b>")
                    await call.message.answer(text="Введите данные Qiwi Кошелька\n"
                                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                              reply_markup=back_keyboard)
                    await QiwiSettings.AddWallet.set()
                else:
                    useless_wallets = ""
                    wallets_list = []
                    for wallet in check_for_qiwi[0]:
                        wallet_data = wallet.split(':')
                        if wallet_data[2] == "1":
                            useless_wallets += wallet_data[0] + "\n"
                            wallets_list.append(wallet)
                    if len(useless_wallets) == 0:
                        await call.message.answer(text="<b>Ненужных кошельков нет!</b>")
                        await call.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
                        await QiwiSettings.InputOption.set()
                    else:
                        await state.update_data(
                            {
                                "useless_wallets": wallets_list
                            }
                        )
                        await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                        await call.message.answer(text="Вы уверены что хотите удалить кошельки:\n" + useless_wallets,
                                                  reply_markup=useless_wallets_keyboard)
                        await QiwiSettings.DeleteUseless.set()
            elif action == "change_acc":
                await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
                print("change_acc")
                check_for_bitzlato = await db.show_bizlato_accs(user_id)
                print("check",check_for_bitzlato)
                if len(check_for_bitzlato) < 2:
                    await call.message.answer(text="<b>Необходимо создать еще один аккаунт</b>")
                    await call.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
                    await QiwiSettings.InputOption.set()
                else:
                    for item in check_for_bitzlato:
                        bitz_api_key = await db.show_bizlato_keys(item[0])

                        if bitz_api_key[0][0] == api_key:
                            print(1)
                            check_for_bitzlato.remove(item)
                    await state.update_data(
                        {
                            "already_have_acc": True
                        }
                    )
                    markup = await bizlato_accs_keyboard(check_for_bitzlato)
                    await call.message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await call.message.answer(text="<b>Выберите аккаунт Bitzlato</b>", reply_markup=markup)
                    await QiwiSettings.InputBizlatoAcc.set()





        else:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await QiwiSettings.InputOption.set()
    if answer_type == types.Message:
        answer = call.text
        if answer == "Настройки Bitzlato":
            await state.finish()
            await bot.send_message(chat_id=call.chat.id, text="<b>Вы выбрали настройки Bizlato</b>",
                                   reply_markup=bizlato_keyboard)
        elif answer == "Параметры торговли":
            await state.finish()
            await bot.send_message(chat_id=call.chat.id, text="<b>Параметры торговли:</b>")
