import re
import os
import asyncio
from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types, executor

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")  # Например: @BigSaleApple
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")  # Например: @topapple1
ADD_NORMAL = int(os.getenv("ADD_NORMAL", 5000))
ADD_16 = int(os.getenv("ADD_16", 10000))

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot)

client = TelegramClient('parser_session', API_ID, API_HASH)

def add_markup_to_prices(text):
    def replacer(match):
        price = int(match.group(1).replace(' ', '').replace(' ', ''))
        if re.search(r'16(?:\s|\D)*(Pro Max|Pro|Plus)?', text, re.IGNORECASE):
            return str(price + ADD_16)
        return str(price + ADD_NORMAL)
    return re.sub(r'\b(\d{4,6})(?:[  ]?₽)?\b', replacer, text)

def format_text(orig: str) -> str:
    text = add_markup_to_prices(orig)
    return text

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    text = event.message.message
    processed = format_text(text)
    await bot.send_message(chat_id=TARGET_CHANNEL, text=processed)

async def main():
    await client.start()
    print("✅ Parser client started")
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=True)
