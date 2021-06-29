from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.inline import qiwi_keyboard
from loader import dp, db, bot
from states import QiwiSettings


@dp.callback_query_handler(state=QiwiSettings.ShowWallets)
async def delete_wallet(message: types.CallbackQuery, state=FSMContext):
    await message.answer()
    call_data = message.data
    if call_data == "back":
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await message.message.answer(text="Вы вернулись назад", reply_markup=start_keyboard)
        await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
        await QiwiSettings.InputOption.set()
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await QiwiSettings.ShowWallets.set()
