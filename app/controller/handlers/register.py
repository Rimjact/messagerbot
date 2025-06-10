import app.model.managers.register as reg_manager

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.model.states.register import RegisterStates


handlers_register_router = Router(name=__name__)


@handlers_register_router.callback_query(F.data == 'register')
async def register_start(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на начало регистрации."""

    await reg_manager.on_register_start_executed(callback, state)


@handlers_register_router.message(RegisterStates.full_name)
async def register_full_name(message: Message, state: FSMContext):
    """Обработчик ввода фамилии, имени и отчества от пользователя."""

    await reg_manager.on_register_full_name_entered(message, state)


@handlers_register_router.message(RegisterStates.email)
async def register_email(message: Message, state: FSMContext):
    """Обработчик ввода адреса электронной почты от пользователя."""

    pass


@handlers_register_router.callback_query(F.data.contains('form_accept_'))
async def register_form_accepted(callback: CallbackQuery):
    """Обработчик запроса на принятие заявки на регистрацию."""

    pass


@handlers_register_router.callback_query(F.data.contains('form_reject_'))
async def register_form_rejected(callback: CallbackQuery):
    """Обработчик запроса на отклонение заявки на регистрацию."""

    pass
