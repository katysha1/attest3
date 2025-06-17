from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton


bth1=KeyboardButton(text='Продолжить')
bth2=KeyboardButton(text='Выход')

keyboard_reply = ReplyKeyboardMarkup(keyboard=[
    [bth1, bth2]
], resize_keyboard=True, one_time_keyboard=True)