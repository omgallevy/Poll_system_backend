from fastapi import FastAPI
from controller.question_controller import router as question_router
from controller.options_controller import router as options_router
from controller.user_answer_controller import router as user_answers_router
from  controller.company_controller import router as company_router
from repository.database import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(question_router)
app.include_router(options_router)
app.include_router(user_answers_router)
app.include_router(company_router)

