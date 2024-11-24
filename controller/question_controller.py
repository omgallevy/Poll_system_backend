
from fastapi import APIRouter, HTTPException
from model.question_request import QuestionRequest

from service import question_service

router = APIRouter(
    prefix="/questions",
    tags=["questions"]
)


@router.get("/{question_id}")
async def get_question(question_id: int):
    question = await question_service.get_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail=f"Question with id: {question_id} not found")
    return question


@router.post("/")
async def create_question(question: QuestionRequest):
    try:
        return await question_service.create_question(question)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create question: {e}")


@router.put("/{question_id}")
async def update_question(question_id: int, question: QuestionRequest):
    existing_question = await question_service.get_by_id(question_id)
    if not existing_question:
        raise HTTPException(status_code=404, detail=f"Can't update question with id: {question_id}, question not found")
    try:
        updated_question = await question_service.update_question(question_id, question)
        return updated_question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update question: {e}")


@router.delete("/{question_id}")
async def delete_question(question_id: int):
    await question_service.delete_question(question_id)
    return {"message": "Question deleted successfully!"}


@router.get("/")
async def get_all_questions():
    return await question_service.get_all()
