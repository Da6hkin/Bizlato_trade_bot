from aiogram.dispatcher.filters.state import StatesGroup, State


class AddWallet(StatesGroup):
    InputBizlatoAcc = State()
    InputWallet = State()


