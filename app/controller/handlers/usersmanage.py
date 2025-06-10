from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.model.states.users import UserChangeDataStates, UserChangeGroupStates, UserDeleteStates

handlers_users_manage_router = Router(name=__name__)


@handlers_users_manage_router.message(F.text == '🧍‍♂️🧍‍♀️Управление пользователями')
async def users_manage(message: Message):
    """Обработчик комманды на управление пользователями."""

    pass


#######################################
###  ИЗМЕНЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ  ###
#######################################
@handlers_users_manage_router.callback_query(F.data == 'manage_users_change_data')
async def users_manage_change_data(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на изменение данных пользователя."""

    pass


@handlers_users_manage_router.message(UserChangeDataStates.tg_id)
async def users_manage_change_data_telegram_id(message: Message, state: FSMContext):
    """Обработчик сообщения для получения Telegram ID пользователя,
    у которого будут изменены данные.
    """

    pass


@handlers_users_manage_router.message(UserChangeDataStates.full_name)
async def users_manage_change_data_full_name(message: Message, state: FSMContext):
    """Обработчик сообщения для получения новых
    фамилии, имени и отчества.
    """

    pass


@handlers_users_manage_router.message(UserChangeDataStates.email)
async def users_manage_change_data_email(message: Message, state: FSMContext):
    """Обработчик сообщения для получения нового
    адреса электронной почты.
    """

    pass


#######################################
###  ИЗМЕНЕНИЕ ГРУППЫ ПОЛЬЗОВАТЕЛЯ  ###
#######################################
@handlers_users_manage_router.callback_query(F.data == 'manage_users_change_group')
async def users_manage_change_group(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на изменение группы пользователя."""

    pass


@handlers_users_manage_router.message(UserChangeGroupStates.tg_id)
async def users_manage_change_group_telegram_id(message: Message, state: FSMContext):
    """Обработчик сообщения для указания Telegram ID пользователя,
    группа которого будет изменена.
    """

    pass


@handlers_users_manage_router.message(UserChangeGroupStates.group_id)
async def users_manage_change_group_id(message: Message, state: FSMContext):
    """Обработчик сообщения для указания ID группы,
    которая будет присвоена пользователю.
    """

    pass


######################################
###  УДАЛЕНИЕ ДАННЫХ ПОЛЬЗОВАТЕЛЯ  ###
######################################
@handlers_users_manage_router.callback_query(F.data == 'manage_users_delete')
async def users_manage_delete(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на удаление данных пользователя."""

    pass


@handlers_users_manage_router.message(UserDeleteStates.tg_id)
async def users_manage_delete_telegram_id(message: Message, state: FSMContext):
    """Обработчик сообщения для указания Telegram ID пользователя,
    данные которого будут удалены.
    """

    pass


####################################
###  ВЫВОД СПИСКА ПОЛЬЗОВАТЕЛЕЙ  ###
####################################
@handlers_users_manage_router.callback_query(F.data == 'manage_users_list')
async def users_list(callback: CallbackQuery):
    """Обработчик запроса на вывод списка
    зарегистрированных пользователей
    """

    pass