from typing import Optional

from pydantic import BaseModel


class OptionRequest(BaseModel):
    question_id: Optional[int] = None
    option_text: str
