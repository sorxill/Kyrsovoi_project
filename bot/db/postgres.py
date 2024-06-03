"""
Модуль, отвечающий за взаимодействие бота с БД, с таблицей отвечающей за профиль.
"""
import logging
from typing import Any

import psycopg2
from psycopg2 import Error

from config.app_config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST


async def get_user_data(user_id: int, user_name: str = None, is_create: bool = False) -> Any | None:
    """
    Метод, отвечающий за получение/создание данных о пользователе по его id в телеграмме.

    :param user_id: ID пользователя в телеграмме.
    :param user_name: Имя пользователя в телеграмме.
    :param is_create: Поле, отвечающее како запрос - создание или получение.

    :return: Если все сработало корректно - данные о пользователе, иначе - None.
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

        # Если у нас запрос на создание, создаем запись.
        if is_create:
            cursor.execute("INSERT INTO kyrsovoi.profile VALUES (%s, 0, 0, %s)", (user_id, user_name,))
            connection.commit()

        #  Выполняем запрос к БД, для получения данных пользователя по ID.
        cursor.execute("SELECT * FROM kyrsovoi.profile WHERE user_id = %s", (user_id,))

        # Получить результат
        record = cursor.fetchone()

        # Закрываем курсор, для избежания утечек.
        cursor.close()

        # Закрываем соединение с БД.
        connection.close()
        return record

    # Вызываем блок ошибок, в случае ои=шибки работы с БД.
    except (Exception, Error) as error:
        logging.warning("Ошибка при работе с PostgreSQL", error)


async def add_stats_for_user(user_id: int, is_good: bool = False) -> bool:
    """
    Метод, обновления статистики у пользователя.

    :param user_id: ID пользователя.
    :param is_good: Правильно ли сделан тест.

    :return: Bool - True, если все обновилось корректно, False - если пользователя не существует.
    """
    try:
        # Получаем данные - существует пользователь или нет.
        if await get_user_data(user_id):
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

            # Если тест выполнен корректно - обновляем поля в таблице profile.
            if is_good:
                # Выполнение запроса.
                cursor.execute("UPDATE kyrsovoi.profile SET count_of_test = count_of_test + 1, successfuly_test = "
                               "successfuly_test + 1 WHERE user_id = %s", (user_id,))

                # Сохраняем изменения.
                connection.commit()

                # Закрываем курсор, чтобы избежать утечек данных.
                cursor.close()

                # Закрываем соединение с БД.
                connection.close()
            else:
                # Выполнение SQL-запроса
                cursor.execute("UPDATE kyrsovoi.profile SET count_of_test = count_of_test + 1 WHERE user_id = %s",
                               (user_id,))

                # Сохраняем изменения.
                connection.commit()

                # Закрываем курсор, чтобы избежать утечек.
                cursor.close()

                # Закрываем соединение.
                connection.close()
            return True
        else:
            return False

    # Вызываем блок ошибок.
    except (Exception, Error) as error:
        logging.warning("Ошибка при работе с PostgreSQL", error)
