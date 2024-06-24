from aiogram import types, Router
from aiogram_dialog import DialogManager, StartMode

from src.bot.dialogs.welcome import StartSG

dialog_router =  Router()

@dialog_router.message()
async def other(message: types.Message, manager: DialogManager):
    await manager.start(StartSG.greeting, mode=StartMode.RESET_STACK)