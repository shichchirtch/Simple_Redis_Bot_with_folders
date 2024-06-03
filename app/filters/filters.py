from aiogram.filters import BaseFilter
from aiogram.types import Message
from external_functions.external_functions import check_user_in_table


class DATA_IS_DIGIT(BaseFilter):
    async def __call__(self, message: Message):
        if message.text.isdigit() and 0 < int(message.text) < 100:
            return True
        return False

class DATA_IS_NOT_DIGIT(BaseFilter):
    async  def __call__(self, message:Message):
        if not message.text.isdigit():
            return True
        return False


class START_ONCE_ONLY(BaseFilter):
    async def __call__(self, message: Message):
        print("START_ONCE_ONLY Filter works\n\n")
        user_tg_id = message.from_user.id
        if await check_user_in_table(user_tg_id):
            return False
        return True