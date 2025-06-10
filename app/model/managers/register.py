import app.view.answers.register as reg_answers
import app.model.database.requests as db_requests

import app.model.utils as utils

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.model.states.register import RegisterStates
from app.model.managers.properties import async_is_forms_acceptance_blocked


async def on_register_start_executed(callback: CallbackQuery, state: FSMContext):
    """Обработчик вызова запроса на начало регистрации."""

    user_tg_id: int = callback.from_user.id

    if await db_requests.async_is_user_exist(user_tg_id):
        await reg_answers.on_register_start_processed(callback, state, 'user_exist')
        return

    if await db_requests.async_is_user_form_exist(user_tg_id):
        await reg_answers.on_register_start_processed(callback, state, 'user_from_exist')
        return

    if await async_is_forms_acceptance_blocked():
        await reg_answers.on_register_start_processed(callback, state, 'forms_acceptance_blocked')
        return

    await reg_answers.on_register_start_processed(callback, state)


async def on_register_full_name_entered(message: Message, state: FSMContext):
    """Обработчик ввода регистрации ФИО пользователя."""

    full_name_text: str = message.text
    if not utils.is_string_valid(full_name_text):
        await reg_answers.on_register_full_name_processed(message, state, 'invalid_string')
        return

    await reg_answers.on_register_full_name_processed(message, state)


async def on_register_email_entered(message: Message, state: FSMContext):
    """"""