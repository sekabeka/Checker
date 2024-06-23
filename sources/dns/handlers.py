
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import db

dns_router = Router()

async def write_user_in_db(_id: int, fullname: str, cl_name: str = 'users') -> None:
    found_user = await db[cl_name].find_one({'id' : _id})
    if found_user is None:
        await db[cl_name].insert_one({
            'id' : _id,
            'fullname' : fullname
        })

async def add_item_for_tracking(_id: int, item: dict, cl_name: str = 'users'):
    count_of_tracking_items = len(await db[cl_name].find_one({'id' : _id})['tracking_items'])
    if count_of_tracking_items < 5:
        await db[cl_name].update_one(
            {'id' : _id},
            {'$push' : {'tracked_items' : item}}
        )

@dns_router.message()
async def add_url(message: Message, state: FSMContext) -> None:
    user = message.from_user
    _id = user.id
    fullname = user.full_name

    await state.update_data(
        {
            'name' : fullname,
            'id' : _id,
        }
    )    
    if 'tracked_items' not in await state.get_data():
        await state.update_data(
            {
                'tracked_items' : []
            }
        )  
    tracked_items: list = (await state.get_data())['tracked_items']
    tracked_items.append({
        'url' : message.text,
        'price' : 0,
        'api_url' : None
    })

    await state.update_data({
        'tracked_items' : tracked_items
    })




    

    
    
