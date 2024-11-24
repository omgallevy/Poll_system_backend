from typing import Optional, List

from model.question_request import QuestionRequest
from model.question_response import QuestionResponse
from repository.database import database

TABLE_NAME = "questions"


async def get_by_id(question_id: int) -> Optional[QuestionResponse]:
    query = f"SELECT * FROM {TABLE_NAME} WHERE question_id = :question_id"
    result = await database.fetch_one(query, values={"question_id": question_id})
    if result:
        return QuestionResponse(**result)
    return None


async def get_all() -> List[QuestionResponse]:
    query = f"SELECT * FROM {TABLE_NAME}"
    results = await database.fetch_all(query)
    return [QuestionResponse(**result) for result in results]


async def create_question(question: QuestionRequest):
    query = f""" 
        INSERT INTO {TABLE_NAME} 
        (question_text) 
        VALUES 
        (:question_text) 
    """
    values = {
        "question_text": question.question_text
    }
    async with database.transaction():
        await database.execute(query, values=values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
    if last_record_id:
        return last_record_id[0]
    else:
        raise Exception("Failed to retrieve last insert ID.")


async def update_question(question_id: int, question: QuestionRequest):
    query = f"""
        UPDATE {TABLE_NAME}
        SET question_text = :question_text
        WHERE question_id = :question_id
    """
    values = {
        "question_id": question_id,
        "question_text": question.question_text
    }
    await database.execute(query, values=values)
    return await get_by_id(question_id)


async def delete_question(question_id: int):
    async with database.transaction():
        delete_options_query = f"DELETE FROM options WHERE question_id = :question_id"
        await database.execute(delete_options_query, values={"question_id": question_id})

        delete_question_query = f"DELETE FROM questions WHERE question_id = :question_id"
        await database.execute(delete_question_query, values={"question_id": question_id})
