from typing import Any, Awaitable, Callable, Dict

import sentry_sdk
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from bot_template import config, dp


class SentryContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if (
            (not event.message)
            and (not event.callback_query)
            and (not event.inline_query)
            and (not event.my_chat_member)
            and (not event.chosen_inline_result)
        ):
            return

        from_user = (
            event.message
            or event.callback_query
            or event.inline_query
            or event.my_chat_member
            or event.chosen_inline_result
        ).from_user

        sentry_sdk.set_user(
            {
                "name": from_user.full_name,
                "id": from_user.id,
                "username": from_user.username,
                "update": event.model_dump_json(),
            }
        )
        return await handler(event, data)


sentry_sdk.init(
    dsn=config.get_item("features.sentry", "public_key"),
    integrations=[AioHttpIntegration()],
    traces_sample_rate=config.get_item(
        "features.sentry", "traces_sample_rate"
    ),
)
dp.update.outer_middleware(SentryContextMiddleware())
