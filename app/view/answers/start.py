from aiogram.types import Message

from app.view.strings import answer_strings

from app.view.keyboards.inline import async_build_keyboard_start
from app.view.keyboards.reply import async_build_keyboard_admin


async def on_start_command_processed(message: Message, is_admin: bool):
    """Обработчик события, когда комманда <code>/start</code> обработана."""

    if is_admin:
        await message.answer(
            text=answer_strings.get('start_admin'),
            reply_markup=await async_build_keyboard_admin()
        )
        return

    await message.answer(
        text=answer_strings.get('start_user'),
        reply_markup=await async_build_keyboard_start()
    )