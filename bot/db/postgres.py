from typing import Any

import psycopg2
from psycopg2 import Error


async def get_user_data(user_id: int, is_create: bool = False) -> Any | None:
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="admin",
                                      # пароль, который указали при установке PostgreSQL
                                      password="admin",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="kyrs",
                                      )

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        if is_create:
            cursor.execute("INSERT INTO kyrsovoi.profile VALUES (%s)", (user_id,))
            connection.commit()
            cursor.execute("SELECT * FROM kyrsovoi.profile WHERE user_id = %s", (user_id,))
            record = cursor.fetchone()
            return record
        else:
            # Выполнение SQL-запроса
            cursor.execute("SELECT * FROM kyrsovoi.profile WHERE user_id = %s", (user_id,))
            # Получить результат
            record = cursor.fetchone()
            return record

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
