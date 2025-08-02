from datetime import datetime
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, load_only

from app.models import Call

# def get_calls(
#     db: Session,
#     skip: int = 0,
#     limit: int = 10,
#     offset: int = 0,
#     agent_id: Optional[str] = None,
#     from_date: Optional[datetime] = None,
#     to_date: Optional[datetime] = None,
#     min_sentiment: Optional[float] = None,
#     max_sentiment: Optional[float] = None,
# ):
#     query = db.query(Call)

#     if agent_id:
#         query = query.filter(Call.agent_id == agent_id)
#     if from_date:
#         query = query.filter(Call.call_date >= from_date)
#     if to_date:
#         query = query.filter(Call.call_date <= to_date)
#     if min_sentiment:
#         query = query.filter(Call.sentiment >= min_sentiment)
#     if max_sentiment:
#         query = query.filter(Call.sentiment <= max_sentiment)

#     return query.offset(offset).limit(limit).all()


# def get_call_by_id(db: Session, call_id: str):
#     return db.query(Call).filter(Call.call_id == call_id).first()


# def get_agent_analytics(db: Session):
#     return db.query(
#         Call.agent_id,
#         func.avg(Call.sentiment_score).label("avg_sentiment"),
#         func.avg(Call.agent_talk_ratio).label("avg_talk_ratio"),
#         func.count(Call.call_id).label("call_count")
#     ).group_by(Call.agent_id).all()




class CallService:
    def __init__(self, db: Session):
        self.db = db

    def get_calls(
        self,
        limit: int = 10,
        offset: int = 0,
        agent_id: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        min_sentiment: Optional[float] = None,
        max_sentiment: Optional[float] = None,
    ) -> List[Call]:
        query = self.db.query(Call).options(
            load_only(
                Call.call_id,
                Call.agent_id,
                Call.start_time,
                Call.transcript,
                Call.sentiment_score,
                Call.agent_talk_ratio,
            )
        )

        if agent_id:
            query = query.filter(Call.agent_id == agent_id)
        if from_date:
            query = query.filter(Call.start_time >= from_date)
        if to_date:
            query = query.filter(Call.start_time <= to_date)
        if min_sentiment:
            query = query.filter(Call.sentiment_score >= min_sentiment)
        if max_sentiment:
            query = query.filter(Call.sentiment_score <= max_sentiment)

        return query.offset(offset).limit(limit).all()

    def get_call_by_id(self, call_id: str) -> Optional[Call]:
        return self.db.get(Call, call_id)

    def get_agent_analytics(self):
        return (
            self.db.query(
                Call.agent_id,
                func.avg(Call.sentiment_score).label("avg_sentiment"),
                func.avg(Call.agent_talk_ratio).label("avg_talk_ratio"),
                func.count(Call.call_id).label("call_count"),
            )
            .group_by(Call.agent_id)
            .all()
        )
