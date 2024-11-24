from typing import Optional

import httpx

from api.internalApi.model.user_response import UserResponse
from config.config import Config

config = Config()


async def get_user_by_id(user_id: int) -> Optional[UserResponse]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{config.USER_SERVICE_BASE_URL}/user/{user_id}")
        if response.status_code == 200:
            return UserResponse(**response.json())
        else:
            return None

async def delete_answers_by_user_id(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{config.USER_SERVICE_BASE_URL}/user/{user_id}")
        if response.status_code != 200:
            response.raise_for_status()