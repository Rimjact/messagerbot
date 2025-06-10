from aiogram.fsm.state import StatesGroup, State


class GroupNewStates(StatesGroup):
    """Класс группы состояний для процедуры
    создания новой группы.\n
    Наследует <code>StatesGroup</code>
    """

    name = State()


class GroupDeleteStates(StatesGroup):
    """Класс группы состояний для
    процедуры удаления группы.\n
    Наследует <code>StatesGroup</code>
    """

    group_id = State()


class GroupChangeNameStates(StatesGroup):
    """Класс группы состояний для процедуры
    изменения имени группы.\n
    Наследует <code>StatesGroup</code>
    """

    group_id = State()
    new_name = State()