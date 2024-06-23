import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sources.dns.checker import dns_user, dns_item
from main import dns
from database import db

dns_router = Router()

@dns_router.message(F.text.regexp(r'dns-shop'))
async def add_url(message: Message, state: FSMContext) -> None:
    pass

    
    
