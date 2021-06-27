from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAcc(StatesGroup):
    ButtonAdd = State()
    InputEmail = State()
    InputAcc = State()
