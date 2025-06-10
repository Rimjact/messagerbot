from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.view.strings import answer_strings
from app.model.states.register import RegisterStates


async def on_register_start_processed(callback: CallbackQuery, state: FSMContext, error: str = ''):
    """Обработчик события, когда запрос на начало регистрации обработан."""

    match error:
        case 'user_exist':
            await callback.answer(answer_strings.get('register').get('user_exist'))
            return
        case 'user_form_exist':
            await callback.answer(answer_strings.get('register').get('user_from_exist'))
            return
        case 'forms_acceptance_blocked':
            await callback.answer(answer_strings.get('register').get('forms_acceptance_blocked'))
            return

    await callback.answer(answer_strings.get('register').get('start'))
    await callback.message.answer(answer_strings.get('register').get('full_name'))
    await state.set_state(RegisterStates.full_name)


async def on_register_full_name_processed(message: Message, state: FSMContext, error: str = ''):
    """Обработчик события, когда введённое ФИО обработано."""

    if error == 'invalid_string':
        await message.answer(answer_strings.get('register').get('full_name_invalid'))
        return

    await state.update_data(full_name=message.text)
    await state.set_state(RegisterStates.email)
    await message.answer(answer_strings.get('register').get('email'))


async def on_register_complete_processed(message: Message, sate: FSMContext):
    """"""

    pass