from typing import Optional, List

from model.options_request import OptionRequest
from model.options_response import OptionResponse
from model.poll_complete_request import PollCompleteRequest
from model.poll_complete_response import PollCompleteResponse
from model.question_response import QuestionResponse
from repository import options_repository, question_repository


async def get_by_id(option_id: int) -> Optional[OptionResponse]:
    return await options_repository.get_by_id(option_id)


async def get_all() -> List[OptionResponse]:
    return await options_repository.get_all()


async def get_options_by_question_id(question_id: int) -> List[OptionResponse]:
    return await options_repository.get_options_by_question_id(question_id)


async def create_option(option: OptionRequest) -> OptionResponse:
    option_id = await options_repository.create_option(option)
    return OptionResponse(option_id=option_id, question_id=option.question_id, option_text=option.option_text)


async def update_option(option_id: int, option: OptionResponse):
    await options_repository.update_option(option_id, option)


async def delete_option(option_id: int):
    await options_repository.delete_option(option_id)


async def create_poll(poll: PollCompleteRequest) -> PollCompleteResponse:
    question_id = await options_repository.create_poll(poll)
    question: Optional[QuestionResponse] = await question_repository.get_by_id(question_id)
    options = await options_repository.get_options_by_question_id(question_id)
    return PollCompleteResponse(
        poll_id=question_id,
        question=QuestionResponse(**dict(question)),
        options=options
    )

async def get_poll_by_id(poll_id: int) -> Optional[PollCompleteResponse]:
    return await options_repository.get_poll_by_id(poll_id)
