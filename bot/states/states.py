from aiogram.dispatcher.filters.state import StatesGroup, State


class MainState(StatesGroup):
    """
    Класс, отвечающий за состояния(State).
    Конкретно этот отвечает за состояния в общем меню.

    :cvar start_state: Состояние начального меню. Основное состояние.
    :cvar choose_test: Состояние отвечающее за выбор тестов, которые можно пройти.
    :cvar choose_create_test: Состояние отвечающее за создание тестов.
    """
    start_state = State()
    choose_test = State()
    choose_create_test = State()
