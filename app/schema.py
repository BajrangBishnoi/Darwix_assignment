from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class CallBase(BaseModel):
    call_id: str
    agent_id: str
    customer_id: str
    transcript: str
    sentiment_score: float
    agent_talk_ratio: float
    start_time: datetime

    class Config:
        from_attributes = True


class CallDetail(CallBase):
    agent_id: str
    customer_id: str
    transcript: str
    sentiment_score: float
    agent_talk_ratio: float
    start_time: datetime


class CallListResponse(BaseModel):
    calls: List[CallBase]


class RecommendationsResponse(BaseModel):
    recommendations: List[CallBase]
    coaching_nudges: List[str]


class AgentAnalytics(BaseModel):
    agent_id: str
    avg_sentiment: float
    avg_talk_ratio: float
    call_count: int
