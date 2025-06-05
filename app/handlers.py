import app.keyboards as kbs
import app.database.requests as requests

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states import UserRegestrationStates
from app.strings import strings
from app.utils import is_email_valid, is_valid_string
from app.database.models import UserForm

handlers_router = Router(name=__name__)


@handlers_router.message(CommandStart())
async def start(message: Message):
    await message.reply(strings.get('start'), reply_markup=await kbs.async_create_inline_keyboard_start(), parse_mode="Markdown")


@handlers_router.callback_query(F.data == 'register')
async def register_start(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id

    if await requests.async_is_user_exist(user_id):
        await callback.answer(strings.get('register').get('user_exist'))
        return

    if await requests.async_is_user_form_exist(user_id):
        await callback.answer(strings.get('register').get('user_form_exist'))
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

    user_form = UserForm(telegram_id=user_id, telegram_chat_id=user_chat_id, full_name=data['full_name'], email=data['email'])

    await requests.async_create_user_form(user_form)

    answer_format = str(strings.get('register').get('successful')).format(user_id, user_chat_id, data['full_name'], data['email'])
    await message.answer(text=answer_format, parse_mode="Markdown")
    await state.clear()