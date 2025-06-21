import aiohttp
from aiogram import Router
from aiogram.types import Message
from config import ADMIN_IDS, API_BASE_URL

router = Router()

@router.message(lambda m: m.from_user.id in ADMIN_IDS and m.text == "/admin")
async def cmd_admin(message: Message):
    await message.answer("⚙️ Панель администратора:\n" +
        "/create_user <имя> - создать пользователя\n" +
        "/broadcast <текст> - рассылка всем"
    )

@router.message(lambda m: m.from_user.id in ADMIN_IDS and m.text.startswith("/create_user"))
async def cmd_create(message: Message):
    name = message.text[len("/create_user "):].strip()
    async with aiohttp.ClientSession() as session:
        resp = await session.post(f"{API_BASE_URL}/users/", json={"name": name})
        data = await resp.json()
    await message.answer(f"Создан пользователь: {data['name']} (ID: {data['id']})")

@router.message(lambda m: m.from_user.id in ADMIN_IDS and m.text.startswith("/broadcast"))
async def cmd_broadcast(message: Message):
    text = message.text[len("/broadcast "):].strip()
    async with aiohttp.ClientSession() as session:
        users = await (await session.get(f"{API_BASE_URL}/users/")).json()
    for u in users:
        try:
            await message.bot.send_message(u["id"], text)
        except:
            pass
    await message.answer("Рассылка завершена.")