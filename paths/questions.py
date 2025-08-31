from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from back.database import get_db
from back.models import Question
from typing import List

from back.schemas import QuestionAddRequest, QuestionResponse

router = APIRouter()

logger = logging.getLogger("question.error")
logger.setLevel(logging.DEBUG)

@router.get("/questions/", response_model=List[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    if db.query(Question).count() == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return db.query(Question).all()

@router.post("/questions/", response_model=QuestionResponse)
def add_question(question: QuestionAddRequest, db: Session = Depends(get_db)):
    if not question.text or not question.text.strip():
        logger.debug("Empty string")
        raise HTTPException(status_code=400, detail="Question text is required")
    db_add = Question(text=question.text)
    db.add(db_add)
    db.commit()
    db.refresh(db_add)
    return db_add

@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)) -> type[Question]:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        logger.debug(f"Question {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        logger.debug(f"Question {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted"}