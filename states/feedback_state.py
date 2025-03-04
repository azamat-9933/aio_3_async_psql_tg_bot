from aiogram.fsm.state import StatesGroup, State


class FeedbackStatesGroup(StatesGroup):
    ask_feedback = State()