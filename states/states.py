from aiogram.fsm.state import StatesGroup, State


class Session(StatesGroup):
    ask_text = State()
    ask_filters = State()

    ask_salary = State()
    ask_count = State()

    ask_search_field = State()
    ask_experience = State()
    ask_only_with_salary = State()

    ask_order_by = State()

    get_data = State()
    