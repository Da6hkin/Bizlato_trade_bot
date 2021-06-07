from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import set_callback

qiwi_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Добавить кошелек", callback_data=set_callback.new(service_name="qiwi",
                                                                                     action="add_wallet")),

    ],
    [
        InlineKeyboardButton(text="Установить сумму лимита", callback_data=set_callback.new(service_name="qiwi",
                                                                                            action="set_limit")),

    ],
    [
        InlineKeyboardButton(text="Выбрать кошельки для работы",
                             callback_data=set_callback.new(service_name="qiwi", action="choose_wallets")),

    ],
    [
        InlineKeyboardButton(text="Удалить Кошелек", callback_data=set_callback.new(service_name="qiwi",
                                                                                    action="delete_wallet")),

    ]
])
