from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Настройки Qiwi"),
            KeyboardButton(text="Настройки Bizlato"),
        ],
        [
            KeyboardButton(text="Параметры торговли")
        ],
    ],
    one_time_keyboard=True,
    resize_keyboard=True,

)
