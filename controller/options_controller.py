from fastapi import APIRouter, HTTPException
from typing import List
from model.options_request import OptionRequest
from model.options_response import OptionResponse
from model.poll_complete_request import PollCompleteRequest
from model.poll_complete_response import PollCompleteResponse
from service import options_service

router = APIRouter(
    prefix="/options",
    tags=["options"]
)


@router.get("/{option_id}")
async def get_option(option_id: int):
    option = await options_service.get_by_id(option_id)
    if not option:
        raise HTTPException(status_code=404, detail=f"Option with id: {option_id} not found")
    return option


@router.post("/")
async def create_option(option: OptionRequest):
    try:
        created_option = await options_service.create_option(option)
        return created_option
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{option_id}")
async def update_option(option_id: int, option: OptionRequest):
    existing_option = await options_service.get_by_id(option_id)
    if not existing_option:
        raise HTTPException(status_code=404, detail=f"Can't update option with id: {option_id}, option not found")
    await options_service.update_option(option_id, option)
    updated_option = await options_service.get_by_id(option_id)
    return updated_option


@router.delete("/{option_id}")
async def delete_option(option_id: int):
    await options_service.delete_option(option_id)
    return {"message": "Option deleted successfully!"}


@router.get("/all", response_model=List[OptionResponse])
async def get_all_options():
    return await options_service.get_all()


@router.post("/create_poll", response_model=PollCompleteResponse)
async def create_poll(poll: PollCompleteRequest):
    try:
        created_poll = await options_service.create_poll(poll)
        return created_poll
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create poll: {e}")


@router.get("/poll/{poll_id}", response_model=PollCompleteResponse)
async def get_poll(poll_id: int):
    poll = await options_service.get_poll_by_id(poll_id)
    if not poll:
        raise HTTPException(status_code=404, detail=f"Poll with id: {poll_id} not found")
    return poll
