from pydantic import BaseModel
from typing import List, Optional

from model.options_request import OptionRequest
from model.question_request import QuestionRequest


class PollCompleteRequest(BaseModel):
    poll_id: Optional[int] =None
    question: QuestionRequest
    options: List[OptionRequest]
