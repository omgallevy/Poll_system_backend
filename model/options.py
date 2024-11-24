from typing import Optional

from pydantic import BaseModel


class Options(BaseModel):
    option_id: Optional[int] = None
    question_id: int
    option_text: str

