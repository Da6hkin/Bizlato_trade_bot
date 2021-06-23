from typing import Union

import asyncpg.exceptions
import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard, bizlato_keyboard, set_callback, back_keyboard, bizlato_accs_keyboard
from loader import dp, bot, db
from aiogram import types
from states import AddAcc, QiwiSettings


@dp.callback_query_handler(state=AddAcc.ButtonAdd)
async def bizlato_add_button(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    callback_data = call.data.split(":")
    if callback_data[0] == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Вы вернулись назад", reply_markup=start_keyboard)
    elif len(callback_data) == 3 and callback_data[1] == "bizlato" and callback_data[2] == "add_acc":
        await state.update_data(
            {
                "return_qiwi": True
            }
        )
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=None)
        await call.message.answer(text="Введите данные Bitzlato Кошелька\n"
                                       "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                       "<i>personId - номер вашего кошелька без знака '+'\n"
                                       "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>",
                                  reply_markup=back_keyboard)
        await AddAcc.InputAcc.set()
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await AddAcc.ButtonAdd.set()


@dp.callback_query_handler(state=AddAcc.InputAcc)
@dp.message_handler(state=AddAcc.InputAcc)
async def input_bizlato_acc(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    message_type = type(message)
    data = await state.get_data()
    if message_type == types.CallbackQuery:
        if message.data == "back":
            await state.finish()
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Вы отменили добавление аккаунта", reply_markup=start_keyboard)
        else:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await AddAcc.InputAcc.set()
    elif message_type == types.Message:
        answer = message.text
        list_answers = answer.split(":")
        if len(list_answers) == 2:
            await message.answer(text="<i>Проверяем аккаунт...</i>")

            accs = await db.check_bizlato_exists(answer)
            if accs[0]:
                await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                          "Попробуйте еще раз...", reply_markup=back_keyboard)
                await AddAcc.InputAcc.set()
            else:
                await db.create_bizlato_acc(
                    user_id=message.from_user.id,
                    bizlato_acc=answer
                )
                await state.finish()
                if data.get("return_qiwi"):
                    user_id = message.from_user.id
                    check_for_accs = await db.show_bizlato_accs(user_id)
                    markup = await bizlato_accs_keyboard(check_for_accs)
                    await message.answer(text="<i>Обрабатывается запрос...</i>", reply_markup=cancel_keyboard)
                    await message.answer(text="<b>Выберите аккаунт Bitzlato</b>", reply_markup=markup)
                    await QiwiSettings.InputBizlatoAcc.set()
                else:
                    await message.answer(text="<i>Аккаунт был успешно добавлен</i>", reply_markup=start_keyboard)
                    await message.answer(text="<b>Настройки Bitzlato</b>", reply_markup=bizlato_keyboard)
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=back_keyboard)
            await AddAcc.InputAcc.set()
