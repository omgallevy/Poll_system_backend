from typing import Optional

from pydantic import BaseModel


class Questions(BaseModel):
    question_id: Optional[int] = None
    question_text: str

