from uuid import uuid4
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uuid: Mapped[str] = mapped_column(
        String, 
        unique=True, 
        index=True, 
        nullable=False,
        default=lambda: str(uuid4())
    )
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)

    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="user", cascade="all, delete-orphan")
    
class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="question", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.uuid", ondelete="CASCADE"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    user: Mapped["User"] = relationship("User", back_populates="answers")
