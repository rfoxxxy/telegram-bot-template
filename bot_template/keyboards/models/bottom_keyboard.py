import asyncio
from typing import List

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot_template.keyboards.exceptions import UnsupportedTypeError
from bot_template.keyboards.models.base import BaseKeyboardButton, ButtonRow
from bot_template.keyboards.utils import KeyboardMarkupMixin
from bot_template.utils import run_async


class TextButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(self, text: str):
        super().__init__("text", text)

    async def build_button(self, ctx):
        if type(ctx).__name__ == "InlineKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return KeyboardButton(text=self.text)


class RequestContactButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(self, text: str):
        super().__init__("contact", text)

    async def build_button(self, ctx):
        if type(ctx).__name__ == "InlineKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return KeyboardButton(text=self.text, request_contact=True)


class RequestLocationButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(self, text: str):
        super().__init__("location", text)

    async def build_button(self, ctx):
        if type(ctx).__name__ == "InlineKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return KeyboardButton(text=self.text, request_location=True)


class RequestPollButton(BaseKeyboardButton):
    """Bottom keyboard button object"""

    def __init__(self, text: str, poll_type: str):
        super().__init__("poll", text, poll_type=poll_type)

    async def build_button(self, ctx):
        if type(ctx).__name__ == "InlineKeyboard":
            raise UnsupportedTypeError(
                f"Type {self.type} isn't supported in {type(ctx).__name__}"
            )
        return KeyboardButton(text=self.text, request_contact=True)


class BottomKeyboard(KeyboardMarkupMixin):
    __slots__ = ["rows"]

    def __init__(self, *args: ButtonRow) -> None:
        self.rows: List[ButtonRow] = list(args) if args else []

    async def build(
        self,
        resize: bool = True,
        one_time: bool = False,
        placeholder: str = None,
        selective: bool = False,
    ) -> "ReplyKeyboardMarkup":
        """Build keyboard markup

        Raises:
            UnsupportedTypeError: if specified unsupported button type

        Returns:
            ReplyKeyboardMarkup: aiogram keyboard markup object
        """
        keyboard = ReplyKeyboardBuilder()
        for row in self.rows:
            buttons = await asyncio.gather(
                *[btn.build_button(self) for btn in row.buttons]
            )
            keyboard.row(*buttons)
        return keyboard.as_markup(
            resize_keyboard=resize,
            one_time_keyboard=one_time,
            input_field_placeholder=placeholder,
            selective=selective,
        )

    def _build(self) -> ReplyKeyboardMarkup:
        """
        Synchronously builds keyboard markup
        """
        return run_async(self.build)
