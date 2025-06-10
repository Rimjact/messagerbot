from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.model.states.mailing import MailingForAllUsers, MailingForUsers, MailingForGroups


handlers_mailing_router = Router(name=__name__)


@handlers_mailing_router.message(F.text == '✉Сформировать рассылку')
async def mailing(message: Message):
    """Обработчик комманды на формирование рассылки."""

    pass


#####################################
###  РАССЫЛКА ВСЕМ ПОЛЬЗОВАТЕЛЯМ  ###
#####################################
@handlers_mailing_router.callback_query(F.data == 'make_mailing_all_users')
async def mailing_all_users_start(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на начало рассылки всем пользователям."""

    pass


@handlers_mailing_router.message(MailingForAllUsers.text)
async def mailing_all_users_message(message: Message, state: FSMContext):
    """Обработчик сообщения, для получения текста, который
    будет рассылатся.
    """

    pass


###########################################
###  РАССЫЛКА КОНКРЕТНЫМ ПОЛЬЗОВАТЕЛЯМ  ###
###########################################
@handlers_mailing_router.callback_query(F.data == 'make_mailing_users')
async def mailing_users(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на начало рассылки конкретным пользователям."""

    pass


@handlers_mailing_router.message(MailingForUsers.telegram_ids)
async def mailing_users_telegram_ids(message: Message, state: FSMContext):
    """Обработчик сообщения, для получения Telegram ID пользователей,
    которым будет отослана рассылка.
    """

    pass


@handlers_mailing_router.message(MailingForUsers.text)
async def mailing_users_message(message: Message, state: FSMContext):
    """Обработчик сообщения, для получения текста, который
    будет рассылатся.
    """

    pass


###########################################
###     РАССЫЛКА КОНКРЕТНЫМ ГРУППАМ     ###
###########################################
@handlers_mailing_router.callback_query(F.data == 'make_mailing_groups')
async def mailing_groups(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на начало рассылки конкретным группам."""

    pass


@handlers_mailing_router.message(MailingForGroups.groups_ids)
async def mailing_groups_ids(message: Message, state: FSMContext):
    """Обработчик сообщения, для получения ID групп,
    пользователям которых будет отослана рассылка."""

    pass


@handlers_mailing_router.message(MailingForUsers.text)
async def mailing_groups_message(message: Message, state: FSMContext):
    """Обработчик сообщения, для получения текста, который
    будет рассылатся.
    """

    pass