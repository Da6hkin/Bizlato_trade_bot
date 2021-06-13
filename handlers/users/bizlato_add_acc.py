import asyncpg.exceptions
import requests
from aiogram.dispatcher import FSMContext
from keyboards.default import cancel_keyboard, start_keyboard
from keyboards.inline import qiwi_keyboard, bizlato_keyboard
from loader import dp, bot, db
from aiogram import types
from states import AddAcc


@dp.callback_query_handler(state=AddAcc.ButtonAdd)
async def bizlato_add_button(call: types.CallbackQuery,state=FSMContext):
    await call.answer(cache_time=30)
    await call.message.answer(text="Введите данные Bizlato Кошелька\n"
                                   "<b>Формат</b> <code>&lt;personId&gt;:&lt;API_KEY&gt;</code> \n"
                                   "<i>personId - номер вашего кошелька без знака '+'\n"
                                   "API_KEY - OAuth-токен выданный вам для доступа к вашему QIWI кошельку.</i>")
    await AddAcc.InputAcc.set()

@dp.message_handler(state=AddAcc.InputAcc)
async def input_bizlato_acc(message: types.Message, state=FSMContext):
    answer = message.text
    if answer == "Отменить":
        await state.finish()
        await message.answer(text="Вы отменили действие", reply_markup=start_keyboard)
        await message.answer(text="Настройки Bitzlato", reply_markup=bizlato_keyboard)

    else:
        list_answers = answer.split(":")
        if len(list_answers) == 2:
            await message.answer(text="<i>Проверяем аккаунт...</i>")

            accs = await db.check_bizlato_exists(answer)
            if accs[0]:
                await message.answer(text="Данный аккаунт уже зарегистрирован в базе\n"
                                          "Попробуйте еще раз...", reply_markup=cancel_keyboard)
            else:
                await db.create_bizlato_acc(
                    user_id=message.from_user.id,
                    bizlato_acc=answer
                )
                await state.finish()
                await message.answer(text="Аккаунт был успешно добавлен",reply_markup=start_keyboard)
                await message.answer(text="Настройки Bitzlato", reply_markup=bizlato_keyboard)
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=cancel_keyboard)
            await AddAcc.InputAcc.set()
