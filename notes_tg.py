user_notes = {}

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def delete_notes_keyboard(notes):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Удалить: {note[:30]}", callback_data=f"del_note_{idx}")]
            for idx, note in enumerate(notes)
        ]
    )