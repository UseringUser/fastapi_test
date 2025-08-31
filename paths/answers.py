from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
from back.database import get_db
from back.models import Answer, Question
from back.schemas import AnswerAddRequest, AnswerResponse
from uuid import uuid4
from datetime import datetime

router = APIRouter()

logger = logging.getLogger("answer.error")
logger.setLevel(logging.DEBUG)

@router.get("/answers/{answer_id}", response_model=AnswerResponse)
def get_answer(answer_id: int ,db: Session = Depends(get_db)):
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not db_answer:
        logger.debug(f"Answer {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    return db_answer

@router.post("/questions/{question_id}/answers", response_model=AnswerResponse)
def add_answer(question_id, answer: AnswerAddRequest, db: Session = Depends(get_db)):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        logger.debug(f"Question {question_id} not found")
        raise HTTPException(status_code=404, detail="Question not found")

    db_answer = db.query(Answer).filter(Answer.text == answer.text).first()
    if not answer.text or not answer.text.strip():
        logger.debug("Empty string")
        raise HTTPException(status_code=400, detail="Answer text is required")

    if db_answer:
        logger.debug("Answer matched")
        raise HTTPException(status_code=400, detail="Answer already exists")

    db_add = Answer(question_id = question_id, user_id = str(uuid4()), text=answer.text)
    db.add(db_add)
    db.commit()
    db.refresh(db_add)
    return db_add

@router.delete("/answers/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not db_answer:
        logger.debug(f"Answer {answer_id} not found")
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(db_answer)
    db.commit()
    return {"message": "Answer deleted"}

