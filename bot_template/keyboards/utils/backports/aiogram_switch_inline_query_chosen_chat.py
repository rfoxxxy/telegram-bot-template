from aiogram.types import fields
from aiogram.types.base import Boolean, String, TelegramObject


class SwitchInlineQueryChosenChat(TelegramObject):
    query: String = fields.Field()
    allow_user_chats: Boolean = fields.Field()
    allow_bot_chats: Boolean = fields.Field()
    allow_group_chats: Boolean = fields.Field()
    allow_channel_chats: Boolean = fields.Field()
