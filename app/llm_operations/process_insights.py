import json
from sqlalchemy.orm import Session
from app.llm_operations.ai_insights import CallInsightsProcessor
from app.models import Call


class CallProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.insights = CallInsightsProcessor()

    def process_all(self):
        calls_to_process = (
            self.db.query(Call)
            .filter(
                Call.embedding == None,
                Call.sentiment_score == None,
                Call.agent_talk_ratio == None,
            )
            .all()
        )

        for call in calls_to_process:
            insights = self.insights.process_call(call)
            if insights:
                call.embedding = json.dumps(insights["embedding"])
                call.sentiment_score = insights["customer_sentiment"]
                call.agent_talk_ratio = insights["agent_talk_ratio"]

        self.db.commit()


def process_all_calls(db: Session):
    CallProcessor(db).process_all()
