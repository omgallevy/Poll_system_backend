from pydantic import BaseModel


class OptionResponse(BaseModel):
    option_id: int
    question_id: int
    option_text: str
    additional_id: int
