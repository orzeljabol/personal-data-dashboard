from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, DateTime, Integer,Float, String, func
from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class DailyEntry(Base):
    __tablename__ = "daily_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date,unique=True, nullable=False)

    sleep_hours: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    energy: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mood: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    deep_work_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    exercise_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stimulation_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    litres_water: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    no_porn: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=False, default=False)
    no_smoking: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=False, default=False)
    no_alcohol: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
