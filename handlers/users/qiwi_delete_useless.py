from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.inline import qiwi_keyboard
from loader import dp, db, bot
from states import QiwiSettings


@dp.callback_query_handler(state=QiwiSettings.DeleteUseless)
async def delete_wallet(message: types.CallbackQuery, state=FSMContext):
    await message.answer()
    call_data = message.data
    if call_data == "delete_useless":
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        data = await state.get_data()
        useless_wallets = data.get("useless_wallets")
        bitzlato_acc = data.get("api_key")
        for wallet in useless_wallets:
            await db.delete_qiwi_wallet(bitzlato_acc, wallet)
        await db.select_all_account()
        await state.reset_data()
        new_data = await state.get_data()
        print(new_data)
        await state.update_data(
            {
                "api_key": bitzlato_acc,
                "user_id": message.from_user.id
            }
        )
        sup_data = await state.get_data()
        print(sup_data)
        await QiwiSettings.InputOption.set()
        await message.message.answer(text="Кошельки были удалены", reply_markup=start_keyboard)
        await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()

    elif call_data == "back":
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await message.message.answer(text="Вы отменили удаление кошельков", reply_markup=start_keyboard)
        await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()
