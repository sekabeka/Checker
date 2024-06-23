import asyncio

from os import getenv
from aioconsole import ainput
from aiogram import Dispatcher, Bot
from playwright.async_api import async_playwright, BrowserContext
from aiohttp import ClientSession
from typing import List

#from sources.dns.handlers import dns_router
#from bot.handlers import router
from sources.dns.checker import DNS, dns_object


from dotenv import load_dotenv

load_dotenv()

# bot_token = getenv('BOT_TOKEN')
# dp = Dispatcher()


async def sss():
    while True:
        url = await ainput('URL: ')
        obj.objects.append(
            dns_object(url)
        )
        await asyncio.sleep(0.1)



async def main():
    global obj
    obj = DNS(
        [
            dns_object('https://www.dns-shop.ru/product/2dfa4e2208833332/zasitnaa-plenka-deppa-dla-smarterra-fitmaster-5/'),
            dns_object('https://www.dns-shop.ru/product/acde03a252aeed20/61-smartfon-apple-iphone-15-128-gb-cernyj/')
        ]
    )
    asyncio.create_task(sss())
    await obj.parse()

    # dp.include_routers(
    #     dns_router,
    #     router
    # )
    # bot = Bot(bot_token)

    return 

asyncio.run(main())



