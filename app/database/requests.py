from sqlalchemy import select, update
from sqlalchemy import BigInteger, Sequence

from app.database.db import create_async_session
from app.database.models import BotProperties, UserForm, User, Group


async def async_get_bot_properties() -> BotProperties:
    """Асинхронный метод, который получает экземпляр
    текущих параметров бота из БД.

    Returns
    -------
    BotProperties
        объект текущих параметров бота
    """

    async_session = create_async_session()

    async with async_session() as session:
        properties = await session.scalar(select(BotProperties))
        await session.close()
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
        объект пользователя из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        await session.close()
        return user


async def async_get_users_all():
    """Асинхронный метод, который получает экземпляры данных
    всех пользователей из базы данных.

    Returns
    -------
    Sequence[User]
        массив объектов пользователей группы из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        await session.close()
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
    Sequence[User]
        массив объектов пользователей группы из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        statement = select(User).where(User.group_id == group_id)
        result = await session.execute(statement)
        users = result.scalars().all()
        await session.close()
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
        объект заявки пользователя из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        user_form = await session.scalar(select(UserForm).where(UserForm.telegram_id == telegram_id))
        await session.close()
        return user_form


async def async_get_group(id: int) -> Group:
    """Асинхронный метод, который получает экземпляр данных о группе
    из базы данных по её идентификатору.

    Parameters
    ----------
    id : int
        уникальный идентификатор группы

    Returns
    -------
    Group
        объект группы из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.id == id))
        await session.close()
        return group


async def async_get_group_by_name(name: str) -> Group:
    """Асинхронный метод, который возвращает экземпляр данных о группе
    из базы данных по её имени.

    Parameters
    ----------
    name : str
        имя группы

    Returns
    -------
    Group
        объект группы из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        group = await session.scalar(select(Group).where(Group.name == name))
        await session.close()
        return group


async def async_get_group_by_id_or_name(id_or_name: str) -> Group:
    """Асинхронный метод, который возвращает экземпляр группы
    по её идентификатору или имени.

    Parameters
    ----------
    id_or_name : str
        идентификатор или имя группы

    Returns
    -------
    Group
        объект группы из БД
    """

    if id_or_name.isdigit():
        group_id = int(id_or_name)
        return await async_get_group(group_id)

    group_name = id_or_name
    return await async_get_group_by_name(group_name)


async def async_get_groups_all():
    """Асинхронный метод, который возвращает экземпляры всех групп
    из базы данных.

    Returns
    -------
    Sequence[User]
        массив объектов всех групп из БД
    """

    async_session = create_async_session()

    async with async_session() as session:
        result = await session.execute(select(Group))
        groups = result.scalars().all()
        await session.close()
        return groups


async def async_get_group_name(group_id: int) -> str:
    """Асинхронный метод, который возвращает имя группы
    по её идентификатору в БД.

    Parameters
    ----------
    group_id : int
        идентификатор группы

    Returns
    -------
    str
        имя группы
    """

    group = await async_get_group(group_id)
    return group.name


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
        await session.close()
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
        await session.close()
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
        await session.close()
        return error


async def async_update_bot_properites(new_properties: BotProperties) -> None:
    """Асинхронный метод, который заменяет
    параметры бота в базе данных на новые.

    Parameters
    ----------
    new_properties : BotProperties
        объект параметров бота
    """

    async_session = create_async_session()

    async with async_session() as session:
        await session.merge(new_properties)
        await session.commit()
        await session.close()



async def async_update_user(user: User) -> None:
    """Асинхронный метод, который заменяет
    объект пользователя в базе данных на новый.
    Нужен для обновления данных.

    Parameters
    ----------
    user : User
        объект пользователя
    """

    async_session = create_async_session()

    async with async_session() as session:
        await session.merge(user)
        await session.commit()
        await session.close()


async def async_update_group(group: Group) -> None:
    """Асинхронный метод, который заменяет
    объект группы в базе данных на новый.

    Parameters
    ----------
    group : Group
        объект группы
    """

    async_session = create_async_session()

    async with async_session() as session:
        await session.merge(group)
        await session.commit()
        await session.close()


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
        await session.close()
        return error


async def async_delete_user_from_object(user: User) -> str:
    """Асинхронный метод, который удаляет пользователя
    из базы данных основываясь на заданном объекте.

    Parameters
    ----------
    user : User
        объект пользователя

    Returns
    -------
    str
        пустая строка или ошибка
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_user_exist(user.telegram_id):
            error = 'Пользователь не найден'
            return error

        await session.delete(user)
        await session.commit()
        await session.close()
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
        await session.close()
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
        await session.close()
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
        await session.close()
        return error


async def async_delete_group_from_object(group: Group) -> str:
    """Асинхронный метод, который удаляет группу из БД,
    используя её объект.

    Parameters
    ----------
    group : Group
        объект группы

    Returns
    -------
    str
        пустая строка или текст ошибки
    """

    error: str = ''
    async_session = create_async_session()

    async with async_session() as session:
        if not await async_is_group_exist(group.id):
            error = 'Группа с таким идентификатором не найдена'
            return error

        await session.delete(group)
        await session.commit()
        await session.close()
        return error