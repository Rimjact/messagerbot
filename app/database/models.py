from sqlalchemy import ForeignKey, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class ModelBase(AsyncAttrs, DeclarativeBase):
    """Базовая модель таблицы для остальных моделей.\n
    Наследует <code>AsyncAttrs</code> и <code>DeclarativeBase</code>
    """
    pass


class BotProperties(ModelBase):
    """Модель таблицы настроек бота.\n
    Наследует класс <code>ModelBase</code>
    """
    __tablename__ = 'properites'

    id: Mapped[int] = mapped_column(primary_key=True)
    acceptance_of_forms_blocked: Mapped[bool] = mapped_column(nullable=False)


class User(ModelBase):
    """Модель таблицы пользователей.\n
    Наследует класс <code>ModelBase</code>
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, nullable=False)
    telegram_chat_id = mapped_column(BigInteger, nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='SET NULL'), nullable=True)


class UserForm(ModelBase):
    """Модель таблицы заявок пользователей.\n
    Наследует класс <code>ModelBase</code>
    """
    __tablename__ = 'forms'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id = mapped_column(BigInteger, nullable=False)
    telegram_chat_id = mapped_column(BigInteger, nullable=False)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(30), nullable=False)


class Group(ModelBase):
    """Модель таблицы групп пользователей.\n
    Наследует класс <code>ModelBase</code>
    """
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)