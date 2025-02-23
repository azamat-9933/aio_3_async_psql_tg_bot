from aiogram.fsm.state import StatesGroup, State


class RegistrationStatesGroup(StatesGroup):
    wait_full_name = State()
    wait_phone_number = State()
    wait_for_submit = State()