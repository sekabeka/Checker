import asyncio

from os import getenv
from aiogram import Dispatcher, Bot
from playwright.async_api import async_playwright, BrowserContext
from aiohttp import ClientSession
from typing import List

from sources.dns.handlers import dns_router
from bot.handlers import router

from dotenv import load_dotenv

load_dotenv()

bot_token = getenv('BOT_TOKEN')
dp = Dispatcher()




async def main():

    dp.include_routers(
        dns_router,
        router
    )
    bot = Bot(bot_token)
    



