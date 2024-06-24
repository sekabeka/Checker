from aiogram.fsm.state import State, StatesGroup

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

class StartSG(StatesGroup):
    greeting = State()

welcome_dialog = Dialog(
    Window(
        Const('Hello'),
        Button(text=Const('some button'), id='welcome'),
        state=StartSG.greeting
    )
)