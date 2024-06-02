"""
Основная точка запуска Telegram проложения.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from routers.start_router import register_base_commands
from config.app_config import TG_TOKEN


# @dp.message_handler()
# async def echo(message: Message):
#     response = requests.post(f"http://0.0.0.0:9000/?msg={message.text}")
#     ans = json.loads(response.text).get("args")
#     await message.answer(f"{ans['up']}, {ans['low']}, {ans['base']}")

# регистрация хендлера
def register_all_handlers(dp):
    register_base_commands(dp)


async def main():
    # Задаем объект типа Bot, который отвечает за взаимодействие с Telegram Bot API.
    bot = Bot(token=TG_TOKEN, parse_mode="HTML")

    # Создаем диспетчер(Dispatcher) - отвечает за управление(распределение) команд по роутерам.
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Логи в консоль информации о боте.
    logging.basicConfig(level=logging.INFO)

    await bot.set_my_commands([BotCommand(command="/start", description="Меню бота")])
    await dp.skip_updates()

    register_all_handlers(dp)

    # запуск пулинга
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped.")
