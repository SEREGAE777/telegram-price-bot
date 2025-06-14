from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Бот работает!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
