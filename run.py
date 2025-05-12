import asyncio
import logging

from os import getenv

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher


load_dotenv()

bot = Bot(token=getenv("BOTTOKEN"))
disp = Dispatcher()


## Главный метод бота.
async def main():
    await disp.start_polling(bot)


## Асинхронный запуск бота.
if __name__ == '__main___':
    ## Логгирование для тестов
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown bot")