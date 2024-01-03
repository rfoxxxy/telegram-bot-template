import inspect

from bot_template.keyboards.models import (
    bottom_keyboard,
    inline_keyboard,
    multi_keyboard,
)
from bot_template.keyboards.models.base import (
    BaseKeyboardButton,
    ButtonRegistry,
)


def auto_register_buttons():
    for module in [bottom_keyboard, inline_keyboard, multi_keyboard]:
        for _, obj in inspect.getmembers(module):
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseKeyboardButton)
                and obj is not BaseKeyboardButton
            ):
                ButtonRegistry.register(obj.__name__, obj)
