from typing import Any

import psycopg2
from psycopg2 import Error

from config.app_config import DB_USER, DB_PORT, DB_PASS, DB_NAME, DB_HOST


async def get_user_data(user_id: int, user_name: str, is_create: bool = False) -> Any | None:
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
        if is_create:
            cursor.execute("INSERT INTO kyrsovoi.profile VALUES (%s, 0, 0, %s)", (user_id, user_name,))
            connection.commit()
            cursor.execute("SELECT * FROM kyrsovoi.profile WHERE user_id = %s", (user_id,))
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return record
        else:
            # Выполнение SQL-запроса
            cursor.execute("SELECT * FROM kyrsovoi.profile WHERE user_id = %s", (user_id,))
            # Получить результат
            record = cursor.fetchone()
            cursor.close()
            connection.close()
            return record

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


async def add_stats_for_user(user_id: int, is_good: bool) -> None:
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
        if is_good:
            cursor.execute("UPDATE kyrsovoi.project SET count_test = count_test + 1, success_test = success_test + 1 "
                           "WHERE user_id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()
        else:
            # Выполнение SQL-запроса
            cursor.execute("UPDATE kyrsovoi.project SET count_test = count_test + 1 WHERE user_id = %s", (user_id,))
            connection.commit()
            cursor.close()
            connection.close()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
