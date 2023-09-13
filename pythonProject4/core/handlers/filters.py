from aiogram.filters import BaseFilter
from aiogram.types import Message


class TextEqualsYesOrNo(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.lower() == 'yes' or message.text.lower() == 'no'
