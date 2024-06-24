import requests
import os
import dotenv
import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.bot.dialogs.welcome import welcome_dialog

from src.bot.handlers.base import router
from src.bot.handlers.dialog import dialog_router, other

dotenv.load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

def get_proxies_for_playwright():
    api_token = os.getenv('API_TOKEN')
    result = []
    response = requests.get(
        url=f"https://proxy6.net/api/{api_token}/getproxy"
    )
    for d in response.json()['list'].values():
        result.append({
            'username' : d["user"],
            'password' : d["pass"],
            'server' : d['host'] + ':' + d['port']
        })
    return result

dialog_router.include_router(welcome_dialog)


async def main():
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        dialog_router,
        router
    )
    bot = Bot(bot_token)
    setup_dialogs(dialog_router)
    dp.message.register(other, lambda msg: msg.text == 'sds')
    await dp.start_polling(bot)

asyncio.run(main())

