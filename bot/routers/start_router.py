from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import keyboard_for_start, keyboard_for_choose_test
from states.states import MainState


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


async def tech_help(message: Message, state: FSMContext):
    """
    Метод, который дает информацию о Тех. Поддержке.

    :param message: Сообщение вида "Тех. Поддержка". Можно получить отсюда информацию.
    :param state: Состояние при вызове. Можно вызвать только из основного меню.

    :return: None. Сообщение с информацией о Тех. Поддержке.
    """
    # Текст сообщения, которое мы отправим.
    content = "Если возникли проблемы - пишите на почту ..."

    # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
    keyboard = ReplyKeyboardRemove()

    # Отправка сообщения в чат с информацией о Тех. Поддержке и удаление клавиатуры.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    # Завершаем состояние. Тк дальше идти некуда, кроме меню.
    await state.finish()


# регистрируем хендлер
def register_base_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_hello, Command('start'), state="*")
    dp.register_message_handler(go_to_test, Text(equals="Пройти тест"), state=MainState.start_state)
    dp.register_message_handler(create_test, Text(equals="Создать тест"), state=MainState.start_state)
    dp.register_message_handler(show_profile, Text(equals="Профиль"), state=MainState.start_state)
    dp.register_message_handler(tech_help, Text(equals="Тех. Поддержка"), state=MainState.start_state)

