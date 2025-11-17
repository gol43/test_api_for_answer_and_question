from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.schemas.answer_schemas import AnswerCreate, AnswerOut
from app.services.answer_service import AnswerService
from app.services.question_service import QuestionService
from app.api.dependencies import answers_services, questions_services

from app.api.auth_handler import get_current_auth_user
from app.schemas.auth_schemas import UserSchema

answer_router = APIRouter()


@answer_router.post('/create_answer/{question_id}')
async def create_answer(question_id: int,
                        answer_in: AnswerCreate,
                        answer_service: Annotated[AnswerService, Depends(answers_services)],
                        question_service: Annotated[QuestionService, Depends(questions_services)],
                        user: UserSchema = Depends(get_current_auth_user)):
    question = await question_service.find_one_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_id = await answer_service.add_answer(answer_in, question_id, user.uuid)
    return {'ok': True, 'created_id': answer_id}


@answer_router.get('/{answer_id}', response_model=AnswerOut)
async def get_answer_by_id(answer_id: int,
                           answer_service: Annotated[AnswerService, Depends(answers_services)]):
    answer = await answer_service.find_one_answer(answer_id)
    return answer


@answer_router.delete('/delete/{answer_id}')
async def delete_answer(answer_id: int,
                        answer_service: Annotated[AnswerService, Depends(answers_services)]):
    result = await answer_service.delete_one_answer(answer_id)
    return {"ok": True, "answer_id_deleted": answer_id}