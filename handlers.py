import aiohttp
from aiogram import Router, F
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import except_

from keyboards import inline_go, kb_reply
from config import API_BASE_URL
from datetime import datetime

router = Router()

class AddTaskStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_deadline = State()
    waiting_for_delete_id = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text= "Привет! Это бот по сохранению списка задач. Выбери что нужно сделать:", reply_markup=inline_go)

@router.callback_query(F.data =='exit')
async def exit_func(query: CallbackQuery):
     await query.message.answer(text = "Вы вышли из режима задач. Чтобы продолжить работу выберите действие:", reply_markup=inline_go)


#Добавить задачу
@router.callback_query(F.data == "add_task")
async def add_task_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text="Введите название задачи:")
    await state.set_state(AddTaskStates.waiting_for_name)
    await callback.answer()

@router.message(AddTaskStates.waiting_for_name, F.date)
async def task_name(message: types.Message, state: FSMContext):
    task_name=message.text
    # await state.update_data(task_name=message.text)
    await message.answer(text="Введите дату дедлайна в формате ДД.ММ.ГГГГ")
    await state.set_state(AddTaskStates.waiting_for_deadline)

@router.message(AddTaskStates.waiting_for_deadline, F.text)
async def dedline(message: types.Message, state: FSMContext):
    date_text = message.text

    try:
        deadline_date = datetime.strptime(date_text, "%d.%m.%Y").date()
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_BASE_URL}/tasks/") as resp:
                if resp.status == 200:
                    await state.update_data(deadline_data=message.text)
                    await message.answer(f"Задача  с дедлайном успешно добавлена в базу данных")
    except:
        pass

#Удалить задачу
@router.callback_query(F.data == "delete_task")
async def delete_task_start(callback: CallbackQuery, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/tasks/") as resp:
            tasks = await resp.json()

            await callback.message.answer(f"Задачи:\n{tasks}")

            if resp.status != 200:
                await callback.message.answer("Введите ID задачи для удаления:")
                # await state.set_state("waiting_for_delete_id")
                await callback.answer()
            else:
                pass

@router.message(F.state == AddTaskStates.waiting_for_delete_id)
async def delete_task_confirm(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите числовой ID задачи.")
        return
    task_id = int(message.text)

    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_BASE_URL}/tasks/{task_id}") as resp:
            if resp.status == 204:
                await message.answer(f"Задача с ID {task_id} удалена.")
            elif resp.status == 404:
                await message.answer("Задача с таким ID не найдена.")
            else:
                await message.answer("Ошибка при удалении задачи.")
    await state.clear()


#Список задач
@router.callback_query(F.data == "tasks")
async def tasks_list(callback: CallbackQuery):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_BASE_URL}/tasks/") as resp:
            if resp.status != 200:
                await callback.message.answer(text="Не удалось получить список задач. Добавьте сначала задачи", reply_markup=inline_go)
                # await callback.message.answer(text="Добавьте сначала задачи", reply_markup=inline_go)
                return
            tasks = await resp.json()

    if not tasks:
        await callback.message.answer("Список задач пуст.")
    else:
        text = "\n".join([f"{t['id']}. {t['name']} (до {t['deadline']})" for t in tasks])
        await callback.message.answer(f"Задачи:\n{text}")
    await callback.message.answer(text="Что еще нужно сделать?", reply_markup=inline_go)