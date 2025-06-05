from os import getenv

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.models import ModelBase


engine = create_async_engine(getenv('DB_PATH'))


def create_async_session() -> async_sessionmaker[AsyncSession]:
    """Создаёт и возвращает асинхронную сессию соединения с БД.

    Returns
    ------
    AsyncSession
        асинхронная сессия соединения с БД
    """

    return async_sessionmaker(engine)



async def async_main() -> None:
    """Асинхронный метод запускающий соединение с базой данных.\n
    Также создаются таблицы, если они не существуют, основанные на <code>ModelBase</code>.
    """

    async with engine.begin() as connection:
        await connection.run_sync(ModelBase.metadata.create_all)