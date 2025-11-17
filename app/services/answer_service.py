from fastapi import HTTPException

from app.repository.repository import SQLAlchemyRepository
from app.schemas.answer_schemas import AnswerCreate

class AnswerService:
    def __init__(self, model):
        self.answers_repository = SQLAlchemyRepository(model)
    
    async def find_one_answer(self, filter):
        obj = {}
        obj['filter_key'] = 'id'
        obj['filter_value'] = filter
        answer = await self.answers_repository.find_one(obj)
        if not answer:
            raise HTTPException(status_code=404, detail="Answer not found")
        return answer

    async def add_answer(self, answer: AnswerCreate, question_id: int, user_id: str) -> int:
        answer_dict = answer.model_dump()
        answer_dict["question_id"] = question_id
        answer_dict["user_id"] = user_id
        answer_id = await self.answers_repository.add_one(answer_dict)
        return answer_id
    
    async def delete_one_answer(self, answer_id: int):
        try:
            await self.answers_repository.delete_one(answer_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))