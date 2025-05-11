import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import TOKEN


bot = Bot(token=TOKEN)
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