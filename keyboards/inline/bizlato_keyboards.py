from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import set_callback, bizlato_callback
from loader import db

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


async def bizlato_accs_keyboard(list_bizlato):
    markup = InlineKeyboardMarkup()
    if len(list_bizlato) == 0:
        markup.insert(
            InlineKeyboardButton(text="Добавить аккаунт Bitzlato",
                                 callback_data=set_callback.new(service_name="bizlato",
                                                                action="add_acc"))
        )
        markup.insert(InlineKeyboardButton(text="Назад", callback_data="back"))
    else:
        for bizlato_acc in list_bizlato:
            call_and_text = bizlato_acc[0]
            markup.insert(
                InlineKeyboardButton(text=call_and_text, callback_data=call_and_text)
            )
        markup.insert(InlineKeyboardButton(text="Назад", callback_data="back"))
    return markup
