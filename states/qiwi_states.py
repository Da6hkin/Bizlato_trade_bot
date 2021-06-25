from aiogram.dispatcher.filters.state import StatesGroup, State


class QiwiSettings(StatesGroup):
    InputBizlatoAcc = State()
    InputOption = State()
    AddWallet = State()
    DeleteWallet = State()
    ShowWallets = State()
    InputLimit = State()
    DeleteUseless = State()



