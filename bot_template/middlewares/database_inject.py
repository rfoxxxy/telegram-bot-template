from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import (
    CallbackQuery,
    ChosenInlineResult,
    InlineQuery,
    Message,
)

from bot_template import db, dp


class DatabaseInjectorMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [
                CallbackQuery | ChosenInlineResult | InlineQuery | Message,
                Dict[str, Any],
            ],
            Awaitable[Any],
        ],
        event: CallbackQuery | ChosenInlineResult | InlineQuery | Message,
        data: Dict[str, Any],
    ) -> Any:
        data["session"] = db.Session()
        await handler(event, data)
        if data.get("session"):
            await data["session"].close()  # type: ignore


dp.message.middleware(DatabaseInjectorMiddleware())
dp.callback_query.middleware(DatabaseInjectorMiddleware())
dp.inline_query.middleware(DatabaseInjectorMiddleware())
dp.chosen_inline_result.middleware(DatabaseInjectorMiddleware())
