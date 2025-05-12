import asyncio
import logging

from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()

## Токен бота от BotFather
TOKEN = getenv("BOT_TOKEN")

## Диспетчер бота
disp = Dispatcher()


async def main() -> None:
    bot_default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
    bot = Bot(token=TOKEN, default=bot_default_properties)

    await disp.start_polling(bot)


if __name__ == '__main___':
    ## Логирование для тестов
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown bot")