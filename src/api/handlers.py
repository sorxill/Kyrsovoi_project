from fastapi import APIRouter

from src.api.models import Test
from src.postgres import create_test_db, get_all_unique_names_test

router = APIRouter()


@router.get("/", name="Ping API", description="Test pinging API", status_code=200)
async def ping_server() -> dict:
    return {
        "status_code": "200 OK"
    }


@router.post("/create_test", description="Creating test")
async def create_test(test_info: Test) -> bool:
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

    if (success_1 and success_2 and success_3 and success_4 and success_5 and success_6 and success_7 and success_8 and
            success_9 and success_10):
        return True
    else:
        return False


@router.get("/test_list", description="List of unique names test")
async def test_list() -> list:
    all_names = await get_all_unique_names_test()
    if all_names is not None:
        return all_names
    else:
        return []
