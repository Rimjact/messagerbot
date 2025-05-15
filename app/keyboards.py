from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def async_create_inline_keyboard_start() -> InlineKeyboardMarkup:
    '''Асинхронный метод, который создаёт и возвращает стартовую клавиатуру.

    Returns
    -------
    InlineKeyboardMarkup
        стартовая клавиатура
    '''

    KEYBOARD_START_DATA = (
        ('📝 Регистрация', 'register'),
        ('⚙ Настройки', 'settings'),
    )

    keyboard = InlineKeyboardBuilder()
    for txt, data in KEYBOARD_START_DATA:
        keyboard.add(InlineKeyboardButton(text=txt, callback_data=data))

    return keyboard.adjust(2).as_markup()