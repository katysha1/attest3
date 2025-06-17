from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from notes_tg import delete_notes_keyboard
from states.state_bot import NoteStates
from notes_tg import user_notes
from keyboard.main_menu import inline_go


router = Router()

@router.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(text='Выбери действие', reply_markup = inline_go)

@router.message(Command('exit'))
async def exit_func(message: Message):
     await message.answer("Вы вышли из режима заметок. До встречи!")


@router.callback_query(F.data == 'add_task')
async  def waiting_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите текст заметки:")
    await state.set_state(NoteStates.waiting_for_note)
    await callback.answer()

@router.message(NoteStates.waiting_for_note)
async def add_note(message: Message, state: FSMContext):
    user_notes.setdefault(message.from_user.id, []).append(message.text)
    await message.answer(text="Заметка успешно добавлена!", reply_markup=inline_go)
    await state.set_state(NoteStates.add_note)


@router.callback_query(F.data == 'delete_task')
async def show_notes_to_delete(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    notes = user_notes.get(user_id, [])
    if notes:
        await callback.message.answer(
            text="Выберите заметку для удаления:",
            reply_markup=delete_notes_keyboard(notes)
        )
        await state.set_state(NoteStates.waiting_for_delete)
    else:
        await callback.message.answer("У вас нет заметок для удаления.")
    await callback.answer()

@router.callback_query(F.data.startswith('del_note_'), NoteStates.waiting_for_delete)
async def delete_note(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    notes = user_notes.get(user_id, [])
    idx = int(callback.data.split('_')[-1])
    if 0 <= idx < len(notes):
        deleted = notes.pop(idx)
        await callback.message.answer(f"Заметка удалена: {deleted}")
    else:
        await callback.message.answer("Заметка не найдена.")
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == 'print_tasks')
async def print_tasks(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    notes = user_notes.get(user_id, [])
    if notes:
        text = "\n".join([f"{idx+1}. {note}" for idx, note in enumerate(notes)])
    else:
        text = "У вас пока нет заметок."
    await callback.message.answer(text=text, reply_markup=inline_go)
    await callback.answer()