from app.services.question_service import QuestionService
from app.services.answer_service import AnswerService
from app.database.models import Question, Answer


def questions_services():
    return QuestionService(Question)


def answers_services():
    return AnswerService(Answer)