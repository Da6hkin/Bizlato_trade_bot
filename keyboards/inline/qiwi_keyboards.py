from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import set_callback

qiwi_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показать кошельки", callback_data=set_callback.new(service_name="qiwi",
                                                                                      action="show_wallets")),
    ],
    [
        InlineKeyboardButton(text="Добавить кошелек", callback_data=set_callback.new(service_name="qiwi",
                                                                                     action="add_wallet")),

    ],
    [
        InlineKeyboardButton(text="Удалить Кошелек", callback_data=set_callback.new(service_name="qiwi",
                                                                                    action="delete_wallet")),

    ],
    [
        InlineKeyboardButton(text="Установить сумму лимита", callback_data=set_callback.new(service_name="qiwi",
                                                                                            action="set_limit")),

    ],
    [
        InlineKeyboardButton(text="Очистить базу ненужных кошельков",
                             callback_data=set_callback.new(service_name="qiwi", action="useless_wallets")),

    ],

    [
        InlineKeyboardButton(text="Сменить аккаунт Bitzlato", callback_data=set_callback.new(service_name="qiwi",
                                                                                             action="change_acc")),
    ],
])

back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Назад", callback_data="back")
    ]
])

useless_wallets_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Удалить", callback_data="delete_useless")
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data="back")
    ],
])


async def qiwi_wallets_keyboard(list_qiwi):
    markup = InlineKeyboardMarkup()
    print("list_qiwi-",list_qiwi)
    if list_qiwi[0] is None:
        markup.insert(
            InlineKeyboardButton(text="Добавить кошелек",
                                 callback_data=set_callback.new(service_name="qiwi",
                                                                action="add_wallet"))
        )
        markup.insert(InlineKeyboardButton(text="Назад", callback_data="back"))
    else:
        for qiwi_wallet in list_qiwi[0]:
            qiwi_number = qiwi_wallet.split(":")
            button_text = qiwi_number[0]
            callback = qiwi_wallet
            markup.insert(
                InlineKeyboardButton(text=button_text, callback_data=callback)
            )
        markup.insert(InlineKeyboardButton(text="Назад", callback_data="back"))
    return markup
