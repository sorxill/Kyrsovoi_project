"""
Основная точка запуска Telegram проложения.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import BotCommand

from bot.keyboards import keyboard_for_start, keyboard_for_choose_test
from bot_config import TG_TOKEN

# Задаем объект типа Bot, который отвечает за взаимодействие с Telegram Bot API.
bot = Bot(token=TG_TOKEN, parse_mode="HTML")

# Создаем диспетчер(Dispatcher) - отвечает за управление(распределение) команд по роутерам.
dp = Dispatcher(bot, storage=MemoryStorage())


async def set_commands(bot_type: Bot) -> None:
    """
    Метод, устанавливающий команды для всего бота. (Внизу всплывающая кнопка быстрых команд).

    :param bot_type: Передаем сюда объект типа Bot.

    :return: None. Ничего не возвращает, тк изменяем состояние переданного объекта.
    """
    # Список статических команд бота.
    commands = [
        BotCommand(command="/start", description="Меню бота")
    ]

    # Устанавливаем боту список статических команд.
    await bot_type.set_my_commands(commands)


async def on_startup() -> None:
    """
    Метод, отвечающий за команды, который происходят при запуске бота.
    В данном случае - информирует нас в консоль о начале работы бота.

    :return: None. Вывод в консоль информации о начале работы.
    """
    # Логирование в консоль.
    logging.info("Bot start working...")


async def on_shutdown():
    """
    Метод, отвечающий за команды, который происходят при отключении бота.
    В данном случае - информирует нас в консоль о завершении работы бота.

    :return: None. Вывод в консоль информации о закрытии.
    """
    # Логирование в консоль.
    logging.warning("Shutting down..")


class CreateTest(StatesGroup):
    """
    Класс, отвечающий за состояния(State).
    Конкретно этот отвечает за состояния создания тестов.

    :cvar waiting_for_test_name: Состояние ожидания создания теста.
    """
    waiting_for_test_name = State()


class MainState(StatesGroup):
    """
    Класс, отвечающий за состояния(State).
    Конкретно этот отвечает за состояния в общем меню.

    :cvar start_state: Состояние начального меню. Основное состояние.
    :cvar choose_test: Состояние отвечающее за выбор тестов, которые можно пройти.
    :cvar choose_create_test: Состояние отвечающее за создание тестов.
    """
    start_state = State()
    choose_test = State()
    choose_create_test = State()


@dp.message_handler(Command('start'), state="*")
async def cmd_hello(message: Message, state: FSMContext) -> None:
    """
    Метод, отвечающий за приветственное сообщение.
    - Удаляет прошлые состояния.
    - Отправляет сообщение о выборе.
    - Отправляет к сообщению клавиатуру с выбором.
    - Удаляет прошлое сообщение, чтобы не сорить чат.
    - Устанавливает состояние начального меню.

    :param message: Сообщение, в котором была вызвана команда "/start".
    :param state: Состояние, которое было на текущий момент вызова команды.

    :return: None. Отправляем сообщение в чат с начальным меню.
    """
    # Завершаем все прошлые состояния.
    await state.finish()

    # Формируем текст ответа, используя f-строку для вставки полного имени из данных сообщения.
    content = f"Выберите что Вам нужно, {message.from_user.full_name}:"

    # Клавиатура для прикрепления к сообщению.
    keyboard = keyboard_for_start.keyboard_for_start

    # Отправляем сообщение и прикрепляем к нему клавиатуру основного меню.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    # Удаляем сообщение с командой "/start".
    await message.delete()

    # Устанавливаем состояние на состояние основного меню.
    await state.set_state(MainState.start_state.state)


@dp.message_handler(Text(equals="Пройти тест"), state=MainState.start_state)
async def go_to_test(message: Message, state: FSMContext):
    """
    Метод, который реализует переход от главного меню, к меню выбора тестов, для прохождения.

    :param message: Сообщение == "Пройти тест". Можем взять из него любую информацию.
    :param state: Текущее состояние. Можно сюда попасть только из основного меню.

    :return: None. Сообщение с выбором нужного теста. И клавиатурой.
    """
    # Текст сообщения, которое мы отправим.
    content = "Выбери нужный тест:"

    # Отправка сообщения в чат, с выбором тестов.
    await message.answer(
        text=content,
    )

    # Удаляем сообщение "Пройти тест", чтобы не засорять чат.
    await message.delete()

    # Устанавливаем состояние выбора тестов.
    await state.set_state(MainState.choose_test.state)


@dp.message_handler(Text(equals="Создать тест"), state=MainState.start_state)
async def create_test(message: Message, state: FSMContext):
    """
    Метод, который осуществляет переход от главного меню, к меню создание тестов, сначала спрашивает точно ли мы хотим
    создать тест, или нет.

    :param message: Сообщение вида "Создать тест". Можем получить из него информацию.
    :param state: Состояние на момент вызова этого метода. Вызывается только из основного меню.

    :return: None. Сообщение с текстом, а также клавиатурой "да/нет".
    """
    # Текст сообщения, которое мы отправим.
    content = "Хотите создать тест:"

    # Клавиатура для прикрепления к сообщению. "ДА" / "НЕТ".
    keyboard_for_choose_create_test = keyboard_for_choose_test.choose_test_keyboard

    # Отправка сообщения в чат, с выбором да/нет.
    await message.answer(
        text=content,
        reply_markup=keyboard_for_choose_create_test,
    )

    # Устанавливаем состояние выбора да/нет.
    await state.set_state(MainState.choose_create_test.state)


@dp.message_handler(Text(equals="Профиль"), state=MainState.start_state)
async def show_profile(message: Message, state: FSMContext):
    """
    Метод, который реализует отображение профиля студента/преподавателя.

    :param message: Сообщение вида "Профиль". Можно получить отсюда информацию.
    :param state: Состояние при вызове. Можно вызвать только из основного меню.

    :return: None. Сообщение с информацией профиля.
    """
    # Текст сообщения, которое мы отправим.
    content = "Вот твой профиль:"

    # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
    keyboard = ReplyKeyboardRemove()

    # Отправка сообщения в чат с информацией о профиле и удаление клавиатуры.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    # Завершаем состояние. Тк дальше идти некуда, кроме меню.
    await state.finish()


@dp.message_handler(Text(equals="Тех. Поддержка"), state=MainState.start_state)
async def tech_help(message: Message, state: FSMContext):
    """
    Метод, который дает информацию о Тех. Поддержке.

    :param message: Сообщение вида "Тех. Поддержка". Можно получить отсюда информацию.
    :param state: Состояние при вызове. Можно вызвать только из основного меню.

    :return: None. Сообщение с информацией о Тех. Поддержке.
    """
    # Текст сообщения, которое мы отправим.
    content = "Вот твой профиль:"

    # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
    keyboard = ReplyKeyboardRemove()

    # Отправка сообщения в чат с информацией о Тех. Поддержке и удаление клавиатуры.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    # Завершаем состояние. Тк дальше идти некуда, кроме меню.
    await state.finish()


# @dp.message_handler()
# async def echo(message: Message):
#     response = requests.post(f"http://0.0.0.0:9000/?msg={message.text}")
#     ans = json.loads(response.text).get("args")
#     await message.answer(f"{ans['up']}, {ans['low']}, {ans['base']}")

async def main():
    """
    Основная функция запуска бота.

    :return: None. Инициализирует работу бота.
    """
    # Установка статических команд.
    await set_commands(bot)

    # Пропускам обновления, которые к нам приходили, когда бот был отключен - чтобы не сломать логику.
    await dp.skip_updates()

    # Логи в консоль информации о боте.
    logging.basicConfig(level=logging.INFO)

    # Запускаем диспетчер(Dispatcher) в режиме "long_polling" -> мы сами получаем обновления об сервера (Tg bot API).
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
