from sqlalchemy import select, update, delete
from sqlalchemy import BigInteger

from app.database.db import create_async_session
from app.database.models import User, Group


async def async_get_user(telegram_id: BigInteger) -> User:
    """Получает экземпляр данных о пользователе
    из базы данных по его идентификатору Telegram.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram

    Returns
    -------
    User
        экземпляр класса с информацией о пользователе с БД
    """

    async with create_async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        return user


async def async_is_user_exist(telegram_id: BigInteger) -> bool:
    """Проверяет, существует ли пользователь
    с таким идентификатором в базе данных.

    Parameters
    ----------
    telegram_id : BigInteger
        уникальный идентификатор пользователя Telegram
    """

    user = await async_get_user(telegram_id)
    return user != None


async def async_create_user(user: User) -> None:
    """Сохраняет информацию о пользователе в базе данных.

    Parameters
    ----------
    user_info : User
        экземпляр класса пользователя.
    """

    async with create_async_session() as session:
        if not async_is_user_exist(user.telegram_id):
            session.add(user)
            await session.commit()
