from app.database import SessionLocal
from app.llm_operations.process_insights import process_all_calls

print("entered")

db = SessionLocal()
print("going good")
process_all_calls(db)
print("okey so far")
db.close()
