from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


KEYBOARD_START_DATA = (
    ('📝 Регистрация', 'register'),
    ('⚙ Настройки', 'settings'),
)


def create_inline_keyboard_start() -> InlineKeyboardMarkup:
    '''Создаёт и возвращает стартовую клавиатуру.

    Returns
    -------
    InlineKeyboardMarkup
        главная клавиатура
    '''

    keyboard_markup = InlineKeyboardMarkup()
    keyboard_buttons = (InlineKeyboardButton(text, callback_data=data) for text, data in KEYBOARD_START_DATA)
    keyboard_markup.row(*keyboard_buttons)

    return keyboard_markup