from aiogram import Router, F
from aiogram.types import Message


handlers_forms_acceptance_router = Router(name=__name__)


@handlers_forms_acceptance_router.message(F.text == '⛔Заблокировать подачу новых заявок')
async def forms_acceptance_block(message: Message):
    """Обработчик комманды блокировки приёма новых заявок на регистрацию."""

    pass


@handlers_forms_acceptance_router.message(F.text == '✅Разблокировать подачу новых заявок')
async def forms_acceptance_unblock(message: Message):
    """Обработчик комманды разблокировки приёма новых заявок на регистрацию."""

    pass