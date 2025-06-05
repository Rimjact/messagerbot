import asyncio
import logging

from os import getenv

from aiogram import Bot, Dispatcher

from app.handlers import handlers_router
from app.database.db import async_main


TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(handlers_router)


# Запуск бота
async def main() -> None:
    await async_main()

    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown bot")