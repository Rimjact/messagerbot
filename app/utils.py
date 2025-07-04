import re

from os import getenv

from app.database.requests import async_get_bot_properties

FULL_NAME_PATTERN = r'[\u0410-\u042F\u0401][\u0430-\u044F\u0451]+'

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+$')
FULL_NAME_REGEX = re.compile(fr'^{FULL_NAME_PATTERN}\s{FULL_NAME_PATTERN}(\s{FULL_NAME_PATTERN})?$')
STRING_REGEX = re.compile(r'^[\u0400-\u04FFA-Za-z -]+$')
GROUP_ID_OR_NAME_REGEX = re.compile(r'^[\u0400-\u04FF\s0-9-]+$')
IDS_REGEX = re.compile(r'^\d+( \d+)*$')


async def async_is_forms_acceptance_blocked() -> bool:
    """Проверяет, заблокирован ли на данный момент
    приём новых заявок на регистрацию от пользователей.

    Returns
    -------
    True если заблокирован, иначе False
    """

    bot_properties = await async_get_bot_properties()
    return bool(bot_properties.forms_acceptance_blocked)


def is_email_valid(email: str) -> bool:
    """Проверяет строку на соответствие
    адресу электронной почты.

    Parameters
    ----------
    email : str
        адрес электронной почты

    Returns
    -------
    bool
        True если соответствует, иначе False
    """

    return bool(EMAIL_REGEX.match(email))


def is_valid_full_name(full_name: str) -> bool:
    """Проверяет строку на соответсвие ФИО.

    Parameters
    ----------
    full_name : str
        строка ФИО для проверки

    Returns
    -------
    bool
        True если соответствует, иначе False
    """

    return bool(FULL_NAME_REGEX.match(full_name))


def is_valid_string(string: str) -> bool:
    """Проверяет строку на соответсвие,
    что она содержит только символы кириллицы,
    пробелы и тире.

    Parameters
    ----------
    string : str
        строка для проверки

    Returns
    -------
    bool
        True если соответствует, иначе False
    """

    return bool(STRING_REGEX.match(string))


def is_valid_string_for_group_find(string: str) -> bool:
    """Проверяет строку на соотвествие для процедуры удаления группы,
    что она содержит только символы кириллицы, пробелы, цифры и тире.

    Parameters
    ----------
    string : str
        строка для проверки

    Returns
    -------
    bool
        True если соответствует, иначе False
    """

    return bool(GROUP_ID_OR_NAME_REGEX.match(string))


def is_valid_ids_string(string: str) -> bool:
    """Проверяет строку на соотвествие, что она содержит
    только цифры и пробелы в строгом формате.

    Parameters
    ----------
    string : str
        строка для проверки

    Returns
    -------
    bool
        True если соответствует, иначе False
    """

    return bool(IDS_REGEX.match(string))


def user_is_admin(user_telegram_id: int) -> bool:
    """Проверяет, является ли пользователь с указанным
    уникальным идентификатором Telegram администратором бота.

    Parameters
    ----------
    user_telegram_id : int
        идентификатор пользователя Telegram

    Returns
    -------
    bool
        True если является, иначе False
    """

    return user_telegram_id == int(getenv('ADMIN_TELEGRAM_ID'))