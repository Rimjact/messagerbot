from aiogram.fsm.state import StatesGroup, State


class UserChangeDataStates(StatesGroup):
    """Класс группы состояний для процедуры
    редактирования данных пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    tg_id = State()
    full_name = State()
    email = State()


class UserChangeGroupStates(StatesGroup):
    """Класс группы состояний для процедуры
    изменение группы пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    tg_id = State()
    group_id = State()


class UserDeleteStates(StatesGroup):
    """Класс группы состояний для процедуры
    удаления пользователя из БД.\n
    Наследует <code>StatesGroup</code>
    """

    tg_id = State()