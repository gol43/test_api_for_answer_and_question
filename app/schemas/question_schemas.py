from pydantic import BaseModel
from datetime import datetime


class QuestionCreate(BaseModel):
    text: str


class QuestionUpdate(BaseModel):
    text: str


class QuestionOut(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class AnswerInQuestion(BaseModel):
    id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionDetailOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    answers: list[AnswerInQuestion] = []

    class Config:
        from_attributes = True