from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

dns_router = Router()



@dns_router.message(F.text.regexp(r'dns-shop'))
async def add_url(message: Message, state: FSMContext) -> None:
    url = message.text
    data = await state.get_data()

    user_tasks = data['User']