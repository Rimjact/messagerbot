import re

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
STRING_REGEX = re.compile(r'^[\u0400-\u04FF\s]+$')


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
    что она содержит только символы кириллицы
    и пробелы.

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

