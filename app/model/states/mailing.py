from aiogram.fsm.state import State, StatesGroup


class MailingForAllUsers(StatesGroup):
    """Класс группы состояний для процедуры создания
    рассылки пользователям.\n
    Наследует <code>StatesGroup</code>
    """

    text = State()


class MailingForUsers(StatesGroup):
    """Класс группы состояний для процедуры создания
    рассылки пользователям.\n
    Наследует <code>StatesGroup</code>
    """

    telegram_ids = State()
    text = State()


class MailingForGroups(StatesGroup):
    """Класс группы состояний для процедуры создания
    рассылки группам.\n
    Наследует <code>StatesGroup</code>
    """

    groups_ids = State()
    text = State()