from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.model.managers.start import on_start_command_entered

handlers_start_router = Router(name=__name__)


@handlers_start_router.message(CommandStart())
async def start(message: Message):
    """Обработчик комманды <code>/start</code>."""

    await on_start_command_entered(message)