import aiogram.utils.formatting as fm
import urllib.parse

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from src.database import collection
from src.bot.variables import DOMAINS, MAX_URLS

router = Router()

@router.message(CommandStart())
async def welcome(message: Message):
    await message.answer(
        **fm.as_list(
            fm.Text('Привет, ', fm.Bold(message.from_user.full_name + '!')),
            'Можешь прислать мне ссылку из DNS и я начну отслеживать для тебя цену на товар.'
        ).as_kwargs()
    )
    _id = message.from_user.id
    if await collection.find_one({'id' : _id}) is None:
        await collection.insert_one({
            'id' : _id,
            'urls' : []
        })

    

@router.message(F.text.startswith('http'))
async def add_url(message: Message):
    url = message.text
    domain  = urllib.parse.urlparse(url).netloc

    if domain not in DOMAINS:
        await message.answer(
            'Этот домен не обслуживается.'
        )
        return
    
    _id = message.from_user.id
    count_of_tracked_urls = len((await collection.find_one({'id' : _id}))['urls'])
    if count_of_tracked_urls < MAX_URLS:
        await collection.update_one(
            {'id' : _id},
            {'$addToSet' : {'urls' : url}}
        )
        await message.answer(
            'Ссылка добавлена для мониторинга.'
        )
    else:
        await message.answer(
            "Достигнуто максимальное количество возможно отслеживаемых товаров."
        )
        



    

   
