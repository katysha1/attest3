import os
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from handlers import user_handler
from dotenv import load_dotenv


dp=Dispatcher()
dp.include_router(user_handler.router)

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))


    await dp.start_polling(bot)

if __name__ == '__main__':

    try:
        asyncio.run(main())
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    except:
        print('Exit')