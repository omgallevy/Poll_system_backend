from pydantic import BaseModel


class UserAnswerResponse(BaseModel):
    answer_id: int
    user_id: int
    question_id: int
    chosen_option_id: int
