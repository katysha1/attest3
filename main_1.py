import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from datetime import datetime
import asyncio
from aiogram import Bot, Dispatcher, types
import uvicorn

load_dotenv()

class Item(BaseModel):
    task: str
    deadline: datetime

    @field_validator('deadline')
    def validate_deadline(cls, v):
        if isinstance(v, datetime):
            return v
        try:
            return datetime.strptime(v, "%d.%m.%Y")
        except ValueError:
            raise ValueError("deadline должен быть в формате ДД.ММ.ГГГГ")

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
app = FastAPI()

# Пример обработчика сообщений
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Получено: {message.text}")

# Запуск бота
async def start_polling():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

# Маршрут FastAPI
@app.get("/")
async def read_root():
    return {"status": "Bot is running"}

# Асинхронная функция запуска uvicorn сервера через Server (не блокирует)
async def start_uvicorn():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, reload=False)
    server = uvicorn.Server(config)
    await server.serve()

# Основная функция запуска uvicorn и бота параллельно
async def main():
    await asyncio.gather(
        start_uvicorn(app),
        start_polling()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutdown")

