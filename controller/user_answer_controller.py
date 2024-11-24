import httpx
from fastapi import APIRouter, HTTPException

from model.user_answer_request import UserAnswerRequest

from service import user_answer_service

router = APIRouter(
    prefix="/user_answers",
    tags=["user_answers"]
)


@router.get("/{answer_id}")
async def get_user_answer(answer_id: int):
    answer = await user_answer_service.get_by_id(answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail=f"User answer with id: {answer_id} not found")
    return answer


@router.post("/")
async def create_user_answer(answer: UserAnswerRequest):
    try:
        created_answer = await user_answer_service.create_user_answer(answer)
        return created_answer
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{answer_id}")
async def update_user_answer(answer_id: int, answer: UserAnswerRequest):
    existing_answer = await user_answer_service.get_by_id(answer_id)
    if not existing_answer:
        raise HTTPException(status_code=404, detail=f"Can't update user answer with id: {answer_id}, answer not found")
    await user_answer_service.update_user_answer(answer_id, answer)
    updated_answer = await user_answer_service.get_by_id(answer_id)
    return updated_answer


# @router.delete("/{answer_id}")
# async def delete_user_answer(answer_id: int):
#     await user_answer_service.delete_user_answer(answer_id)
#     return {"message": "User answer deleted successfully!"}


@router.delete("/user/{user_id}")
async def delete_all_user_answers(user_id: int):
    await user_answer_service.delete_all_user_answers(user_id)
    return {"message": f"All answers for user_id {user_id} have been deleted successfully."}


@router.get("/all")
async def get_all_user_answers():
    return await user_answer_service.get_all()


@router.get("/user/{user_id}")
async def get_user_answers(user_id: int):
    try:
        answers = await user_answer_service.get_answers_by_user_id(user_id)
        return answers
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching user answers: {e}")


