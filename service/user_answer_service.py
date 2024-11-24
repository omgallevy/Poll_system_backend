from typing import Optional, List

from config.config import Config
from model.user_answer_request import UserAnswerRequest
from model.user_answer_response import UserAnswerResponse
from repository import user_answer_repository
import httpx

config = Config()


async def get_by_id(answer_id: int) -> Optional[UserAnswerResponse]:
    return await user_answer_repository.get_by_id(answer_id)


async def get_all() -> List[UserAnswerResponse]:
    return await user_answer_repository.get_all()


async def create_user_answer(answer: UserAnswerRequest) -> UserAnswerResponse:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.USER_SERVICE_BASE_URL}/{answer.user_id}")
        if response.status_code != 200:
            raise Exception("User not found in user service")

    answer_id = await user_answer_repository.create_user_answer(answer)
    return UserAnswerResponse(answer_id=answer_id, user_id=answer.user_id, question_id=answer.question_id,
                              chosen_option_id=answer.additional_id)


async def update_user_answer(answer_id: int, answer: UserAnswerRequest):
    await user_answer_repository.update_user_answer(answer_id, answer)


async def delete_all_user_answers(user_id: int):
    await user_answer_repository.delete_all_user_answers(user_id)


async def get_answers_by_user_id(user_id: int) -> Optional[UserAnswerResponse]:
    return await user_answer_repository.get_answers_by_user_id(user_id)
