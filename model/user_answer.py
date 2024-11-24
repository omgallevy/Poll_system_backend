from typing import Optional

from pydantic import BaseModel


class UserAnswer(BaseModel):
    answer_id: Optional[int] = None
    user_id: int
    question_id: int
    chosen_option_id: int
