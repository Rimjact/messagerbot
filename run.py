import asyncio
import logging

from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from app.controller.handlers.start import handlers_start_router
from app.controller.handlers.register import handlers_register_router
from app.controller.handlers.formsacceptance import handlers_forms_acceptance_router
from app.controller.handlers.usersmanage import handlers_users_manage_router
from app.controller.handlers.groupsmanage import handlers_groups_manage_router
from app.controller.handlers.mailing import handlers_mailing_router

from app.model.database.db import async_main as async_db_main


TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_routers(
    handlers_start_router,
    handlers_register_router,
    handlers_forms_acceptance_router,
    handlers_users_manage_router,
    handlers_groups_manage_router,
    handlers_mailing_router
)


# Запуск бота
async def main() -> None:
    await async_db_main()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown bot")