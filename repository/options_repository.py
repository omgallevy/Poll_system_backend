from typing import Optional, List

from fastapi import HTTPException

from model.options_request import OptionRequest
from model.options_response import OptionResponse
from model.poll_complete_request import PollCompleteRequest
from model.poll_complete_response import PollCompleteResponse
from model.question_response import QuestionResponse
from repository.database import database

TABLE_NAME_QUESTIONS = "questions"
TABLE_NAME_OPTIONS = "options"


async def get_by_id(option_id: int) -> Optional[OptionResponse]:
    query = f"SELECT * FROM {TABLE_NAME_OPTIONS} WHERE option_id = :option_id"
    result = await database.fetch_one(query, values={"option_id": option_id})
    if result:
        return OptionResponse(**result)
    return None


async def get_all() -> List[OptionResponse]:
    query = f"SELECT * FROM {TABLE_NAME_OPTIONS}"
    results = await database.fetch_all(query)
    return [OptionResponse(**result) for result in results]


async def get_options_by_question_id(question_id: int) -> List[OptionResponse]:
    query = f"SELECT * FROM {TABLE_NAME_OPTIONS} WHERE question_id = :question_id"
    results = await database.fetch_all(query, values={"question_id": question_id})
    return [OptionResponse(**result) for result in results] if results else []


async def create_option(option: OptionRequest) -> int:
    existing_options = await get_options_by_question_id(option.question_id)
    if len(existing_options) >= 4:
        raise Exception("Cannot add more than 4 options to a question")
    query = f""" 
        INSERT INTO {TABLE_NAME_OPTIONS} 
        (question_id, option_text) 
        VALUES 
        (:question_id, :option_text) 
    """
    values = {
        "question_id": option.question_id,
        "option_text": option.option_text
    }
    async with database.transaction():
        await database.execute(query, values=values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID()")
        return last_record_id[0]


async def update_option(option_id: int, option: OptionRequest):
    query = f""" 
        UPDATE {TABLE_NAME_OPTIONS} 
        SET question_id = :question_id, 
            option_text = :option_text 
        WHERE option_id = :option_id 
    """

    values = {
        "option_id": option_id,
        "question_id": option.question_id,
        "option_text": option.option_text
    }
    await database.execute(query, values=values)


async def delete_option(option_id: int):
    query = f"DELETE FROM {TABLE_NAME_OPTIONS} WHERE option_id = :option_id"
    await database.execute(query, values={"option_id": option_id})


async def create_poll(poll: PollCompleteRequest):
    query_question = f"""
        INSERT INTO {TABLE_NAME_QUESTIONS} (question_text)
        VALUES (:question_text)
    """
    values_question = {"question_text": poll.question.question_text}

    async with database.transaction():
        await database.execute(query=query_question, values=values_question)

        query_last_id = "SELECT LAST_INSERT_ID()"
        question_result = await database.fetch_one(query=query_last_id)
        if not question_result:
            raise HTTPException(status_code=400, detail="Failed to insert question")
        question_id = question_result['LAST_INSERT_ID()']

        query_option = f"""
            INSERT INTO {TABLE_NAME_OPTIONS} (question_id, option_text, additional_id)
            VALUES (:question_id, :option_text, :additional_id)
        """

        options_values = [
            {
                "question_id": question_id,
                "option_text": poll.options[i].option_text,
                "additional_id": i + 1
            }
            for i in range(len(poll.options))
        ]

        await database.execute_many(query=query_option, values=options_values)

        return question_id


async def get_poll_by_id(poll_id: int) -> Optional[PollCompleteResponse]:
    query_question = f"SELECT * FROM {TABLE_NAME_QUESTIONS} WHERE id = :poll_id"
    question_result = await database.fetch_one(query_question, values={"poll_id": poll_id})
    if not question_result:
        return None

    query_options = f"SELECT * FROM {TABLE_NAME_OPTIONS} WHERE question_id = :poll_id"
    options_results = await database.fetch_all(query_options, values={"poll_id": poll_id})
    options = [OptionResponse(**result) for result in options_results]
    return PollCompleteResponse(
        poll_id=poll_id,
        question=QuestionResponse(**question_result),
        options=options
    )
