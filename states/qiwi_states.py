from aiogram.dispatcher.filters.state import StatesGroup, State


class QiwiSettings(StatesGroup):
    InputBizlatoAcc = State()
    InputOption = State()
    AddWallet = State()


