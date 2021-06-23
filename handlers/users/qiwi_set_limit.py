from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import start_keyboard
from keyboards.inline import qiwi_keyboard, back_keyboard
from loader import dp, bot, db
from states import QiwiSettings


@dp.message_handler(state=QiwiSettings.InputLimit)
@dp.callback_query_handler(state=QiwiSettings.InputLimit)
async def input_qiwi_wallet(message: Union[types.Message, types.CallbackQuery], state=FSMContext):
    answer_type = type(message)
    if answer_type == types.CallbackQuery:
        if message.data == "back":
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.message.answer(text="Вы отменили добавление кошелька", reply_markup=start_keyboard)
            await message.message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
            await QiwiSettings.InputOption.set()
        else:
            await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
            await message.answer()
            await QiwiSettings.InputLimit.set()
    elif answer_type == types.Message:
        answer = message.text
        if answer.isnumeric():
            limit = int(answer)
            if limit > 0:
                data = await state.get_data()
                api_key = data.get("api_key")
                check_for_qiwi = await db.show_wallets(api_key)
                k = 0
                for wallet in check_for_qiwi[0]:
                    wallet_string = wallet.split(":")
                    new_wallet = wallet_string[0] + ":" + wallet_string[1] + ":" + wallet_string[2] + ":" + answer
                    await db.delete_qiwi_wallet(api_key, wallet)
                    if k == 0:
                        await db.create_qiwi_wallet(api_key, new_wallet)
                        k += 1
                    else:
                        await db.add_qiwi_wallet(api_key, new_wallet)
                await db.select_all_account()
                await message.answer(text=f"Лимит в <b>{limit}</b> был установлен\n", reply_markup=start_keyboard)
                await message.answer(text="<b>Настройки Qiwi</b>", reply_markup=qiwi_keyboard)
                await QiwiSettings.InputOption.set()
            else:
                await message.answer(text="Укажите <b>лимит</b> в формате числа более единицы:",
                                     reply_markup=back_keyboard)
                await QiwiSettings.InputLimit.set()
        else:
            await message.answer(text="Неправильные формат данных...\n"
                                      "Попробуйте еще раз", reply_markup=back_keyboard)
            await QiwiSettings.InputLimit.set()
