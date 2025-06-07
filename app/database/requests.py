from sqlalchemy import select, update
from sqlalchemy import BigInteger

from app.database.db import create_async_session
from app.database.models import BotProperties, UserForm, User, Group


async def async_get_bot_properties() -> BotProperties:
    """Асинхронный метод, который получает экземпляр
    текущих параметров бота из БД.

    Returns
    -------
    BotProperties
        текущее параметры бота
    """

    async_session = create_async_session()

    async with async_session() as session:
        properties = await session.scalar(select(BotProperties))
        return properties


async def async_get_user(telegram_id: BigInteger) -> User:
    """Асинхронный метод, который получает экземпляр данных
    о пользователе из базы данных по его идентификатору Telegram.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    User
        экземпляр класса с информацией о пользователе
    """

    async_session = create_async_session()

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        return user


async def async_get_all_users():
    """Асинхронный метод, который получает экземпляры данных
    всех пользователей из базы данных.

    Returns
    -------
    list
        массив данных о пользователях
    """

    async_session = create_async_session()

    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return users


async def async_get_all_users_from_group(group_id: int):
    """Асинхронный метод, который получает экземпляры данных
    всех пользователей из БД по идентификатору группы.

    Parameters
    ----------
    group_id : int
        идентификатор группы

    Returns
    -------
    list
        массив данных о пользователях группы
    """

    async_session = create_async_session()

    async with async_session() as session:
        statement = select(User).where(User.group_id == group_id)
        result = await session.execute(statement)
        users = result.scalars().all()
        return users


async def async_get_user_form(telegram_id: BigInteger) -> UserForm:
    """Асинхронный метод, который получает экзепляр данных о заявке пользователя
    из базы данных по его идентификатору Telegram.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    UserForm
        экземпляр класса с информацией о заявке пользователя с БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        user_form = await session.scalar(select(UserForm).where(UserForm.telegram_id == telegram_id))
        return user_form


async def async_get_group(id: int) -> Group:
    """Асинхронный метод, который получает экземпляр данных о группе
    из базы данных по его идентификатору.

    Parameters
    ----------
    id : int
        уникальный идентификатор группы

    Returns
    -------
    Group
        экземпляр класса с информацией о группе
    """

    async_session = create_async_session()

    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.id == id))
        return group


async def async_get_group_by_name(name: str) -> Group:
    """Асинхронный метод, который получает экземпляр данных о группе
    из базы данных по его имени.

    Parameters
    ----------
    name : str
        имя группы

    Returns
    -------
    Group
        экземпляр класса с информацией о группе
    """

    async_session = create_async_session()

    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.name == name))
        return group


async def async_is_user_exist(telegram_id: BigInteger) -> bool:
    """Асинхронный метод, который проверяет, существует ли пользователь
    с таким идентификатором в базе данных.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    bool
        True если существует, иначе False
    """

    user = await async_get_user(telegram_id)
    return user != None


async def async_is_user_form_exist(telegram_id: BigInteger) -> bool:
    """Асинхронный метод, который проверяет, существует ли заявка пользователя
    с таким идентификатором в базе данных.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    bool
        True если существует, иначе False
    """

    user_form = await async_get_user_form(telegram_id)
    return user_form != None


async def async_is_group_exist(id: int) -> bool:
    """Асинхронный метод, который проверяет, существует ли группа
    с таким идентификатором в базе данных.

    Parameters
    ----------
    id : int
        уникальный идентификатор группы

    Returns
    -------
    bool
        True если существует, иначе False
    """

    group = await async_get_group(id)
    return group != None


async def async_is_group_exist_by_name(name: str) -> bool:
    """Асинхроннй метод, который проверяет, существует ли группа
    с таким идентификатором в базе данных.

    Parameters
    ----------
    name : str
        имя группы

    Returns
    -------
    bool
        True если существует, иначе False
    """

    group = await async_get_group_by_name(name)
    return group != None


async def async_create_user(user: User) -> str:
    """Асинхронный метод, который сохраняет информацию
    о пользователе в базу данных.

    Parameters
    ----------
    user : User
        экземпляр класса пользователя

    Returns
    -------
    str
        пусткая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if await async_is_user_exist(user.telegram_id):
            error = 'Пользователь с таким Telegram ID уже существует'
            return error

        session.add(user)
        await session.commit()
        return error


async def async_create_user_form(user_form: UserForm) -> str:
    """Асинхронный метод, который сохраняет информацию
    о заявке пользователя в базу данных.

    Parameters
    ----------
    user_form : UserForm
        экземпляр класса заявки пользователя

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if await async_is_user_form_exist(user_form.telegram_id):
            error = 'Заявка пользователя с таким Telegram ID уже существует'
            return error

        session.add(user_form)
        await session.commit()
        return error


async def async_create_group(group: Group) -> str:
    """Асинхронный метод, который сохраняет информацию
    о группе в базу данных.

    Parameters
    ----------
    group : Group
        экземпляр класса группы

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if await async_is_group_exist_by_name(group.name):
            error = 'Группа с таким именем уже существует'
            return error

        session.add(group)
        await session.commit()
        return error


async def async_update_bot_properites(new_properties: BotProperties) -> None:
    """Асинхронный метод, который заменяет
    параметры бота в базе данных на новые.
    """

    async_session = create_async_session()

    async with async_session() as session:
        await session.merge(new_properties)
        await session.commit()


async def async_delete_user(telegram_id: BigInteger) -> str:
    """Асинхронный метод, который удаляет пользователя
    из базы данных.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_user_exist(telegram_id):
            error = 'Пользователя с таким Telegram ID не найден'
            return error

        user = await async_get_user(telegram_id)
        await session.delete(user)
        await session.commit()
        return error


async def async_delete_user_form(telegram_id: BigInteger) -> str:
    """Асинхронный метод, который удаляет заявку пользователя
    из базы данных.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_user_form_exist(telegram_id):
            error = 'Заявку от данного пользователя не найдено'
            return error

        user_form = await async_get_user_form(telegram_id)
        await session.delete(user_form)
        await session.commit()
        return error


async def async_delete_user_form_object(user_form: UserForm) -> str:
    """Асинхронный метод, который удаляет заявку пользователя
    из базы данных основываясь на заданном объекте.

    Parameters
    ----------
    user_form : UserForm
        объект заявки пользователя в БД

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_user_form_exist(user_form.telegram_id):
            error = 'Заявку от данного пользователя не найдено'
            return error

        await session.delete(user_form)
        await session.commit()
        return error


async def async_delete_group(id: int) -> str:
    """Асинхронный метод, который удаляет группу из базы данных.

    Parameters
    ----------
    id : int
        идентификатор группы

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_group_exist(id):
            error = 'Группа с таким идентификатором не найдена'
            return error

        group = await async_get_group(id)
        await session.delete(group)
        await session.commit()
        return error