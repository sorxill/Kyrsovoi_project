import psycopg2
from psycopg2 import Error

from config.app_config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.api.models import Question


async def create_test_db(test_name: str, test_data: Question) -> bool:
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
        cursor.execute("INSERT INTO kyrsovoi.test VALUES (%s, %s, %s, %s, %s, %s, %s)", (
            test_data.question,
            test_data.answer_1,
            test_data.answer_2,
            test_data.answer_3,
            test_data.answer_4,
            test_data.correct_answer,
            test_name,
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except (Exception, Error) as error:
        return False
