from pydantic import BaseModel


class QuestionResponse(BaseModel):
    question_id: int
    question_text: str

