import re

from os import getenv

from pprint import pprint

from sqlalchemy import BigInteger

from app.database.requests import async_get_bot_properties


EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
STRING_REGEX = re.compile(r'^[\u0400-\u04FF\s-]+$')
GROUP_ID_OR_NAME_REGEX = re.compile(r'^[\u0400-\u04FF\s0-9-]+$')





async def async_is_acceptance_of_forms_blocked() -> bool:
    """Проверяет, заблокирован ли на данный момент
    приём новых заявок на регистрацию от пользователей.

    Returns
    -------
    True если заблокирован, иначе False
    """

    bot_properties = await async_get_bot_properties()
    return bool(bot_properties.acceptance_of_forms_blocked)


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
        True если соотвествует, иначе False
    """

    return bool(EMAIL_REGEX.match(email))


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
        True если соотвествие, иначе False
    """

    return bool(STRING_REGEX.match(string))


def is_valid_string_for_group_find(string: str) -> bool:
    """Проверяет строку на соотвествие для процедуры удаления группы,
    что она содержит только символы кириллицы, пробелы, цифры и тире.
    """

    return bool(GROUP_ID_OR_NAME_REGEX.match(string))


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