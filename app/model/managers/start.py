import app.model.utils as utils

from aiogram.types import Message

from app.view.answers.start import on_start_command_processed


async def on_start_command_entered(message: Message):
    """Обработчик сигнала ввода комманды <code>/start</code>."""

    user_tg_id: int = message.from_user.id

    if utils.is_user_has_admin_privileges(user_tg_id):
        await on_start_command_processed(message, is_admin=True)
        return

    await on_start_command_processed(message, is_admin=False)