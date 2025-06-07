import app.database.requests as requests

from os import getenv

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboards import async_create_reply_keyboard_admin, async_create_inline_keyboard_start, async_create_inline_keyboard_form
from app.states import UserRegestrationStates
from app.strings import strings
from app.utils import async_is_acceptance_of_forms_blocked, is_email_valid, is_valid_string, user_is_admin
from app.database.models import UserForm, User

handlers_router = Router(name=__name__)


@handlers_router.message(CommandStart())
async def start(message: Message):
    if user_is_admin(message.from_user.id):
        await message.reply(
            text=strings.get('start_admin'),
            reply_markup=await async_create_reply_keyboard_admin(),
            parse_mode='Markdown',
        )
        return

    await message.reply(
        strings.get('start_user'),
        reply_markup=await async_create_inline_keyboard_start(),
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

    if await async_is_acceptance_of_forms_blocked():
        await callback.answer(strings.get('register').get('acceptance_of_forms_blocked'))
        return

    await callback.answer(strings.get('register').get('start'))
    await state.set_state(UserRegestrationStates.full_name)
    await callback.message.answer(strings.get('register').get('full_name'))


@handlers_router.message(UserRegestrationStates.full_name)
async def register_full_name(message: Message, state: FSMContext):
    message_text = message.text

    if not is_valid_string(message_text):
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

    form_keyboard = await async_create_inline_keyboard_form(user_id)
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


@handlers_router.message(F.text == '⛔Заблокировать подачу новых заявок')
async def block_acceptance_of_forms(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    bot_properties = await requests.async_get_bot_properties()
    bot_properties.acceptance_of_forms_blocked = True
    await requests.async_update_bot_properites(bot_properties)

    await message.answer(strings.get('admin').get('block_acceptance_of_forms'), reply_markup=await async_create_reply_keyboard_admin())
    await message.delete()


@handlers_router.message(F.text == '✅Разблокировать подачу новых заявок')
async def block_acceptance_of_forms(message: Message):
    if not user_is_admin(message.from_user.id):
        return

    bot_properties = await requests.async_get_bot_properties()
    bot_properties.acceptance_of_forms_blocked = False
    await requests.async_update_bot_properites(bot_properties)

    await message.answer(strings.get('admin').get('unblock_acceptance_of_forms'), reply_markup=await async_create_reply_keyboard_admin())
    await message.delete()