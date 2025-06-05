from aiogram.fsm.state import State, StatesGroup


class UserRegestrationStates(StatesGroup):
    """Класс группы состояний для процедуры регистрации пользователя.\n
    Наследует <code>StatesGroup</code>
    """

    full_name = State()
    email = State()
