import asyncio
import logging
import os

from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import handlers


load_dotenv()


logging.basicConfig(
    level=logging.WARNING,
    filename = "logs/errors.log",
    format = "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    )


async def main():
    bot = Bot(token=os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
  

if __name__ == "__main__":
    asyncio.run(main())
