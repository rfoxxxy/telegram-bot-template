from aiogram import flags, types
from aiogram.filters.command import Command

from bot_template import dp
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
@flags.use_database
async def start_handler(message: types.Message, user: User):
    return await message.reply(
        f"hello, {user.name}! <b>some</b> <i>test</i>\n<u>moment</u>"
    )


@dp.message(Command("test"))
@flags.use_database
async def test_handler(message: types.Message, user: User):
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
            WebAppButton("open", "https://lossless-pay-test.neonteam.cc/pay"),
        ),
        ButtonRow(URLPayButton(10000, "USD", "https://google.com")),
    )
    return await message.reply("test!", reply_markup=await keyboard.build())
