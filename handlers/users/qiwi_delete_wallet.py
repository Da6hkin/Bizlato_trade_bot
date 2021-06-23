
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import start_keyboard
from keyboards.inline import back_keyboard, qiwi_keyboard
from loader import dp, db, bot
from states import QiwiSettings


@dp.callback_query_handler(state=QiwiSettings.DeleteWallet)
async def delete_wallet(message: types.CallbackQuery, state=FSMContext):
    await message.answer()
    data = await state.get_data()
    api_key = data.get("api_key")
    call_data = message.data
    wallets = await db.show_wallets(api_key)
    if call_data == "back":
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await message.message.answer(text="Вы отменили удаление кошелька", reply_markup=start_keyboard)
        await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()
    elif call_data in wallets[0]:

        await db.delete_qiwi_wallet(api_key, call_data)
        await message.message.answer(text="<i>Кошелек был успешно удален</i>", reply_markup=start_keyboard)
        print(await db.select_all_account())
        await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await QiwiSettings.DeleteWallet.set()
