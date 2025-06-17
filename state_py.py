from aiogram.fsm.state import StatesGroup, State


class NoteStates(StatesGroup):
    start = State()
    waiting_for_note=State()
    add_note = State()
    delete_note = State()