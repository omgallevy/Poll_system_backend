from pydantic import BaseModel


class UserAnswerRequest(BaseModel):
    user_id: int
    question_id: int
    additional_id: int
