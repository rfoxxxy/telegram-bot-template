import asyncio
from typing import List

import babel.numbers
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from babel.core import Locale

try:
    from sqlalchemy.exc import OperationalError
except ImportError:
    pass

from bot_template import config
from bot_template.keyboards.database import database
from bot_template.keyboards.exceptions import UnsupportedTypeError
from bot_template.keyboards.models.base import BaseKeyboardButton, ButtonRow
from bot_template.keyboards.utils import KeyboardMarkupMixin, get_pay_text
from bot_template.keyboards.utils.backports.aiogram_inline_keyboard_button import (
    InlineKeyboardButton,
)
from bot_template.keyboards.utils.backports.aiogram_switch_inline_query_chosen_chat import (
    SwitchInlineQueryChosenChat,
)
from bot_template.utils import run_async


class CallbackButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(self, text: str, callback_data: str, **kwargs):
        super().__init__(
            "callback", text, callback_data, additional_data=kwargs
        )

    async def __encode_data(self, data: str, additional_data: dict) -> str:
        if config.get_item("features", "use_modern_callback"):
            try:
                callback = await database.add_callback(data, additional_data)
            except OperationalError:
                await database.init_database()
                return await self.__encode_data(data, additional_data)
            return callback.query  # type: ignore
        return data

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(
            self.text,
            callback_data=await self.__encode_data(
                self.callback_data, self.additional_data
            ),
        )


class SwitchInlineButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(self, text: str, switch_inline_query: str):
        super().__init__(
            "switch_inline_query",
            text,
            switch_inline_query=switch_inline_query,
        )

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(
            self.text, switch_inline_query=self.switch_inline_query
        )


class SwitchInlineCurrentChatButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(self, text: str, switch_inline_query: str):
        super().__init__(
            "switch_inline_query_current_chat",
            text,
            switch_inline_query=switch_inline_query,
        )

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(
            self.text,
            switch_inline_query_current_chat=self.switch_inline_query,
        )


class SwitchInlineChosenChatButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(
        self,
        text: str,
        switch_inline_query: str,
        allow_user_chats: bool = True,
        allow_bot_chats: bool = True,
        allow_group_chats: bool = True,
        allow_channel_chats: bool = True,
    ):
        self.allow_user_chats = allow_user_chats
        self.allow_bot_chats = allow_bot_chats
        self.allow_group_chats = allow_group_chats
        self.allow_channel_chats = allow_channel_chats
        super().__init__(
            "switch_inline_query_chosen_chat",
            text,
            switch_inline_query=switch_inline_query,
        )

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(
            self.text,
            switch_inline_query_chosen_chat=SwitchInlineQueryChosenChat(
                query=self.switch_inline_query,
                allow_user_chats=self.allow_user_chats,
                allow_bot_chats=self.allow_bot_chats,
                allow_group_chats=self.allow_group_chats,
                allow_channel_chats=self.allow_channel_chats,
            ),
        )


class UserProfileButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(self, text: str, user_id: int):
        super().__init__("url", text, url=f"tg://user?id={user_id}")

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(self.text, url=self.url)


class PayButton(BaseKeyboardButton):
    """Inline keyboard button object"""

    def __init__(self, price: float, val: str, locale: str | Locale = None):
        if not locale:
            locale = types.User.get_current().locale
        super().__init__(
            "payment",
            f"{get_pay_text(str(locale))} {babel.numbers.format_currency(price, val, locale=locale)}",
        )

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(self.text, pay=True)


class URLButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(self, text: str, url: str):
        super().__init__("url", text, url=url)

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(self.text, url=self.url)


class URLPayButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(
        self, price: float, val: str, url: str, locale: str | Locale = None
    ):
        if not locale:
            locale = types.User.get_current().locale
        super().__init__(
            "url",
            f"{get_pay_text(str(locale))} {babel.numbers.format_currency(price, val, locale=locale)}",
            url=url,
        )

    async def build_button(self, ctx):
        if type(ctx).__name__ == "BottomKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return InlineKeyboardButton(self.text, url=self.url)


class InlineKeyboard(KeyboardMarkupMixin):
    __slots__ = ["rows"]

    def __init__(self, *args: ButtonRow) -> None:
        self.rows: List[ButtonRow] = list(args) if args else []

    async def build(self) -> "InlineKeyboardMarkup":
        """Build keyboard markup

        Raises:
            UnsupportedTypeError: if specified unsupported button type

        Returns:
            InlineKeyboardMarkup: aiogram keyboard markup object
        """
        keyboard = InlineKeyboardMarkup()
        for row in self.rows:
            buttons = await asyncio.gather(
                *[btn.build_button(self) for btn in row.buttons]
            )
            keyboard.row(*buttons)
        return keyboard

    def _build(self) -> InlineKeyboardMarkup:
        """
        Synchronously builds keyboard markup
        """
        return run_async(self.build)
