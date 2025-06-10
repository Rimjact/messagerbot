import app.database.requests as requests
import app.keyboards as kbs

from os import getenv

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states import CreateMailingForAllUsers, CreatingMailingForUsers, CreatingMailingForGroups, UserRegestrationStates, UserChangeDataStates, UserChangeGroupStates, UserDeleteStates, GroupAddNewStates, GroupDeleteStates, GroupChangeNameStates
from app.strings import strings
from app.utils import async_is_forms_acceptance_blocked, is_email_valid, is_valid_string, is_valid_full_name, is_valid_string_for_group_find, is_valid_ids_string, user_is_admin
from app.database.models import UserForm, User, Group
from app.emailsender import async_send_mail

handlers_router = Router(name=__name__)


@handlers_router.message(CommandStart())
async def start(message: Message):
    if user_is_admin(message.from_user.id):
        await message.reply(
            text=strings.get('start_admin'),
            reply_markup=await kbs.async_create_reply_keyboard_admin(),
            parse_mode='Markdown',
        )
        return

    await message.reply(
        strings.get('start_user'),
        reply_markup=await kbs.async_create_inline_keyboard_start(),
        parse_mode='Markdown',
    )


@handlers_router.callback_query(F.data == 'register')
async def register_start(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if await requests.async_is_user_exist(user_id):
        await callback.answer(strings.get('register').get('user_exist'))
        return

    if await requests.async_is_user_form_exist(user_id):
        await callback.answer(strings.get('register').get('user_form_exist'))
        return

    if await async_is_forms_acceptance_blocked():
        await callback.answer(strings.get('register').get('acceptance_of_forms_blocked'))
        return

    await callback.answer(strings.get('register').get('start'))
    await state.set_state(UserRegestrationStates.full_name)
    await callback.message.answer(strings.get('register').get('full_name'))


@handlers_router.message(UserRegestrationStates.full_name)
async def register_full_name(message: Message, state: FSMContext):
    message_text = message.text

    if not is_valid_full_name(message_text):
        await message.answer(strings.get('register').get('full_name_is_not_valid'))
        await state.set_state(UserRegestrationStates.full_name)
        return

    await state.update_data(full_name=message_text)
    await state.set_state(UserRegestrationStates.email)
    await message.answer(strings.get('register').get('email'))


@handlers_router.message(UserRegestrationStates.email)
async def register_email(message: Message, state: FSMContext):
    message_text = message.text

    if not is_email_valid(message_text):
        await message.answer(strings.get('register').get('email_is_not_valid'))
        await state.set_state(UserRegestrationStates.email)
        return

    await state.update_data(email=message_text)

    data = await state.get_data()
    user_id = message.from_user.id
    user_chat_id = message.chat.id

    user_form = UserForm(
        telegram_id=user_id,
        telegram_chat_id=user_chat_id,
        full_name=data['full_name'],
        email=data['email']
    )

    await requests.async_create_user_form(user_form)

    bot = message.chat.bot

    form_text_format = str(strings.get('register').get('form')).format(user_id, user_chat_id, data['full_name'], data['email'])

    form_keyboard = await kbs.async_create_inline_keyboard_form(user_id)
    await bot.send_message(getenv('ADMIN_TELEGRAM_ID'), text=form_text_format, reply_markup=form_keyboard, parse_mode='Markdown')

    answer_text_format = str(strings.get('register').get('successful')).format(user_id, user_chat_id, data['full_name'], data['email'])
    await message.answer(text=answer_text_format, parse_mode='Markdown')

    await state.clear()


@handlers_router.callback_query(F.data.contains('form_accept_'))
async def form_accepted(callback: CallbackQuery):
    user_telegram_id = int(callback.data.split('_')[2])

    user_form = await requests.async_get_user_form(user_telegram_id)

    user = User(
        telegram_id=user_form.telegram_id,
        telegram_chat_id=user_form.telegram_chat_id,
        full_name=user_form.full_name,
        email=user_form.email,
        group_id=None
    )

    await requests.async_create_user(user)
    await requests.async_delete_user_form_object(user_form)

    accepted_text_format = str(strings.get('register').get('admin_form_accepted')).format(user_form.full_name)
    await callback.answer(accepted_text_format, parse_mode='Markdown')
    await callback.message.answer(accepted_text_format, parse_mode='Markdown')
    await callback.message.delete()

    bot = callback.bot
    await bot.send_message(user_form.telegram_chat_id, text=strings.get('register').get('user_form_accepted'), parse_mode='Markdown')


@handlers_router.callback_query(F.data.contains('form_reject_'))
async def form_rejected(callback: CallbackQuery):
    user_telegram_id = user_telegram_id = int(callback.data.split('_')[2])

    user_form: UserForm = await requests.async_get_user_form(user_telegram_id)
    await requests.async_delete_user_form_object(user_form)

    rejected_text_format = str(strings.get('register').get('admin_form_rejected')).format(user_form.full_name)
    await callback.answer(rejected_text_format, parse_mode='Markdown')
    await callback.message.answer(rejected_text_format, parse_mode='Markdown')
    await callback.message.delete()

    bot = callback.bot
    await bot.send_message(user_form.telegram_chat_id, text=strings.get('register').get('user_form_rejected'), parse_mode='Markdown')


@handlers_router.message(F.text == '✉Сформировать рассылку')
async def make_mailing(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    await message.answer(text=strings.get('admin').get('make_mailing'), reply_markup=await kbs.async_create_inline_keyboard_make_mailing(), parse_mode='Markdown')
    await message.delete()


@handlers_router.callback_query(F.data == 'make_mailing_all_users')
async def make_mailing_all_users_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('make_mailing_all_users'))
    await callback.message.answer(strings.get('admin').get('make_mailing_message'))
    await callback.message.delete()
    await state.set_state(CreateMailingForAllUsers.message)


@handlers_router.message(CreateMailingForAllUsers.message)
async def make_mailing_all_users_complete(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if len(msg_text) < 4:
        await message.answer(strings.get('admin').get('make_mailing_message_invalid'))
        await state.set_state(CreateMailingForAllUsers.message)
        return

    await state.update_data(message_text=msg_text)

    data = await state.get_data()

    users = await requests.async_get_users_all()
    bot = message.bot

    process_message = await message.answer(strings.get('admin').get('make_mailing_complete'))

    counter_success: int = 0
    counter_not_found: int = 0

    users_emails = list()

    for user in users:
        sended_message = await bot.send_message(user.telegram_id, text=data['message_text'])
        if not sended_message:
            counter_not_found += 1
            continue

        users_emails.append(user.email)
        counter_success += 1


    await async_send_mail(users_emails, 'STI MESSAGER BOT', data['message_text'])

    answer_text_format = str(strings.get('admin').get('make_mailing_complete_statistics')).format(counter_success, counter_not_found)
    await process_message.delete()
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')
    await state.clear()


@handlers_router.callback_query(F.data == 'make_mailing_users')
async def make_mailing_users_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('make_mailing_users'))
    await callback.message.answer(strings.get('admin').get('make_mailing_users_ids'))
    await callback.message.delete()
    await state.set_state(CreatingMailingForUsers.users_telegram_ids)


@handlers_router.message(CreatingMailingForUsers.users_telegram_ids)
async def make_mailing_users_telegram_ids(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not is_valid_ids_string(msg_text):
        await message.answer(strings.get('admin').get('make_mailing_users_ids_invalid'))
        await state.set_state(CreatingMailingForUsers.users_telegram_ids)
        return

    await state.update_data(users_telegram_ids=msg_text)

    await message.answer(strings.get('admin').get('make_mailing_message'))
    await state.set_state(CreatingMailingForUsers.message)


@handlers_router.message(CreatingMailingForUsers.message)
async def make_mailing_users_complete(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if len(msg_text) < 4:
        await message.answer(strings.get('admin').get('make_mailing_message_invalid'))
        await state.set_state(CreateMailingForAllUsers.message)
        return

    await state.update_data(message_text=msg_text)

    data = await state.get_data()
    users_telegram_ids_list = str(data['users_telegram_ids']).split(' ')

    process_message = await message.answer(strings.get('admin').get('make_mailing_complete'))

    bot = message.bot

    users_emails = list()

    counter_success: int = 0
    counter_not_found: int = 0

    for user_telegram_id in users_telegram_ids_list:
        user_telegram_id = int(user_telegram_id)
        if not await requests.async_is_user_exist(user_telegram_id):
            counter_not_found += 1
            continue

        user = await requests.async_get_user(user_telegram_id)

        sended_message = await bot.send_message(user.telegram_id, data['message_text'])
        if not sended_message:
            counter_not_found += 1
            continue

        users_emails.append(user.email)
        counter_success += 1

    await async_send_mail(users_emails, 'STI MESSAGER BOT', data['message_text'])

    answer_text_format = str(strings.get('admin').get('make_mailing_complete_statistics')).format(counter_success, counter_not_found)
    await process_message.delete()
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')
    await state.clear()


@handlers_router.callback_query(F.data == 'make_mailing_groups')
async def make_mailing_groups(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('make_mailing_groups'))
    await callback.message.answer(strings.get('admin').get('make_mailing_groups_ids'))
    await callback.message.delete()
    await state.set_state(CreatingMailingForGroups.groups_ids)


@handlers_router.message(CreatingMailingForGroups.groups_ids)
async def make_mailing_groups_ids(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not is_valid_ids_string(msg_text):
        await message.answer(strings.get('admin').get('make_mailing_groups_ids_invalid'))
        await state.set_state(CreatingMailingForGroups.groups_ids)
        return

    await state.update_data(groups_ids=msg_text)
    await message.answer(strings.get('admin').get('make_mailing_message'))
    await state.set_state(CreatingMailingForGroups.message)


@handlers_router.message(CreatingMailingForGroups.message)
async def make_mailing_groups_complete(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if len(msg_text) < 4:
        await message.answer(strings.get('admin').get('make_mailing_message_invalid'))
        await state.set_state(CreateMailingForAllUsers.message)
        return

    await state.update_data(message_text=msg_text)

    data = await state.get_data()
    groups_ids_list = str(data['groups_ids']).split(' ')

    process_message = await message.answer(strings.get('admin').get('make_mailing_complete'))

    bot = message.bot

    users_emails = list()

    counter_success: int = 0
    counter_not_found: int = 0

    for group_id in groups_ids_list:
        group_id = int(group_id)
        if not await requests.async_is_group_exist(group_id):
            continue

        users_in_group = await requests.async_get_all_users_from_group(group_id)
        for user in users_in_group:
            sended_message = await bot.send_message(user.telegram_id, data['message_text'])
            if not sended_message:
                counter_not_found += 1
                continue

            users_emails.append(user.email)
            counter_success += 1

    await async_send_mail(users_emails, 'STI MESSAGER BOT', data['message_text'])

    answer_text_format = str(strings.get('admin').get('make_mailing_complete_statistics')).format(counter_success, counter_not_found)
    await process_message.delete()
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')
    await state.clear()


@handlers_router.message(F.text == '🧍‍♂️🧍‍♀️Управление пользователями')
async def users_manage(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    await message.answer(text=strings.get('admin').get('users_manage'), reply_markup=await kbs.async_create_inline_keyboard_manage_users(), parse_mode='Markdown')
    await message.delete()


@handlers_router.callback_query(F.data == 'manage_users_change_data')
async def users_change_data(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('users_change_data'))
    await callback.message.answer(strings.get('admin').get('users_id'))
    await callback.message.delete()
    await state.set_state(UserChangeDataStates.user_telegram_id)


@handlers_router.message(UserChangeDataStates.user_telegram_id)
async def users_change_data_id(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not msg_text.isdigit():
        await message.answer(strings.get('admin').get('users_id_invalid'))
        await state.set_state(UserChangeDataStates.user_telegram_id)
        return

    user_telegram_id = int(msg_text)
    await state.update_data(user_telegram_id=user_telegram_id)

    await message.answer(strings.get('admin').get('users_change_data_full_name'))
    await state.set_state(UserChangeDataStates.full_name)


@handlers_router.message(UserChangeDataStates.full_name)
async def users_change_data_name(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not is_valid_full_name(msg_text):
        await message.answer(strings.get('admin').get('users_change_data_full_name_invalid'))
        await state.set_state(UserChangeDataStates.full_name)
        return

    await state.update_data(full_name=msg_text)

    await message.answer(strings.get('admin').get('users_change_data_email'))
    await state.set_state(UserChangeDataStates.email)


@handlers_router.message(UserChangeDataStates.email)
async def user_changes_data_email(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not is_email_valid(msg_text):
        await message.answer(strings.get('admin').get('users_change_data_email_invalid'))
        await state.set_state(UserChangeDataStates.email)
        return

    await state.update_data(email=msg_text)

    data = await state.get_data()
    user_telegram_id = data['user_telegram_id']
    user_full_name = data['full_name']
    user_email = data['email']

    if not await requests.async_is_user_exist(user_telegram_id):
        await message.answer(strings.get('admin').get('users_not_found'), reply_markup=await kbs.async_create_reply_keyboard_admin())
        await state.clear()
        return

    user = await requests.async_get_user(user_telegram_id)
    user.full_name = user_full_name
    user.email = user_email

    await requests.async_update_user(user)

    answer_text_format = str(strings.get('admin').get('users_change_data_complete')).format(user_telegram_id, user_full_name, user_email)
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')

    answer_user_text_format = str(strings.get('admin').get('users_change_data_complete_user')).format(user_full_name, user_email)
    await message.bot.send_message(user_telegram_id, text=answer_user_text_format, parse_mode='Markdown')

    await state.clear()


@handlers_router.callback_query(F.data == 'manage_users_change_group')
async def users_change_group(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('users_change_group'))
    await callback.message.answer(strings.get('admin').get('users_id'))
    await callback.message.delete()
    await state.set_state(UserChangeGroupStates.user_telegram_id)


@handlers_router.message(UserChangeGroupStates.user_telegram_id)
async def user_change_group_user_id(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not msg_text.isdigit():
        await message.answer(strings.get('admin').get('users_id_invalid'))
        await state.set_state(UserChangeGroupStates.user_telegram_id)
        return

    user_telegram_id = int(msg_text)
    await state.update_data(user_telegram_id=user_telegram_id)

    await message.answer(strings.get('admin').get('users_change_group_id'))
    await state.set_state(UserChangeGroupStates.group_id)


@handlers_router.message(UserChangeGroupStates.group_id)
async def user_change_group_complete(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not msg_text.isdigit():
        await message.answer(strings.get('admin').get('users_change_group_id_invalid'))
        await state.set_state(UserChangeGroupStates.group_id)
        return

    group_id = int(msg_text)
    await state.update_data(group_id=group_id)

    data = await state.get_data()
    user_telegram_id = data['user_telegram_id']
    user_group_id = data['group_id']

    if not await requests.async_is_user_exist(user_telegram_id):
        await message.answer(strings.get('admin').get('users_not_found'), reply_markup=await kbs.async_create_reply_keyboard_admin())
        await state.clear()
        return

    if not await requests.async_is_group_exist(user_group_id):
        await message.answer(strings.get('admin').get('groups_not_found'), reply_markup=await kbs.async_create_reply_keyboard_admin())
        await state.clear()
        return

    user = await requests.async_get_user(user_telegram_id)
    user.group_id = user_group_id
    await requests.async_update_user(user)

    group_name = await requests.async_get_group_name(user_group_id)

    anwer_text_format = str(strings.get('admin').get('users_change_group_complete')).format(user_telegram_id, group_name)
    await message.answer(text=anwer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin())

    answer_user_text_format = str(strings.get('admin').get('users_change_data_complete_user')).format(group_name)
    await message.bot.send_message(user_telegram_id, text=answer_user_text_format, parse_mode='Markdown')

    await state.clear()


@handlers_router.callback_query(F.data == 'manage_users_delete')
async def user_delete_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('users_delete'))
    await callback.message.answer(strings.get('admin').get('users_id'))
    await callback.message.delete()
    await state.set_state(UserDeleteStates.user_telegram_id)


@handlers_router.message(UserDeleteStates.user_telegram_id)
async def user_delete_complete(message: Message, state: FSMContext):
    msg_text = str(message.text)

    if not msg_text.isdigit():
        await message.answer(strings.get('admin').get('users_id_invalid'))
        await state.set_state(UserDeleteStates.user_telegram_id)
        return

    await state.update_data(user_telegram_id=int(msg_text))

    data = await state.get_data()
    user_telegram_id = data['user_telegram_id']

    if not await requests.async_is_user_exist(user_telegram_id):
        await message.answer(strings.get('admin').get('users_not_found'))
        await state.clear()
        return

    user = await requests.async_get_user(user_telegram_id)
    await requests.async_delete_user_from_object(user)

    answer_text_format = str(strings.get('admin').get('users_delete_complete')).format(user_telegram_id)
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin())

    await message.bot.send_message(user_telegram_id, text=strings.get('admin').get('users_delete_complete_user'), parse_mode='Markdown')
    await state.clear()



@handlers_router.callback_query(F.data == 'manage_users_list')
async def users_veiw_list(callback: CallbackQuery):
    users = await requests.async_get_users_all()

    users_list_text = strings.get('admin').get('users_view_all')
    for user in users:
        users_list_text += f'*{user.telegram_id}*  {user.full_name}  {user.email}  {user.group_id}\n'

    await callback.answer('Вы сделали запрос на вывод списка групп')
    await callback.message.answer(text=users_list_text, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')
    await callback.message.delete()


@handlers_router.message(F.text == '📝Управление группами')
async def groups_manage(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    await message.answer(text=strings.get('admin').get('groups_manage'), reply_markup=await kbs.async_create_inline_keyboard_manage_groups(), parse_mode='Markdown')
    await message.delete()


@handlers_router.callback_query(F.data == 'manages_groups_add_new')
async def groups_add_new_group_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('groups_add_new'))
    await callback.message.answer(strings.get('admin').get('groups_add_new_name'))
    await callback.message.delete()
    await state.set_state(GroupAddNewStates.name)


@handlers_router.message(GroupAddNewStates.name)
async def groups_add_new_group_complete(message: Message, state: FSMContext):
    group_name = message.text

    if not is_valid_string(group_name):
        await message.answer(strings.get('admin').get('groups_name_invalid'))
        await state.set_state(GroupAddNewStates.name)
        return

    if await requests.async_is_group_exist_by_name(group_name):
        await message.answer(strings.get('admin').get('groups_add_new_already_exist'))
        await state.set_state(GroupAddNewStates.name)
        return

    await state.update_data(name=group_name)

    data = await state.get_data()
    group = Group(
        name=data['name']
    )

    await requests.async_create_group(group)
    answer_text_format = str(strings.get('admin').get('groups_add_new_complete')).format(data['name'])
    await message.answer(answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin())

    await state.clear()


@handlers_router.callback_query(F.data == 'manage_groups_delete')
async def groups_delete_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('groups_delete'))
    await callback.message.answer(strings.get('admin').get('groups_delete_by_id_or_name'))
    await callback.message.delete()
    await state.set_state(GroupDeleteStates.id_or_name)


@handlers_router.message(GroupDeleteStates.id_or_name)
async def groups_delete_complete(message: Message, state: FSMContext):
    if not is_valid_string_for_group_find(message.text):
        await message.answer(strings.get('admin').get('groups_id_or_name_invalid'))
        await state.set_state(GroupDeleteStates.id_or_name)
        return

    await state.update_data(id_or_name=message.text)

    data = await state.get_data()
    id_or_name = str(data['id_or_name'])

    group = await requests.async_get_group_by_id_or_name(id_or_name)

    if not group:
        await message.answer(text=strings.get('admin').get('groups_not_found'), reply_markup=await kbs.async_create_reply_keyboard_admin())
        await state.clear()
        return

    await requests.async_delete_group_from_object(group)

    answer_text_format = str(strings.get('admin').get('groups_delete_complete')).format(id_or_name)
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin())
    await state.clear()


@handlers_router.callback_query(F.data == 'manage_groups_change_name')
async def groups_change_name(callback: CallbackQuery, state: FSMContext):
    await callback.answer(strings.get('admin').get('groups_change_name'))
    await callback.message.answer(strings.get('admin').get('groups_change_name_id_or_name'))
    await callback.message.delete()
    await state.set_state(GroupChangeNameStates.id_or_name)


@handlers_router.message(GroupChangeNameStates.id_or_name)
async def groups_change_name_id_or_name(message: Message, state: FSMContext):
    msg_text = message.text

    if not is_valid_string_for_group_find(msg_text):
        await message.answer(strings.get('admin').get('groups_id_or_name_invalid'))
        state.set_state(GroupChangeNameStates.id_or_name)
        return

    await message.answer(strings.get('admin').get('groups_change_name_new_name'))
    await state.update_data(id_or_name=msg_text)
    await state.set_state(GroupChangeNameStates.new_name)


@handlers_router.message(GroupChangeNameStates.new_name)
async def groups_change_name_new_name(message: Message, state: FSMContext):
    msg_text = message.text

    if not is_valid_string(msg_text):
        await message.answer(strings.get('admin').get('groups_name_invalid'))
        state.set_state(GroupChangeNameStates.new_name)
        return

    await state.update_data(new_name=msg_text)

    data = await state.get_data()
    id_or_name = str(data['id_or_name'])

    group = await requests.async_get_group_by_id_or_name(id_or_name)

    if not group:
        await message.answer(text=strings.get('admin').get('groups_not_found'), reply_markup=await kbs.async_create_reply_keyboard_admin())
        await state.clear()
        return

    group.name = data['new_name']
    await requests.async_update_group(group)

    answer_text_format = str(strings.get('admin').get('groups_change_name_complete')).format(id_or_name, data['new_name'])
    await message.answer(text=answer_text_format, reply_markup=await kbs.async_create_reply_keyboard_admin())
    await state.clear()


@handlers_router.callback_query(F.data == 'manage_groups_list')
async def groups_view_list(callback: CallbackQuery):
    groups = await requests.async_get_groups_all()

    groups_list_text = strings.get('admin').get('groups_view_all')
    for group in groups:
        groups_list_text += f'*{group.id}*  {group.name}\n'

    await callback.answer('Вы сделали запрос на вывод списка групп')
    await callback.message.answer(text=groups_list_text, reply_markup=await kbs.async_create_reply_keyboard_admin(), parse_mode='Markdown')
    await callback.message.delete()


@handlers_router.message(F.text == '⛔Заблокировать подачу новых заявок')
async def block_acceptance_of_forms(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    bot_properties = await requests.async_get_bot_properties()
    bot_properties.forms_acceptance_blocked = True
    await requests.async_update_bot_properites(bot_properties)

    await message.answer(strings.get('admin').get('block_acceptance_of_forms'), reply_markup=await kbs.async_create_reply_keyboard_admin())
    await message.delete()


@handlers_router.message(F.text == '✅Разблокировать подачу новых заявок')
async def block_acceptance_of_forms(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    bot_properties = await requests.async_get_bot_properties()
    bot_properties.forms_acceptance_blocked = False
    await requests.async_update_bot_properites(bot_properties)

    await message.answer(strings.get('admin').get('unblock_acceptance_of_forms'), reply_markup=await kbs.async_create_reply_keyboard_admin())
    await message.delete()