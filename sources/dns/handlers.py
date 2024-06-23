
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sources.dns.checker import dns_user, dns_item, DNS
from database import db

dns_router = Router()

async def set_dns_checker(bot: Bot) -> DNS:
    global dns
    dns = DNS(bot)
    return dns

MAX_ITEMS = 5

@dns_router.message()
async def add_url(message: Message, state: FSMContext) -> None:
    pass
    

    
    
