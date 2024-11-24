from pydantic import BaseModel
from datetime import date
from typing import Optional


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: int
    address: str
    joining_date: Optional[date]
    is_registered: bool
