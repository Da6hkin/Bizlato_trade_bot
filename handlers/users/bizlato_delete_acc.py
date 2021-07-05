from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.inline import bizlato_keyboard
from loader import dp, bot, db
from states import DeleteAcc


@dp.callback_query_handler(state=DeleteAcc.ChooseAcc)
async def select_bitzlato_acc(call: types.CallbackQuery, state=FSMContext):
    await call.answer()
    call_data = call.data
    bizlato_emails = await db.show_bizlato_accs(call.from_user.id)
    print(call_data)
    print(bizlato_emails[0])
    print(bizlato_emails[0][0])
    if call_data == "back":
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.message.answer(text="Настройки Bitzlato:", reply_markup=bizlato_keyboard)

    elif call_data in bizlato_emails[0][0]:
        await state.finish() 
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await db.delete_bizlato_acc(call_data)
        await call.message.answer(text="<i>Аккаунт был успешно удален</i>", reply_markup=start_keyboard)
        print(await db.select_all_account())
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await DeleteAcc.ChooseAcc.set()
