import random

import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from bot.db.postgres import get_user_data, add_stats_for_user
from bot.keyboards.keyboard_for_start import keyboard_for_start
from bot.states.states import MainState


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

    if message.text == "/start":
        # Формируем текст ответа, используя f-строку для вставки полного имени из данных сообщения.
        content = f"Выберите что Вам нужно, {message.from_user.full_name}:"

        # Клавиатура для прикрепления к сообщению.
        keyboard = keyboard_for_start

        # Отправляем сообщение и прикрепляем к нему клавиатуру основного меню.
        await message.answer(
            text=content,
            reply_markup=keyboard,
        )

        # Удаляем сообщение с командой "/start".
        await message.delete()

        # Устанавливаем состояние на состояние основного меню.
        await state.set_state(MainState.start_state.state)
    else:
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
    content = "Чтобы выбрать тест напишите и отправьте название теста без пробелов и в нужном регистре.\n\n"

    list_all_test = await list_test()

    if len(list_all_test) != 0:

        # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
        keyboard = ReplyKeyboardRemove()

        for i in range(len(list_all_test)):
            content += f"{i + 1}) {list_all_test[i][0]}\n"

        # Отправка сообщения в чат, с выбором тестов.
        await message.answer(
            text=content,
            reply_markup=keyboard,
        )

        # Удаляем сообщение "Пройти тест", чтобы не засорять чат.
        await message.delete()

        # Устанавливаем состояние выбора тестов.
        await state.set_state(MainState.choose_test.state)
    else:
        await message.answer(
            text="Сейчас нет никаких доступных тестов."
        )
        await cmd_hello(message, state)


async def testing_choose(message: Message, state: FSMContext):
    chosen_test = message.text

    response = requests.get("http://127.0.0.1:8000/test_info", {"name": chosen_test})
    all_good = response.json()
    if all_good:
        message_test, right_answer = await get_message_for_test(all_good)
        await message.answer(text=message_test)
        await state.set_data(right_answer.get("data").strip())
        await state.set_state(MainState.testing_process)
    else:
        await message.answer(
            text="Такого теста не существует, проверьте правильность."
        )

        await state.set_state(MainState.start_state)
        return await go_to_test(message, state)


async def testing_process(message: Message, state: FSMContext):
    data = await state.get_data()
    data_text = message.text
    if data_text == data:
        await add_stats_for_user(user_id=message.from_user.id, is_good=True)
        await message.answer(
            text="Вы успешно прошли тест, ваша статистика обновлена!\nПоздравляем!"
        )
        return await cmd_hello(message, state)
    else:
        await add_stats_for_user(user_id=message.from_user.id, is_good=False)
        await message.answer(
            text="Вы не прошли тест, ваша статистика обновлена.\nПопробуй ещё разок!"
        )
        return await cmd_hello(message, state)


async def get_message_for_test(test_info: list) -> tuple[str, dict]:
    content = "Вы выбрали тест: " + test_info[0][-1] + ("\n\n-----\nПример ответа:\n\n1-ИКСС\n2-М.А.Бонч-Бруевич\n"
                                                        "3-1703\n-----\n")
    right_answer = ""
    for i in range(0, len(test_info)):
        content += f"{i+1}) {test_info[i][0]}"
        right_answer += f"{i+1}-{test_info[i][-2]}\n"
        content += "\n\n"
        answers = [test_info[i][1], test_info[i][2], test_info[i][3], test_info[i][4]]
        answers_random = random.sample(answers, 4)
        content += f"1){answers_random[0]}\n2){answers_random[1]}\n3){answers_random[2]}\n4){answers_random[3]}"
        content += "\n\n"
    return content, {"data": right_answer}


async def create_test(message: Message, state: FSMContext):
    """
    Метод, который осуществляет переход от главного меню, к меню создание тестов, сначала спрашивает точно ли мы хотим
    создать тест, или нет.

    :param message: Сообщение вида "Создать тест". Можем получить из него информацию.
    :param state: Состояние на момент вызова этого метода. Вызывается только из основного меню.

    :return: None. Сообщение с текстом.
    """
    # Текст сообщения, которое мы отправим.
    content = "Для создания текста необходимо написать 10 вопросов и ответов к ним в определенном формате, " \
              "описанном ниже.\nОбязательные параметры для корректного теста:\n - КАЖДЫЙ вопрос оканчивается '?'\n" \
              "- Чтобы корректно составить тест необходимо вводить вопрос ответ СТРОГО в заданном формате, учитывая " \
              "пробелы, знаки препинания и т.д\n- КАЖДЫЙ тест должен иметь УНИКАЛЬНОЕ название.\n\n!!! Если хотите " \
              "добавить 10 вопросов к уже существующему тесту - напишите его название, без пробелов(как он записан" \
              " при выборе тестов) и дальше вопросы как в примере\n\n" \
              "Пример:\n\nОбщий тест\n\nНазовите год основания города Санкт-Петербрг?\n1803/1802/1905/1703 (1703)\n\n" \
              "В честь кого назван СПбГУТ?\nМ.А.Бонч-Бруевич/А.С.Пушкин/А.Н.Николаева/Э.Р.Мамедова (М.А.Бонч-Бруевич)" \
              "\n\n...\n\nНа каком вы факультете?\nРТС/ИКСС/СЦТ/ЦЕУБИ (ИКСС)"

    # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
    keyboard = ReplyKeyboardRemove()

    # Отправка сообщения в чат.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    # Устанавливаем состояние создания теста.
    await state.set_state(MainState.choose_create_test.state)


async def created_test(message: Message, state: FSMContext):

    message_text = message.text

    objects = await get_dict_with_test(message_text)

    if await create_test_from_db(objects):
        await message.answer(
            text="Вопрос был занесен в базу данных.",
        )
    else:
        await message.answer(
            text="Во время создания теста произошла ошибка.\nПроверьте корректность вопросов или обратитесь в поддержку"
        )

    await cmd_hello(message, state)


async def get_dict_with_test(text: str) -> dict:

    objects = {}

    result = text.split("\n\n")
    test_name = result[0]
    result = result[1:]
    objects["test_name"] = test_name
    counter = 1
    for answer in result:
        objects_ = {}
        question, answers = answer.split("?")
        question += "?"
        objects_["question"] = question.strip()
        answer_1, answer_2, answer_3, answer_4 = answers.strip().split("/")
        answer_4, correct_answer = answer_4.split("(")
        correct_answer = correct_answer[:-1]
        answer_4 = answer_4[:-1]
        objects_["answer_1"] = answer_1.strip()
        objects_["answer_2"] = answer_2.strip()
        objects_["answer_3"] = answer_3.strip()
        objects_["answer_4"] = answer_4.strip()
        objects_["correct_answer"] = correct_answer.strip()
        objects[f"quest_{counter}"] = objects_
        counter += 1

    return objects


async def create_test_from_db(test_dict: dict) -> bool:
    response = requests.post("http://127.0.0.1:8000/create_test", json=test_dict)
    all_good = response.text
    if all_good == "true":
        return True
    else:
        return False


async def list_test():
    response = requests.get("http://127.0.0.1:8000/test_list")
    answer = response.json()
    return answer


async def show_profile(message: Message, state: FSMContext):
    """
    Метод, который реализует отображение профиля студента/преподавателя.

    :param message: Сообщение вида "Профиль". Можно получить отсюда информацию.
    :param state: Состояние при вызове. Можно вызвать только из основного меню.

    :return: None. Сообщение с информацией профиля.
    """
    # Текст сообщения, которое мы отправим.
    content = ""

    if not await get_user_data(message.from_user.id, message.from_user.full_name):

        user_id, all_test, good_tests, name = await get_user_data(message.from_user.id,
                                                                  message.from_user.full_name,
                                                                  is_create=True
                                                                  )
    else:
        user_id, all_test, good_tests, name = await get_user_data(message.from_user.id, message.from_user.full_name)

    content += (f"ID пользователя: {user_id}\n\nИмя пользователя: {name}\n\nКоличество пройденных тестов: {all_test}"
                f"\n\nПоложительных тестов: {good_tests}")

    # Вызываем класс удаления клавиатуры у сообщения. Поэтому в конце у класса стоит "()".
    keyboard = ReplyKeyboardRemove()

    # Отправка сообщения в чат с информацией о профиле и удаление клавиатуры.
    await message.answer(
        text=content,
        reply_markup=keyboard,
    )

    await cmd_hello(message, state)


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

    await cmd_hello(message, state)


# регистрируем хендлер
def register_base_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_hello, Command('start'), state="*")
    dp.register_message_handler(go_to_test, Text(equals="Пройти тест"), state=MainState.start_state)
    dp.register_message_handler(create_test, Text(equals="Создать тест"), state=MainState.start_state)
    dp.register_message_handler(show_profile, Text(equals="Профиль"), state=MainState.start_state)
    dp.register_message_handler(tech_help, Text(equals="Тех. Поддержка"), state=MainState.start_state)
    dp.register_message_handler(created_test, state=MainState.choose_create_test)
    dp.register_message_handler(testing_choose, state=MainState.choose_test)
    dp.register_message_handler(testing_process, state=MainState.testing_process)
