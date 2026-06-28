from fastapi import FastAPI, Depends, HTTPException
from app.db import engine, get_db
from app.models import Base, DailyEntry
from app.schemas import DailyEntryCreate, DailyEntryRead, DailyEntryEdit, Summary7Days
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import app.services as services
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="Personal Data Dashboard (V1)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"status": "Personal Data Dashboard API is running"}
@app.post("/api/entries/", response_model=DailyEntryRead, status_code=201)
def create_entry(payload: DailyEntryCreate, db: Session = Depends(get_db)):
    existing_entry = db.query(DailyEntry).filter(DailyEntry.date == payload.date).first()
    if existing_entry:
        raise HTTPException(status_code=400, detail="Entry for this date already exists")
    new_entry = DailyEntry(**payload.model_dump())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry
@app.get("/api/entries", response_model=list[DailyEntryRead])            
def get_entries(
    start_date: Optional[date] = None, 
    end_date: Optional[date] = None, 
    db: Session = Depends(get_db)):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date")
    query = db.query(DailyEntry)
    if start_date:
        query = query.filter(DailyEntry.date >= start_date)
    if end_date:
        query = query.filter(DailyEntry.date <= end_date)
    entries = query.order_by(DailyEntry.date.desc()).all()
    return entries
@app.get("/api/entries/{entry_id}", response_model=DailyEntryRead)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry
@app.patch("/api/entries/{entry_id}", response_model=DailyEntryRead, status_code=200)
def update_entry(entry_id: int, payload: DailyEntryEdit, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry
@app.delete("/api/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return 
@app.get("/api/entries/date/{entry_date}", response_model=DailyEntryRead)
def get_entry_by_date(entry_date: date, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.date == entry_date).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry
@app.patch("/api/entries/date/{entry_date}", response_model=DailyEntryRead, status_code=200)
def update_entry_by_date(entry_date: date, payload: DailyEntryEdit, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.date == entry_date).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry
@app.delete("/api/entries/date/{entry_date}", status_code=204)
def delete_entry_by_date(entry_date: date, db: Session = Depends(get_db)):
    entry = db.query(DailyEntry).filter(DailyEntry.date == entry_date).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return 
@app.get("/api/entries/summary/7days", response_model=Summary7Days)
def get_last_7_days_summary(db: Session = Depends(get_db)):

    entries = services.get_last_7_days_entries(db)
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found for the last 7 days")

    return Summary7Days(
        average_sleep_hours=services.calculate_average_sleep_hours(entries),
        average_mood=services.calculate_average_mood(entries),
        average_energy=services.calculate_average_energy(entries),
        total_deep_work_minutes=services.calculate_total_deep_work_minutes(entries),
        average_deep_work_minutes=services.calculate_average_deep_work_minutes(entries),
        total_exercise_minutes=services.calculate_total_exercise_minutes(entries),
        average_exercise_minutes=services.calculate_average_exercise_minutes(entries),
        total_stimulation_minutes=services.calculate_total_stimulation_minutes(entries),
        average_stimulation_minutes=services.calculate_average_stimulation_minutes(entries),
        average_litres_water=services.calculate_average_litres_water(entries),
    )
