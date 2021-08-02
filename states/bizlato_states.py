from aiogram.dispatcher.filters.state import StatesGroup, State


class AddAcc(StatesGroup):
    ButtonAdd = State()
    InputEmail = State()
    InputKid = State()
    InputAcc = State()
    InputCode = State()
    Accept_acc = State()

class DeleteAcc(StatesGroup):
    ChooseAcc = State()

class ChangeCode(StatesGroup):
    ChooseAcc = State()
    InputCode = State()
    AcceptCode = State()

