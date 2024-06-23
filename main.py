import asyncio
import logging

from dotenv import load_dotenv
from os import getenv
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.mongo import MongoStorage

from sources.dns.handlers import dns_router, set_dns_checker
from database import client

logging.basicConfig(filename='log.log', filemode='w', level=logging.DEBUG)

load_dotenv()

bot_token = getenv('BOT_TOKEN')



storage = MongoStorage(client)
dp = Dispatcher(storage=storage)


async def main():
    bot = Bot(bot_token)
    dp.include_routers(
        dns_router,
    )
    dns_checker = await set_dns_checker(bot)
    task = asyncio.create_task(dns_checker.parse())
    await dp.start_polling(bot)
    
asyncio.run(main())