from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Настройки Qiwi"),
            KeyboardButton(text="Настройки Bitzlato"),
        ],
        [
            KeyboardButton(text="Параметры торговли")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True,

)

cancel_keyboard = ReplyKeyboardRemove()
