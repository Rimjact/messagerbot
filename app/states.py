from aiogram.fsm.state import State, StatesGroup


class UserRegestrationStates(StatesGroup):
    """Класс группы состояний для процедуры регистрации пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    full_name = State()
    email = State()


class GroupAddNewStates(StatesGroup):
    """Класс группы состояния для процедуры создания новой группы.\n
    Наследует <code>StatesGroup</code>
    """

    name = State()


class GroupDeleteStates(StatesGroup):
    """Класс группы состояния для процедуры удаления группы.\n
    Наследует <code>StatesGroup</code>
    """

    id_or_name = State()


class GroupChangeNameStates(StatesGroup):
    """Класс группы состояния для процедуры изменения имени группы.\n
    Наследует <code>StatesGroup</code>
    """

    id_or_name = State()
    new_name = State()