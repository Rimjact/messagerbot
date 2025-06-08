from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from sqlalchemy import BigInteger

from app.utils import async_is_acceptance_of_forms_blocked

async def async_create_inline_keyboard(keyboard_data, adjust: int) -> InlineKeyboardMarkup:
    """Асинхронный метод, который создаёт и возвращает инлайн клавиатуру,
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


async def async_create_reply_keyboard(keyboard_data, adjust: int) -> ReplyKeyboardMarkup:
    """Асинхронный метод, который возвращает реплай клавиатуру,
    основанную на переданных параметрах.

    Parameters
    ----------
    keyboard_data
        информация о кнопках клавиатуры
    adjust : int
        на сколько столбцов будет разбита клавиатура

    Returns
    -------
    ReplyKeyboardMarkup
        клавиатура
    """

    keyboard = ReplyKeyboardBuilder()
    for txt in keyboard_data:
        keyboard.add(KeyboardButton(text=txt))

    return keyboard.adjust(adjust).as_markup(resize_keyboard=True)


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

    Parameters
    ----------
    user_telegram_id : BigInteger
        уникальный идентификатор пользователя, который отправил заявку

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


async def async_create_inline_keyboard_make_mailing() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращяет клавиатуру создания рассылки.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура создания рассылки
    """

    KEYBOARD_MAKE_MAILING_DATA = (
        ('📣Всем', 'make_mailing_all_users'),
        ('🙍‍♂️Конкретным пользователям', 'make_mailing_users'),
        ('📄Конкретным группам', 'make_mailing_groups'),
    )

    return await async_create_inline_keyboard(KEYBOARD_MAKE_MAILING_DATA, 1)


async def async_create_inline_keyboard_manage_groups() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращяет клавиатуру управления группами.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура управления группами
    """

    KEYBOARD_MANAGE_GROUPS_DATA = (
        ('➕Добавить новую', 'manages_groups_add_new'),
        ('➖Удалить существующую', 'manage_groups_delete'),
        ('✏Изменить название', 'manage_groups_change_name'),
        ('📄Вывести список групп', 'manage_groups_list'),
    )

    return await async_create_inline_keyboard(KEYBOARD_MANAGE_GROUPS_DATA, 1)


async def async_create_inline_keyboard_manage_users() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращает клавиатуру управления пользователями.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура управления пользователями
    """

    KEYBOARD_MANAGE_USERS_DATA = (
        ('✏ Изменить данные', 'manage_users_change_data'),
        ('➖ Удалить зарегистрированного', 'manage_users_delete'),
        ('📌 Переместить в группу', 'manage_users_change_group'),
        ('📄Вывести список пользователей', 'manage_users_list'),
    )

    return await async_create_inline_keyboard(KEYBOARD_MANAGE_USERS_DATA, 1)


async def async_create_reply_keyboard_admin() -> ReplyKeyboardMarkup:
    """Асинхронный метод, который возвращает клавиатуру для адмнистратора.

    Returns
    -------
    ReplyKeyboardMarkup
        клавиатура администратора
    """

    keyboard_admin_data = (
        '✉Сформировать рассылку',
        '🧍‍♂️🧍‍♀️Управление пользователями',
        '📝Управление группами',
        '⛔Заблокировать подачу новых заявок' if not await async_is_acceptance_of_forms_blocked() else '✅Разблокировать подачу новых заявок'
    )

    return await async_create_reply_keyboard(keyboard_admin_data, 2)