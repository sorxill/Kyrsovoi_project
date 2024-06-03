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


# регистрация хендлера
def register_all_handlers(dp):
    """
    Метод регистрации хендлеров к диспетчеру.
    Метод не является асинхронным. Он выполняется синхронно. Необходимо для того, чтобы обеспечить корректность.

    :param dp: Объект диспетчера.

    :return: None.
    """
    # Вызываем метод регистрации из модуля хендлеров.
    register_base_commands(dp)


async def main():
    # Задаем объект типа Bot, который отвечает за взаимодействие с Telegram Bot API.
    bot = Bot(token=TG_TOKEN, parse_mode="HTML")

    # Создаем диспетчер(Dispatcher) - отвечает за управление(распределение) команд по роутерам.
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Логи в консоль информации о боте.
    logging.basicConfig(level=logging.INFO)

    # Устанавливаем боту основные команды - "/start".
    await bot.set_my_commands([BotCommand(command="/start", description="Меню бота")])

    # Пропускаем все обновления(запросы к боту), пока он был офлайн.
    await dp.skip_updates()

    # Вызываем метод регистрации наших хендлеров.
    register_all_handlers(dp)

    # запуск пулинга
    try:
        await dp.start_polling()
    finally:
        # Закрываем сессию взаимодействия бота с API телеграмма.
        await bot.session.close()


# Блок вызова программы только из файла.
if __name__ == '__main__':
    try:
        # Пытаемся запустить асинхронно функцию main, которая обеспечит работу бота.
        asyncio.run(main())
    # В случае эксренной остановки ("ctrl + c" или другого сочения клавиш)/В случае системной ошибки - вызываем лог.
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped.")
