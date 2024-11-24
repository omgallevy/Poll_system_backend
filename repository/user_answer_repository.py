from typing import Optional, List

import httpx

from api.internalApi.model.user_response import UserResponse
from config.config import Config

from model.user_answer_request import UserAnswerRequest
from model.user_answer_response import UserAnswerResponse
from repository.database import database

TABLE_NAME_USER_ANSWERS = "user_answer"
TABLE_NAME_OPTIONS = "options"

config = Config()


async def validate_user(user_id: int) -> bool:
    url = f"{config.USER_SERVICE_BASE_URL}/{user_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            user_data = response.json()
            user = UserResponse(**user_data)
            return user.is_registered
        return False


async def get_by_id(answer_id: int) -> Optional[UserAnswerResponse]:
    query = f"SELECT * FROM {TABLE_NAME_USER_ANSWERS} WHERE answer_id = :answer_id"
    result = await database.fetch_one(query, values={"answer_id": answer_id})
    if result:
        return UserAnswerResponse(**result)
    return None


async def get_all() -> List[UserAnswerResponse]:
    query = f"SELECT * FROM {TABLE_NAME_USER_ANSWERS}"
    results = await database.fetch_all(query)
    return [UserAnswerResponse(**result) for result in results]


async def create_user_answer(answer: UserAnswerRequest) -> int:
    if not await validate_user(answer.user_id):
        raise Exception("User not found or not registered")

    query_get_option_id = f""" 
        SELECT option_id FROM {TABLE_NAME_OPTIONS} 
        WHERE question_id = :question_id AND additional_id = :additional_id 
    """
    option_result = await database.fetch_one(query=query_get_option_id, values={"question_id": answer.question_id,
                                                                                "additional_id": answer.additional_id})
    if not option_result:
        raise Exception("Option not found")

    option_id = option_result["option_id"]

    query_insert_answer = f""" 
        INSERT INTO {TABLE_NAME_USER_ANSWERS} (user_id, question_id, chosen_option_id) 
        VALUES (:user_id, :question_id, :chosen_option_id) 
    """
    values_answer = {
        "user_id": answer.user_id,
        "question_id": answer.question_id,
        "chosen_option_id": option_id
    }

    async with database.transaction():
        await database.execute(query=query_insert_answer, values=values_answer)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    return last_record_id[0]


async def update_user_answer(answer_id: int, answer: UserAnswerRequest):
    query = f"""
        UPDATE {TABLE_NAME_USER_ANSWERS}
        SET user_id = :user_id,
            question_id = :question_id,
            chosen_option_id = :chosen_option_id
        WHERE answer_id = :answer_id
    """
    values = {
        "answer_id": answer_id,
        "user_id": answer.user_id,
        "question_id": answer.question_id,
        "chosen_option_id": answer.additional_id
    }
    await database.execute(query, values=values)


async def delete_all_user_answers(user_id: int):
    query = f"DELETE FROM {TABLE_NAME_USER_ANSWERS} WHERE user_id = :user_id"
    await database.execute(query, values={"user_id": user_id})


async def get_answers_by_user_id(user_id: int) -> Optional[UserAnswerResponse]:
    query = f"SELECT * FROM {TABLE_NAME_USER_ANSWERS} WHERE user_id = :user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return UserAnswerResponse(**result)
    return None
