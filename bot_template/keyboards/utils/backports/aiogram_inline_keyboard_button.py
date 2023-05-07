from aiogram.types import InlineKeyboardButton as InlineButton
from aiogram.types import fields

from bot_template.keyboards.utils.backports.aiogram_switch_inline_query_chosen_chat import (
    SwitchInlineQueryChosenChat,
)


class InlineKeyboardButton(InlineButton):
    switch_inline_query_chosen_chat: SwitchInlineQueryChosenChat = (
        fields.Field(base=SwitchInlineQueryChosenChat)
    )
