from aiogram.types import ReplyKeyboardMarkup

from app.model.managers.properties import async_is_forms_acceptance_blocked

from app.view.keyboards.builders import async_build_reply_keyboard


async def async_build_keyboard_admin() -> ReplyKeyboardMarkup:
    """Асинхронный метод, который возвращает клавиатуру для адмнистратора.

    Returns
    -------
    ReplyKeyboardMarkup
        клавиатура администратора
    """

    KEYBOARD_ADMIN_DATA = (
        '✉ Сформировать рассылку',
        '🧍‍♂️🧍‍♀️ Управление пользователями',
        '📝 Управление группами',
        '⛔Заблокировать подачу новых заявок' if not await async_is_forms_acceptance_blocked() else '✅Разблокировать подачу новых заявок'
    )

    return await async_build_reply_keyboard(KEYBOARD_ADMIN_DATA, 2)
