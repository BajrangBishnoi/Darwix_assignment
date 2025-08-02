import json
from datetime import datetime
from app.database import SessionLocal
from app.models import Call


def load_calls_from_json(json_file):
    db = SessionLocal()
    with open(json_file, "r") as f:
        calls = json.load(f)

    for item in calls:
        call = Call(
            call_id=item["call_id"],
            agent_id=item["agent_id"],
            customer_id=item["customer_id"],
            language=item["language"],
            start_time=datetime.fromisoformat(item["start_time"]),
            duration_seconds=item["duration_seconds"],
            transcript=item["transcript"],
        )
        db.merge(call)  
    db.commit()
    db.close()
    print("Data loaded successfully.")


# Run script
if __name__ == "__main__":
    load_calls_from_json("call_transcripts1.json")
