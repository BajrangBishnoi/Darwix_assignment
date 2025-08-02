from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.llm_operations.ai_insights import get_recommendations
from app.schema import *
from app.crud import CallService
from . import models
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/api/v1/calls", response_model=CallListResponse)
def list_calls(
    limit: int = 10,
    offset: int = 10,
    agent_id: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None,
    min_sentiment: Optional[float] = None,
    max_sentiment: Optional[float] = None,
    db: Session = Depends(get_db),
):
    calls = CallService(db).get_calls(
        limit=limit,
        offset=offset,
        agent_id=agent_id,
        from_date=from_date,
        to_date=to_date,
        min_sentiment=min_sentiment,
        max_sentiment=max_sentiment,
    )
    return {"calls": [CallBase.from_orm(call) for call in calls]}


@app.get("/api/v1/calls/{call_id}", response_model=CallDetail)
def get_call(call_id: str, db: Session = Depends(get_db)):
    call = CallService(db).get_call_by_id(call_id)
    if not call:
        raise HTTPException(status_code=404, detail="Call not found")
    return call


@app.get("/api/v1/calls/{call_id}/recommendations")
def recommendations(call_id: str, db: Session = Depends(get_db)):
    result = get_recommendations(call_id, db)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/api/v1/analytics/agents", response_model=List[AgentAnalytics])
def get_analytics(db: Session = Depends(get_db)):
    data = CallService(db).get_agent_analytics()
    return [
        AgentAnalytics(
            agent_id=row.agent_id,
            avg_sentiment=row.avg_sentiment,
            avg_talk_ratio=row.avg_talk_ratio,
            call_count=row.call_count,
        )
        for row in data
    ]
