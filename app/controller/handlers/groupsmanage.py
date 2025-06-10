from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.model.states.groups import GroupNewStates, GroupChangeNameStates, GroupDeleteStates

handlers_groups_manage_router = Router(name=__name__)


@handlers_groups_manage_router.message(F.text == '📝Управление группами')
async def groups_manage(message: Message):
    """Обработчик комманды на управление группами."""

    pass


#################################
###  ДОБАВЛЕНИЕ НОВОЙ ГРУППЫ  ###
#################################
@handlers_groups_manage_router.callback_query(F.data == 'manages_groups_add_new')
async def groups_manage_add_new(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на добавление новой группы."""

    pass


@handlers_groups_manage_router.message(GroupNewStates.name)
async def groups_manage_add_new_name(message: Message, state: FSMContext):
    """Обработчик сообщения для указания названия новой группы."""

    pass


################################
###  ИЗМЕНЕНИЕ ИМЕНИ ГРУППЫ  ###
################################
@handlers_groups_manage_router.callback_query(F.data == 'manage_groups_change_name')
async def groups_manage_change_name(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на изменение имени группы."""

    pass


@handlers_groups_manage_router.message(GroupChangeNameStates.group_id)
async def groups_manage_change_name_id(message: Message, state: FSMContext):
    """Обработчик сообщения для указания ID группы,
    у которой будет имзенено название.
    """

    pass


@handlers_groups_manage_router.message(GroupChangeNameStates.new_name)
async def groups_manage_change_name_new(message: Message, state: FSMContext):
    """Обработчик сообщения для указания нового имени группы."""

    pass


#########################
###  УДАЛЕНИЕ ГРУППЫ  ###
#########################
@handlers_groups_manage_router.callback_query(F.data == 'manage_groups_delete')
async def groups_manage_delete(callback: CallbackQuery, state: FSMContext):
    """Обработчик запроса на удаление группы."""

    pass


@handlers_groups_manage_router.message(GroupDeleteStates.group_id)
async def groups_manage_delete_id(message: Message, state: FSMContext):
    """Обработчик сообщения для указания ID группы,
    которая будет удалена."""

    pass


############################
###  ВЫВОД СПИСКА ГРУПП  ###
############################
@handlers_groups_manage_router.callback_query(F.data == 'manage_groups_list')
async def groups_manage_list(callback: CallbackQuery):
    """Обработчик запроса на вывод списка всех групп."""

    pass