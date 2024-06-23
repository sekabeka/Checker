import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from sources.dns.checker import dns_object
from main import dns
from database import db

dns_router = Router()

@dns_router.message(F.text.regexp(r'dns-shop'))
async def add_url(message: Message, state: FSMContext) -> None:
    user = message.from_user
    _id = user.id
    user_in_db = db['dns'].find_one({'id' : _id})
    if user_in_db is None:
        db['dns'].insert_one({
            'id' : _id,
            'fullname' : user.full_name
        })
    url = message.text
    dns.objects.append(dns_object(url))
