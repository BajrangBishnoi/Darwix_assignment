# Darwix Ingestion & Query API

This project is a modular Python application designed to process call transcripts and analyze them by leveraging Large Language Models (LLMs) for generating meaningful insights. It integrates transformer-based embedding models, sentiment analysis, and stores results efficiently in a structured SQL database using SQLAlchemy and Alembic for migrations. 

---

##  Repository Contents

- `ingest.py`: Script to ingest data into the database.
- `api/`: Django app that contains models, serializers, views, and routing for querying data.
- `llm_operations`: This module is responsible for running the LLM-powered processing pipeline — from extracting insights to generating embeddings and sentiment scores. 
It is designed to integrates seamlessly with the overall FastAPI-based backend.
- `Dockerfile`, `docker-compose.yml`, `.dockerignore`: Docker assets for containerization.
- `requirements.txt`: Python dependencies.
- `README.md`: Project setup, usage, and notes (you are here).

---
##  Project Structure
```bash
darwix_assignment/
│
├── app/
     ├── llm_operations/
            ├── run_processing.py/
            ├── ai_insights.py
            ├── process_insights.py
│ ├── init.py
│ ├── main.py # FastAPI app and route setup
│ ├── ingest.py # Ingestion function to populate database
│ ├── database.py # DB models and session logic
│ ├── crud.py # CRUD operations for DB
│ ├── schema.py
│
├── tests/
      ├── test_main.py
      ├── test_service.py
├── venv/ 
├── .env 
├── Dockerfile # Docker build file
├── docker-compose.yml # Multi-container setup
├── requirements.txt # Project dependencies
├── README.md
```


---

##  Features

-  FastAPI backend with async route handling
-  SQLite-based item description storage
-  Dockerized for easy deployment
-  Modular structure: `CRUD`, `DB`, and ingestion split clearly
-  Clean JSON responses

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/darwix-api.git
cd darwix_assignment
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  #on linux
venv\Scripts\activate  # On Windows:
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a .env file at the root:
```bash
DATABASE_URL=sqlite:///./calls.db   #or postgresql configurations
```

### Database Migrations (Alembic)
 Initial Setup (one-time)
 ```bash
alembic init alembic
```
Update the alembic.ini file and alembic/env.py with the correct SQLAlchemy database URL and model import path. 

Auto-generate a new migration after model changes:
```bash
alembic revision --autogenerate -m "Add new model or modify schema"
alembic upgrade head
```

### Dockerized Setup
1. Build and Run with Docker Compose
```bash
docker-compose up --build
```

To run on local setup for testing, open the terminal and move to directory of this project and run:
```bash
uvicorn app.main:app --reload 
```
### Ingestion Script
Data ingestion is handled via app/ingest.py. This script reads and inserts item descriptions into the database. It is not exposed via API endpoint.
```bash
python app/ingest.py
```
This will populate the database with predefined item descriptions.

### API Endpoints
Once the app is running, visit:
```bash
http://localhost:8000/docs
```
Fetch all calls
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/calls?limit=10&offset=10' \
  -H 'accept: application/json'
```
Fetch call by ID
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/calls/533a7bc7-66d9-427d-89ef-5d947772ea5f' \
  -H 'accept: application/json'
```
Fetch call by ID and recommendations
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/calls/533a7bc7-66d9-427d-89ef-5d947772ea5f/recommendations' \
  -H 'accept: application/json'
```
Fetch agent analysis
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/analytics/agents' \
  -H 'accept: application/json' 
```

### LLM Operations (app/llm_operations/)

### Execution Entry Point
Run the following command from the root directory to trigger the entire LLM pipeline:

```bash
python app/llm_operations/run_processing.py
```

### Design Notes
Tech Stack: FastAPI for speed and type safety; SQLite for lightweight persistence.

Indexing: indexing on agent_id and start_time using SQLAlchemy ORM.

Error Handling: Exception handling with FastAPI's HTTPException, returning meaningful status codes and also FastAPI includes automatic validation with Pydantic

Can swap SQLite with PostgreSQL for production.

Uvicorn workers (via Gunicorn) can handle concurrency.

Containerization	Docker	Enables reproducible, isolated dev environment
