from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.schemas.question_schemas import QuestionCreate, QuestionOut, QuestionUpdate, QuestionDetailOut
from app.services.question_service import QuestionService
from app.api.dependencies import questions_services

question_router = APIRouter()


@question_router.post('/create_question/')
async def create_question(question_in: QuestionCreate,
                          question_service: Annotated[QuestionService, Depends(questions_services)]):
    question_id = await question_service.add_question(question_in)
    return {'ok': True, 'created_id': question_id}


@question_router.get('/get_all_questions/', response_model=list[QuestionOut])
async def get_all_questions(question_service: Annotated[QuestionService, Depends(questions_services)]):
    return await question_service.find_questions()


@question_router.patch('/update_status/{question_id}')
async def update_question(question_id: int,
                                 question_in: QuestionUpdate,
                                 question_service: Annotated[QuestionService, Depends(questions_services)]):
    updated_id = await question_service.update_one_question(question_id, question_in)
    return {"ok": True, "updated_id": updated_id}


@question_router.get('/{question_id}', response_model=QuestionDetailOut)
async def get_question_by_id(question_id: int,
                             question_service: Annotated[QuestionService, Depends(questions_services)]):
    question = await question_service.find_one_question_with_answers(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@question_router.delete('/delete/{question_id}')
async def delete_question(question_id: int,
                          question_service: Annotated[QuestionService, Depends(questions_services)]):
    await question_service.delete_one_question(question_id)
    return {"ok": True, "question_id deleted": question_id}