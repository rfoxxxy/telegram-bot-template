from typing import Union

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, Message

from bot_template import dp


class ChatAdminFilter(BoundFilter):
    key = "is_chat_admin"

    def __init__(self, chat_admin: bool):
        self.chat_admin = chat_admin

    async def check(self, event: Union[Message, CallbackQuery]) -> bool:
        msg = event.message if isinstance(event, CallbackQuery) else event
        if msg.chat.id == msg.from_user.id:
            return True and self.chat_admin
        else:
            member = await msg.chat.get_member(event.from_user.id)
            if (
                isinstance(event, Message)
                and not member.is_chat_admin()
                and self.chat_admin
            ):
                return False
            return member.is_chat_admin() and self.chat_admin


dp.filters_factory.bind(
    ChatAdminFilter,
    event_handlers=[dp.message_handlers, dp.callback_query_handlers],
)
