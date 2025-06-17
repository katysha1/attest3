from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_go = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавление новой заметки', callback_data='add_task')],
    [InlineKeyboardButton(text='Удалить заметку', callback_data='delete_task')],
    [InlineKeyboardButton(text='Просмотр списка всех заметок', callback_data='print_tasks')]
])