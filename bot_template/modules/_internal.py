from aiogram import Bot, F, types
from aiogram.filters.command import Command
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext

from bot_template import dp
from bot_template.keyboards.models import ButtonRow, InlineKeyboard, URLButton


@dp.callback_query(F.data == "test_callback")
async def test_button(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get("action")
    match action:
        case "show_username":
            return await call.answer(
                f"SUCCESS!\n\nusername: @{callback_data['user'].username}",
                True,
            )
        case _:
            return await call.answer("SUCCESS!", True)


@dp.message(Command("reset_state"), StateFilter("*"))
async def start_handler(message: types.Message, state: FSMContext):
    if not await state.get_state():
        return await message.reply("no state active")
    await state.reset_state(with_data=False)
    return await message.reply("success")


@dp.inline_query(F.query == "tests")
async def test_inline_handler(query: types.InlineQuery):
    keyboard = InlineKeyboard(
        ButtonRow(URLButton("google", "https://google.com"))
    )
    return await query.answer(
        [
            types.InlineQueryResultArticle(
                id=query.id + "1",
                title="test",
                reply_markup=await keyboard.build(),
                description="test object",
                input_message_content=types.InputTextMessageContent(
                    message_text="test"
                ),
            )
        ],
        cache_time=0,
    )


@dp.chosen_inline_result()
async def test_chosen_inline_handler(
    chosen: types.ChosenInlineResult, bot: Bot
):
    await bot.edit_message_text(
        f"test successful, {chosen.from_user.full_name}!",
        inline_message_id=chosen.inline_message_id,
    )
