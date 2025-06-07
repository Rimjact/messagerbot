from aiogram.fsm.state import State, StatesGroup


class UserRegestrationStates(StatesGroup):
    """Класс группы состояний для процедуры регистрации пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    full_name = State()
    email = State()


class UserChangeDataStates(StatesGroup):
    """Класс группы состояний для процедуры редактирования данных пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    user_telegram_id = State()
    full_name = State()
    email = State()


class UserChangeGroupStates(StatesGroup):
    """Класс группы состояний для процедуры переноса пользователя в группу.\n
    Наследует <code>StatesGroup</code>
    """

    user_telegram_id = State()
    group_id = State()


class UserDeleteStates(StatesGroup):
    """Класс группы состояний для процедуры удаления пользователя из БД.\n
    Наследует <code>StatesGroup</code>
    """

    user_telegram_id = State()

class GroupAddNewStates(StatesGroup):
    """Класс группы состояний для процедуры создания новой группы.\n
    Наследует <code>StatesGroup</code>
    """

    name = State()


class GroupDeleteStates(StatesGroup):
    """Класс группы состояний для процедуры удаления группы.\n
    Наследует <code>StatesGroup</code>
    """

    id_or_name = State()


class GroupChangeNameStates(StatesGroup):
    """Класс группы состояний для процедуры изменения имени группы.\n
    Наследует <code>StatesGroup</code>
    """

    id_or_name = State()
    new_name = State()