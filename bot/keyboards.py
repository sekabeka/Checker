from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_item_keyboard(url: str) -> InlineKeyboardMarkup:
    item_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Go to product',
                    url=url
                )
            ],
            [
                InlineKeyboardButton(
                    text='Remove this product',
                    callback_data=''
                )
            ]
        ]
    )
    return item_keyboard



