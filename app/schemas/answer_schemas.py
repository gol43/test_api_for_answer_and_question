from pydantic import BaseModel
from datetime import datetime


class AnswerCreate(BaseModel):
    text: str
    

class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True