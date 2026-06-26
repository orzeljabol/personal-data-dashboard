from fastapi import FastAPI, Depends, HTTPException
from app.db import engine, get_db
from app.models import Base, DailyEntry
from app.schemas import DailyEntryCreate, DailyEntryRead, DailyEntryEdit
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
import app.services as services

def get_last_7_days_entries(db: Session = Depends(get_db)):
    seven_days_ago = date.today() - timedelta(days=7)
    entries = db.query(DailyEntry).filter(DailyEntry.date >= seven_days_ago).order_by(DailyEntry.date.desc()).all()
    return entries
def calculate_average_sleep_hours(entries):
    total_sleep = 0
    days = 0
    for entry in entries:
        if entry.sleep_hours is not None:
            total_sleep += entry.sleep_hours
            days += 1
    if days > 0:
        average_sleep = total_sleep / days
    else:
        return 0
    return average_sleep
def calculate_average_mood(entries):
    total_mood = 0
    days = 0
    for entry in entries:
        if entry.mood is not None:
            total_mood += entry.mood
            days += 1
    if days > 0:
        average_mood = total_mood / days
    else:
        return 0
    return average_mood
def calculate_average_energy(entries):
    total_energy = 0
    days = 0
    for entry in entries:
        if entry.energy is not None:
            total_energy += entry.energy
            days += 1
    if days > 0:
        average_energy = total_energy / days
    else:
        return 0
    return average_energy
def calculate_total_deep_work_minutes(entries):
    total_deep_work = 0
    for entry in entries:
        if entry.deep_work_minutes is not None:
            total_deep_work += entry.deep_work_minutes
    return total_deep_work
def calculate_average_deep_work_minutes(entries):
    total_deep_work = 0
    days = 0
    for entry in entries:
        if entry.deep_work_minutes is not None:
            total_deep_work += entry.deep_work_minutes
            days += 1
    if days > 0:
        average_deep_work = total_deep_work / days
    else:
        return 0
    return average_deep_work
def calculate_average_exercise_minutes(entries):

    total_exercise = 0
    days = 0    
    for entry in entries:
        if entry.exercise_minutes is not None:
            total_exercise += entry.exercise_minutes
            days += 1
    if days > 0:
        average_exercise = total_exercise / days
    else:
        return 0
    return average_exercise
def calculate_total_exercise_minutes(entries):
    total_exercise = 0
    for entry in entries:
        if entry.exercise_minutes is not None:
            total_exercise += entry.exercise_minutes
    return total_exercise
def calculate_average_stimulation_minutes(entries):
    total_stimulation = 0
    days = 0
    for entry in entries:
        if entry.stimulation_minutes is not None:
            total_stimulation += entry.stimulation_minutes
            days += 1
    if days > 0:
        average_stimulation = total_stimulation / days
    else:
        return 0
    return average_stimulation
def calculate_total_stimulation_minutes(entries):
    total_stimulation = 0
    for entry in entries:
        if entry.stimulation_minutes is not None:
            total_stimulation += entry.stimulation_minutes
    return total_stimulation
def calculate_average_litres_water(entries):
    total_water = 0
    days = 0
    for entry in entries:
        if entry.litres_water is not None:
            total_water += entry.litres_water
            days += 1
    if days > 0:
        average_water = total_water / days
    else:
        return 0
    return average_water