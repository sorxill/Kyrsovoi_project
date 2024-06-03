"""
Модуль, отвечающий за хендлеры.
"""
from fastapi import APIRouter

from src.api.models import Test
from src.postgres import create_test_db, get_all_unique_names_test, get_test_info_by_name

# Создание роутера, который нужно будет присоединить к основному инстансу(объекту) приложения в модуле main.
router = APIRouter()


# Обработка HTTP запроса типа GET на роутер, по адресу "/".
@router.get("/", name="Ping API", description="Test pinging API", status_code=200)
async def ping_server() -> dict:
    """
    Метод пинга сервера - проверки работоспособности приложения.
    :return: Простой dict, с текстовыми данными.
    """
    return {
        "status_code": "200 OK"
    }


# Обработка HTTP запроса типа POST на роутер, по адресу "/create_test". В параметрах test_info типа валидации Test.
@router.post("/create_test", description="Creating test")
async def create_test(test_info: Test) -> bool:
    """
    Метод создания теста в бд, по заданным данным теста.

    :param test_info: Данные о тесте в виде типа валидации Test.

    :return: Булево значение - True/False в случае успешном создании/не успешном создании.
    """
    # Десять раз вызываем метод создание записи вопроса в БД.(в каждом тесте 10 вопросов)
    success_1 = await create_test_db(test_info.test_name, test_info.quest_1)
    success_2 = await create_test_db(test_info.test_name, test_info.quest_2)
    success_3 = await create_test_db(test_info.test_name, test_info.quest_3)
    success_4 = await create_test_db(test_info.test_name, test_info.quest_4)
    success_5 = await create_test_db(test_info.test_name, test_info.quest_5)
    success_6 = await create_test_db(test_info.test_name, test_info.quest_6)
    success_7 = await create_test_db(test_info.test_name, test_info.quest_7)
    success_8 = await create_test_db(test_info.test_name, test_info.quest_8)
    success_9 = await create_test_db(test_info.test_name, test_info.quest_9)
    success_10 = await create_test_db(test_info.test_name, test_info.quest_10)

    # В случае, если каждый запрос исполнился корректно и вернулось True - вернем True.
    if (success_1 and success_2 and success_3 and success_4 and success_5 and success_6 and success_7 and success_8 and
            success_9 and success_10):
        return True
    else:
        return False


# Обработка HTTP запроса типа GET на роутер, по адресу "/test_list". Возвращает список из уникальных названий тестов.
@router.get("/test_list", description="List of unique names test")
async def test_list() -> list:
    """
    Метод возвращает уникальные названия тестов, которые существуют в БД.

    :return: Список уникальных значений, если их нет - пустой список.
    """
    # Получаем список уникальных названий.
    all_names = await get_all_unique_names_test()

    # Если список не пустой, то вернем его.
    if all_names is not None:
        return all_names
    # Иначе вернем пустой список.
    else:
        return []


# Обработка HTTP запроса типа GET на роутер, по адресу "/test_info". Возвращает данные теста,
# по его названию(получаем из запроса)
@router.get("/test_info", description="Get info about test by name")
async def test_info_by_name(name: str) -> tuple | None:
    """
    Метод, который возвращает кортеж данных по тесту.

    :param name: Название теста, как в БД.

    :return: Возвращаем кортеж данных о тесте.
    """
    # Получаем данные из БД по имени.
    test_info = await get_test_info_by_name(name)

    # Если что-то вернулось, то возвращаем.
    if test_info:
        return test_info
    return None
