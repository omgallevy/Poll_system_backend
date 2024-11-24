from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question_text: str
