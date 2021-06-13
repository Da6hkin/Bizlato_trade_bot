from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAcc(StatesGroup):
    ButtonAdd = State()
    InputAcc = State()
