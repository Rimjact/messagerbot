from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from sqlalchemy import BigInteger


async def async_create_inline_keyboard(keyboard_data, adjust: int) -> InlineKeyboardMarkup:
    """Асинхронный метод, который создаёт и возвращает клавиатуру,
    основанную на переданных параметрах.

    Parameters
    ----------
    keyboard_data
        информация о кнопках клавиатуры
    adjust : int
        на сколько колонок будет разбита клавиатура

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура
    """

    keyboard = InlineKeyboardBuilder()
    for txt, data in keyboard_data:
        keyboard.add(InlineKeyboardButton(text=txt, callback_data=data))

    return keyboard.adjust(adjust).as_markup()


async def async_create_inline_keyboard_start() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращает стартовую клавиатуру.

    Returns
    -------
    InlineKeyboardMarkup
        стартовая клавиатура
    """

    KEYBOARD_START_DATA = (
        ('📝 Регистрация', 'register'),
        ('⚙ Настройки', 'settings'),
    )

    return await async_create_inline_keyboard(KEYBOARD_START_DATA, 2)


async def async_create_inline_keyboard_form(user_telegram_id: BigInteger) -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращает клавиатуру для анкеты.

    Returns
    -------
    InlineKeyboardMarkup
        стартовая клавиатура
    """

    KEYBOARD_FORM_DATA = (
            ('✔Принять', 'form_accept_' + str(user_telegram_id)),
            ('❌Отклонить', 'form_reject_' + str(user_telegram_id)),
    )

    return await async_create_inline_keyboard(KEYBOARD_FORM_DATA, 2)