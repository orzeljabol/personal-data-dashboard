# Personal Data Dashboard (V1)

A small FastAPI + SQLite app to track daily metrics (sleep, mood, deep work, habits) and view simple weekly summaries.

## Tech
- Python
- FastAPI
- SQLite (SQLAlchemy)

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
