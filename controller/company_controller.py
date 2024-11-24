from fastapi import APIRouter, HTTPException
from service import company_service


router = APIRouter(
    prefix="/company",
    tags=["company"]
)


@router.get("/option_counts/{question_id}")
async def get_option_counts_by_question(question_id: int):
    try:
        counts = await company_service.get_option_counts_by_question(question_id)
        return counts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/total_answers/{question_id}")
async def get_total_answers(question_id: int):
    try:
        result = await company_service.get_total_answers(question_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/user_answers/{user_id}")
async def get_user_answers(user_id: int):
    try:
        answers = await company_service.get_user_answers(user_id)
        return answers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/questions_answers/{user_id}")
async def get_total_questions_answers_by_user(user_id: int):
    try:
        result = await company_service.get_total_questions_answers_by_user(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
