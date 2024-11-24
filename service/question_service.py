from typing import Optional, List

from model.question_request import QuestionRequest
from model.question_response import QuestionResponse
from repository import question_repository


async def get_by_id(question_id: int) -> Optional[QuestionResponse]:
    return await question_repository.get_by_id(question_id)


async def get_all() -> List[QuestionResponse]:
    return await question_repository.get_all()


async def create_question(question: QuestionRequest) -> QuestionResponse:
    return await question_repository.create_question(question)


async def update_question(question_id: int, question: QuestionRequest) -> QuestionResponse:
    existing_question = await question_repository.get_by_id(question_id)
    if existing_question is not None:
        return await question_repository.update_question(question_id, question)
    else:
        raise Exception(f"Can't update question with id {question_id}, id is not existing")


async def delete_question(question_id: int):
    await question_repository.delete_question(question_id)
