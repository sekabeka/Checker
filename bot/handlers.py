import aiogram.utils.formatting as fm

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext

from database import db
from bot.functions import check_user_in_database
from classes import UserTasks


router = Router()

@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext):
    user = message.from_user
    if not check_user_in_database(user):
        user_info = {
            'id' : user.id,
            'fullname' : user.full_name
        }
        db['users'].insert_one(user_info)
        await state.update_data({
            'UserTasks' : UserTasks(user.id)
        })
    await message.answer(
        **fm.as_list(
            fm.Text('Привет, ', fm.Bold(user.full_name + '!')),
            'Я могу помочь тебе с отслеживаем цен на интересующие тебя товары.',
            fm.Text('Пока что я могу отслеживать цены лишь из ', fm.Bold('DNS'), '. Но в дальнейшем список сайтов будет расширяться.'),
            'Достаточно прислать мне ссылку из DNS на товар и я буду отслеживать изменение цены.',
            'Если цена поменятся, я уведомлю тебя об этом.',
        ).as_kwargs()
    )

#эта команда удалит вообще все отслеживаемые запросы
@router.message(Command('clear'))
async def clear_state(message: Message, state: FSMContext):
    pass


#по этой команде выводим список всех отслеживаемых товаров.
@router.message(Command('list'))
async def get_user_tasks(message: Message, state: FSMContext):
    pass

#эта команда позволит удалить отслеживаемый товар.
@router.message(Command('delete'))
async def delete_task_from_user(message: Message, state: FSMContext):
    pass

#

