from pydantic import BaseModel
from typing import List

from model.options_response import OptionResponse
from model.question_response import QuestionResponse


class PollCompleteResponse(BaseModel):
    poll_id: int
    question: QuestionResponse
    options: List[OptionResponse]
