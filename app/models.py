import json
import uuid

from sqlalchemy import (Column, DateTime, Float, Integer, LargeBinary, String,
                        Text)

from app.database import Base


class Call(Base):
    __tablename__ = "calls"

    call_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, index=True)
    customer_id = Column(String)
    language = Column(String)
    start_time = Column(DateTime, index=True)
    duration_seconds = Column(Integer)
    transcript = Column(Text)
    embedding = Column(Text, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    agent_talk_ratio = Column(Float, nullable=True)
