from aiogram.types import InlineKeyboardMarkup

from app.view.keyboards.builders import async_build_inline_keyboard


async def async_build_keyboard_start() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращает стартовую клавиатуру.

    Returns
    -------
    InlineKeyboardMarkup
        стартовая клавиатура
    """

    KEYBOARD_START_DATA = (
        ('📝 Регистрация', 'register'),
        ('⚙ Настройки', 'settings')
    )

    return await async_build_inline_keyboard(KEYBOARD_START_DATA, 2)


async def async_build_keyboard_form(tg_id: int) -> InlineKeyboardMarkup:
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

    KEYBAORD_FORM_DATA = (
        ('✔ Принять', 'form_accept_' + str(tg_id)),
        ('❌ Отклонить', 'form_reject_' + str(tg_id))
    )

    return await async_build_inline_keyboard(KEYBAORD_FORM_DATA, 2)


async def async_build_keyboard_mailing() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращяет клавиатуру создания рассылки.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура создания рассылки
    """

    KEYBOARD_MAILING_DATA = (
        ('📣Всем', 'mailing_all_users'),
        ('🙍‍♂️Конкретным пользователям', 'mailing_users'),
        ('📄Конкретным группам', 'mailing_groups')
    )

    return await async_build_inline_keyboard(KEYBOARD_MAILING_DATA, 2)


async def async_build_keyboard_groups_manage() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращяет клавиатуру управления группами.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура управления группами
    """

    KEYBOARD_GROUPS_MANAGE_DATA = (
        ('➕Добавить новую', 'groups_manage_add_new'),
        ('➖Удалить существующую', 'groups_manage_delete'),
        ('✏Изменить название', 'groups_manage_change_name'),
        ('📄Вывести список групп', 'groups_manage_list')
    )

    return await async_build_inline_keyboard(KEYBOARD_GROUPS_MANAGE_DATA, 2)


async def async_build_keyboard_users_manage() -> InlineKeyboardMarkup:
    """Асинхронный метод, который возвращает клавиатуру управления пользователями.

    Returns
    -------
    InlineKeyboardMarkup
        клавиатура управления пользователями
    """

    KEYBOARD_USERS_MANAGE_DATA = (
        ('✏ Изменить данные', 'users_manage_change_data'),
        ('➖ Удалить зарегистрированного', 'users_manage_delete'),
        ('📌 Переместить в группу', 'users_manage_change_group'),
        ('📄Вывести список пользователей', 'users_manage_list')
    )

    return await async_build_inline_keyboard(KEYBOARD_USERS_MANAGE_DATA, 2)