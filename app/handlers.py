import app.keyboards as kbs

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


handler_router = Router(name=__name__)


@handler_router.message(CommandStart())
async def start(message: Message):
    await message.reply("Добро пожаловать! Я эксперементальный бот, который занимается рассылкой сообщений зарегистрированным пользователям. Пожалуйста, выберете что-либо из пунктов ниже.",
                        reply_markup=await kbs.create_inline_keyboard_start_async())