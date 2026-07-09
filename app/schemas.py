from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class DailyEntryBase(BaseModel):
    date:date
    sleep_hours: Optional[float] = Field(default=None, ge=0, le=14)
    energy: Optional[int] = Field(default=None, ge=1, le=10)
    mood: Optional[int] = Field(default=None, ge=1, le=10)
    deep_work_minutes: Optional[int] = Field(default=None, ge=0, le=600)
    exercise_minutes: Optional[int] = Field(default=None, ge=0, le=300)
    stimulation_minutes: Optional[int] = Field(default=None, ge=0, le=600)
    litres_water: Optional[float] = Field(default=None, ge=0, le=10)
    notes: Optional[str] = Field(default=None, max_length=500)
    no_porn: Optional[bool] = None
    no_smoking: Optional[bool] = None
    no_alcohol: Optional[bool] = None
class DailyEntryEdit(BaseModel):
    sleep_hours: Optional[float] = Field(default=None, ge=0, le=14)
    energy: Optional[int] = Field(default=None, ge=1, le=10)
    mood: Optional[int] = Field(default=None, ge=1, le=10)
    deep_work_minutes: Optional[int] = Field(default=None, ge=0, le=600)
    exercise_minutes: Optional[int] = Field(default=None, ge=0, le=300)
    stimulation_minutes: Optional[int] = Field(default=None, ge=0, le=600)
    litres_water: Optional[float] = Field(default=None, ge=0, le=10)
    notes: Optional[str] = Field(default=None, max_length=500)
    no_porn: Optional[bool] = None
    no_smoking: Optional[bool] = None
    no_alcohol: Optional[bool] = None
class DailyEntryCreate(DailyEntryBase):
    pass
class DailyEntryRead(DailyEntryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
class Summary7Days(BaseModel):
    average_sleep_hours: Optional[float]
    average_mood: Optional[float]
    average_energy: Optional[float]

    total_deep_work_minutes: int
    average_deep_work_minutes: Optional[float]

    total_exercise_minutes: int
    average_exercise_minutes: Optional[float]

    total_stimulation_minutes: int
    average_stimulation_minutes: Optional[float]

    average_litres_water: Optional[float]
class AnalyticsSummary(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    tracked_days: int = 0

    average_sleep_hours: Optional[float] = None
    average_mood: Optional[float] = None
    average_energy: Optional[float] = None

    total_deep_work_minutes: int = 0
    average_deep_work_minutes: Optional[float] = None

    total_exercise_minutes: int = 0
    average_exercise_minutes: Optional[float] = None

    total_stimulation_minutes: int = 0
    average_stimulation_minutes: Optional[float] = None

    average_litres_water: Optional[float] = None
    clean_days: int = 0
    
    best_mood_day: Optional[date] = None
    worst_mood_day: Optional[date] = None