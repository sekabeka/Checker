from aiogram.fsm.state import State, StatesGroup

class User(StatesGroup):
    username = State()
    