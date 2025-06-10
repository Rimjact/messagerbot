import re

from os import getenv


EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
STRING_REGEX = re.compile(r'^[A-Za-z\u0400-\u04FF\s-]+$')
IDS_REGEX = re.compile(r'^\d+( \d+)*$')


def is_user_has_admin_privileges(user_tg_id: int) -> bool:
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

    return user_tg_id == int(getenv('ADMIN_TELEGRAM_ID'))


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


def is_string_valid(string: str) -> bool:
    """Проверяет строку на соответсвие,
    что она содержит только символы кириллицы,
    латиницы, пробелы и тире.

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


def is_ids_string_valid(string: str) -> bool:
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