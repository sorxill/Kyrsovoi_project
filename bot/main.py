import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
import requests
from aiogram.types import BotCommand

from keyboards.keyboard_for_start import keyboard_for_start
from bot_config import TG_TOKEN

bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


async def set_commands(bot_type: Bot):
    commands = [
        BotCommand(command="/start", description="Заказать напитки")
    ]
    await bot_type.set_my_commands(commands)


async def on_startup():
    logging.info("Bot start working...")


async def on_shutdown():
    logging.warning("Shutting down..")


# @dp.message_handler(Command('start'))
# async def cmd_hello(message: types.Message):
#     content = f"Здравствуй, {message.from_user.full_name}"
#     await message.answer(
#         content,
#         reply_markup=keyboard_for_start,
#     )
#     await message.delete()


# @dp.message_handler()
# async def echo(message: Message):
#     response = requests.post(f"http://0.0.0.0:9000/?msg={message.text}")
#     ans = json.loads(response.text).get("args")
#     await message.answer(f"{ans['up']}, {ans['low']}, {ans['base']}")


async def main():
    await set_commands(bot)
    await dp.skip_updates()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
