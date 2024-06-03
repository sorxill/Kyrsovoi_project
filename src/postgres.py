import psycopg2
from psycopg2 import Error

from config.app_config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.api.models import Question, Test


async def create_test_db(test_name: str, test_data: Question) -> bool:
    """
    Метод, для создания записи теста в БД.

    :param test_name: Название теста.
    :param test_data: Содержимое теста в формате модели Question(Валидация на входе).

    :return: True / False - исполнился ли запрос корректно.
    """
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=DB_USER,
                                      # пароль, который указали при установке PostgreSQL
                                      password=DB_PASS,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME,
                                      )

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение запроса в БД. %s - это указание порядка столбца и какое значение туда вставить.
        cursor.execute("INSERT INTO kyrsovoi.test VALUES (%s, %s, %s, %s, %s, %s, %s)", (
            test_data.question,
            test_data.answer_1,
            test_data.answer_2,
            test_data.answer_3,
            test_data.answer_4,
            test_data.correct_answer,
            test_name,
        ))

        # Сохранение изменений в соединении.
        connection.commit()

        # Закрываем курсор, чтобы избежать утечек.
        cursor.close()

        # Закрываем соединение к БД.
        connection.close()
        return True

    # Вызываем блок ошибок и возвращает False.
    except (Exception, Error) as error:
        return False


async def get_all_unique_names_test() -> list:
    """
    Метод, которые выдает все уникальные названия тестов.

    :return: Отправляет список всех уникальных тестов.
    """
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=DB_USER,
                                      # пароль, который указали при установке PostgreSQL
                                      password=DB_PASS,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME,
                                      )

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Запрос в БД.
        cursor.execute("SELECT DISTINCT test_name FROM kyrsovoi.test")

        # Забираем из курсора результат выполнения команды execute. Получаем данные о тесте.
        result = cursor.fetchall()

        # Закрываем курсов - от утечек.
        cursor.close()

        # Закрываем соединение.
        connection.close()
        return result

    # Вызываем блок ошибок и возвращает пустой список.
    except (Exception, Error) as error:
        return []


async def get_test_info_by_name(name: str) -> tuple | None:
    """
    Метод получения данных теста по его названию, возвращает 10 случайных вопросов и ответов к ним.

    :param name: Название теста.

    :return: Данные о тесте.
    """
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=DB_USER,
                                      # пароль, который указали при установке PostgreSQL
                                      password=DB_PASS,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME,
                                      )

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        # Запрос в БД.
        cursor.execute("SELECT * FROM kyrsovoi.test WHERE test_name = %s ORDER BY random() LIMIT 10", (name,))

        # Забираем из курсора результат выполнения команды execute. Получаем данные о тесте.
        result = cursor.fetchall()

        # Закрываем курсов - от утечек.
        cursor.close()

        # Закрываем соединение.
        connection.close()
        return result

    # Вызываем блок ошибок, в случае появления ошибок в PostgreSQL.
    except (Exception, Error) as error:
        return None
