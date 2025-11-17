from fastapi import FastAPI

from app.api.answer_handler import answer_router
from app.api.question_handler import question_router
from app.api.auth_handler import auth_router

app = FastAPI(
    openapi_url="/api/v1/hightalent/openapi.json",
    docs_url="/api/v1/hightalent/docs"
)

app.include_router(answer_router, prefix='/api/v1/answers', tags=['answers'])
app.include_router(question_router, prefix='/api/v1/questions', tags=['questions'])

app.include_router(auth_router, prefix='/api/v1/auth', tags=['auth'])
