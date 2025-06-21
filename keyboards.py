from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton


inline_go = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавление новой задачи', callback_data='add_task'),
    InlineKeyboardButton(text='Удалить задачу', callback_data='delete_task')],
    [InlineKeyboardButton(text='Просмотр списка всех задач', callback_data='tasks'),
    InlineKeyboardButton(text='Выход', callback_data='exit')]
])


bth1=KeyboardButton(text='В задачи')
bth2=KeyboardButton(text='Выход')
# bth3=KeyboardButton(text='Список задач')
# bth4=KeyboardButton(text='Выход')


kb_reply = ReplyKeyboardMarkup(keyboard=[
    [bth1, bth2],
    # [bth3, bth4]
], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Выберите пункт меню.')