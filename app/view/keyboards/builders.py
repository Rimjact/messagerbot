from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


async def async_build_inline_keyboard(data, adjust: int) -> InlineKeyboardMarkup:
    """Асинхронный метод, который создаёт и возвращает инлайн клавиатуру,
    основанную на переданных параметрах.

    Parameters
    ----------
    data
        информация о кнопках клавиатуры
    adjust : int
        на сколько колонок будет разбита клавиатура

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура
    """

    builder = InlineKeyboardBuilder()
    for text, callback_data in data:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback_data))

    return builder.adjust(adjust).as_markup()


async def async_build_reply_keyboard(data, adjust: int) -> ReplyKeyboardMarkup:
    """Асинхронный метод, который возвращает реплай клавиатуру,
    основанную на переданных параметрах.

    Parameters
    ----------
    data
        информация о кнопках клавиатуры
    adjust : int
        на сколько столбцов будет разбита клавиатура

    Returns
    -------
    ReplyKeyboardMarkup
        клавиатура
    """

    builder = ReplyKeyboardBuilder()
    for text in data:
        builder.add(KeyboardButton(text=text))

    return builder.adjust(adjust).as_markup(resize_keyboard=True)