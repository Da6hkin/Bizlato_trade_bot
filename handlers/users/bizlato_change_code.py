from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.inline import bizlato_keyboard, back_keyboard, bizlato_accept_acc
from loader import dp, bot, db
from states import ChangeCode


@dp.callback_query_handler(state=ChangeCode.ChooseAcc)
async def select_bitzlato_acc(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    call_data = call.data
    bizlato_emails = await db.show_bizlato_accs(call.from_user.id)
    if call_data == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Настройки Bitzlato:", reply_markup=bizlato_keyboard)

    elif call_data in bizlato_emails[0][0]:
        await state.update_data({
            "email": call_data
        })
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Введите секретный код двухфакторной аутентификации:",
                                  reply_markup=back_keyboard)
        await ChangeCode.InputCode.set()
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await ChangeCode.ChooseAcc.set()


@dp.message_handler(state=ChangeCode.InputCode)
@dp.callback_query_handler(state=ChangeCode.InputCode)
async def input_bizlato_code(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    answer_type = type(message)
    if answer_type == types.CallbackQuery:
        if message.data == "back":
            await state.finish()
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Настройки Bitzlato:", reply_markup=bizlato_keyboard)
        else:
            await message.answer()
    elif answer_type == types.Message:
        answer = message.text
        await state.update_data({
            "code": answer
        })
        await message.answer(text=f"Вы указали {answer}", reply_markup=bizlato_accept_acc)
        await ChangeCode.AcceptCode.set()


@dp.callback_query_handler(state=ChangeCode.AcceptCode)
async def change_google_code(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    call_data = call.data
    if call_data == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Настройки Bitzlato:", reply_markup=bizlato_keyboard)

    elif call_data == "accept_acc":
        new_data = await state.get_data()
        email = new_data.get("email")
        code = new_data.get("code")
        await state.finish()
        await db.update_bizlato_code(code, email)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="<i>Секретный код был изменен</i>", reply_markup=start_keyboard)

    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await ChangeCode.AcceptCode.set()
