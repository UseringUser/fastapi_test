from datetime import date, datetime

from pydantic import BaseModel
from typing import List

class AnswerAddRequest(BaseModel):
    text: str

class AnswerResponse(BaseModel):
    id: int
    question_id: int
    text: str
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

class QuestionAddRequest(BaseModel):
    text: str

class QuestionResponse(BaseModel):
    id: int
    text: str
    created_at: datetime

    class Config:
        orm_mode = True