from aiogram.types import User

from database import db



def check_user_in_database(user:User) -> bool:
    id = user.id
    if db['users'].find_one({'id' : id}):
        return True
    return False


def get_user_from_database(user: User):
    return db['users'].find_one({'id' : user.id})