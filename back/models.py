from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    answers = relationship(
        "Answer",
        backref="question",
        cascade="all, delete, delete-orphan",
    )

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, unique=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    user_id = Column(String)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.now())

