from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import set_callback

bizlato_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить аккаунт Bizlato", callback_data=set_callback.new(service_name="bizlato",
                                                                                             action="add_acc")),

    ],
    [
        InlineKeyboardButton(text="Удалить аккаунт Bizlato", callback_data=set_callback.new(service_name="bizlato",
                                                                                            action="delete_acc"))
    ]
])
