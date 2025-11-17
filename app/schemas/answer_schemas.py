from pydantic import BaseModel, field_validator
from datetime import datetime


class AnswerCreate(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str) -> str:
        if not v or v.strip() == "":
            raise ValueError("Текст ответа должен содержать хотя бы один символ")
        return v.strip()

class AnswerOut(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

    class Config:
        from_attributes = True