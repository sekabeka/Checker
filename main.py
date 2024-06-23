import asyncio
import logging

from aiogram import Dispatcher, Bot

from sources.dns.checker import DNS

logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG)


async def main():
    global dns, bot
    dns = DNS()
    bot = Bot()
    