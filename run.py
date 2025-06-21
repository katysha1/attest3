import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router as user_router
from admin import router as admin_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
