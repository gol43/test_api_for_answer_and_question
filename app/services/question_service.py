from fastapi import HTTPException

from app.repository.repository import SQLAlchemyRepository
from app.schemas.question_schemas import QuestionCreate, QuestionUpdate
from app.database.models import Answer

class QuestionService:
    def __init__(self, model):
        self.questions_repository = SQLAlchemyRepository(model)
    
    async def find_questions(self):
        questions_all = await self.questions_repository.find_all()
        return questions_all
    
    async def find_one_question(self, filter):
        obj = {}
        obj['filter_key'] = 'id'
        obj['filter_value'] = filter
        question = await self.questions_repository.find_one(obj)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    
    async def add_question(self, question: QuestionCreate) -> int:
        question_dict = question.model_dump()
        question_id = await self.questions_repository.add_one(question_dict)
        return question_id

    async def update_one_question(self, question_id: int, question: QuestionUpdate) -> int:
        try:
            return await self.questions_repository.update_one(question_id, question.model_dump())
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    
    async def delete_one_question(self, question_id: int):
        try:
            await self.questions_repository.delete_one_cascade(question_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    async def find_one_question_with_answers(self, question_id: int):
        return await self.questions_repository.find_one_with_answers(question_id, Answer)