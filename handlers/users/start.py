from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default import start_keyboard
from loader import dp


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=start_keyboard)
