from aiogram import types
from aiogram.filters.command import Command

from bot_template import db, dp
from bot_template.database.models import User
from bot_template.keyboards.models import (
    ButtonRow,
    CallbackButton,
    InlineKeyboard,
    MarkdownViewWebAppButton,
    URLPayButton,
    WebAppButton,
)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    return await message.reply("hello, world!")


@dp.message(Command("test"))
async def test_handler(
    message: types.Message, session: db.Session, user: User
):
    keyboard = InlineKeyboard(
        ButtonRow(
            MarkdownViewWebAppButton(
                "Read me",
                "https://raw.githubusercontent.com/rfoxxxy/telegram-bot-template/main/README.md",
            )
        ),
        ButtonRow(
            CallbackButton(
                "test callback",
                "test_callback",
                action="show_username",
                user=user,
            ),
            WebAppButton("test webapp", "https://google.com"),
        ),
        ButtonRow(URLPayButton(10000, "USD", "https://google.com")),
    )
    return await message.reply("test!", reply_markup=await keyboard.build())
