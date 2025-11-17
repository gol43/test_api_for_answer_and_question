from pydantic import BaseModel, field_validator
from datetime import datetime


class QuestionCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст вопроса должен содержать хотя бы один символ")
        return v.strip()


class QuestionUpdate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст вопроса должен содержать хотя бы один символ")
        return v.strip()

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