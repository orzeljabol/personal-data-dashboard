from datetime import date, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.models import DailyEntry


def get_entries_by_date_range(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    query = db.query(DailyEntry)

    if start_date:
        query = query.filter(DailyEntry.date >= start_date)

    if end_date:
        query = query.filter(DailyEntry.date <= end_date)

    return query.order_by(DailyEntry.date.desc()).all()


def get_last_7_days_entries(db: Session):
    seven_days_ago = date.today() - timedelta(days=7)

    return (
        db.query(DailyEntry)
        .filter(DailyEntry.date >= seven_days_ago)
        .order_by(DailyEntry.date.desc())
        .all()
    )


def get_values(entries, field_name):
    return [
        getattr(entry, field_name)
        for entry in entries
        if getattr(entry, field_name) is not None
    ]


def calculate_average(entries, field_name):
    values = get_values(entries, field_name)

    if not values:
        return None

    return round(sum(values) / len(values), 2)


def calculate_total(entries, field_name):
    values = get_values(entries, field_name)
    return sum(values)


def calculate_average_sleep_hours(entries):
    return calculate_average(entries, "sleep_hours")


def calculate_average_mood(entries):
    return calculate_average(entries, "mood")


def calculate_average_energy(entries):
    return calculate_average(entries, "energy")


def calculate_total_deep_work_minutes(entries):
    return calculate_total(entries, "deep_work_minutes")


def calculate_average_deep_work_minutes(entries):
    return calculate_average(entries, "deep_work_minutes")


def calculate_total_exercise_minutes(entries):
    return calculate_total(entries, "exercise_minutes")


def calculate_average_exercise_minutes(entries):
    return calculate_average(entries, "exercise_minutes")


def calculate_total_stimulation_minutes(entries):
    return calculate_total(entries, "stimulation_minutes")


def calculate_average_stimulation_minutes(entries):
    return calculate_average(entries, "stimulation_minutes")


def calculate_average_litres_water(entries):
    return calculate_average(entries, "litres_water")


def get_best_mood_day(entries):
    entries_with_mood = [
        entry for entry in entries
        if entry.mood is not None
    ]

    if not entries_with_mood:
        return None

    best_entry = max(entries_with_mood, key=lambda entry: entry.mood)
    return best_entry.date


def get_worst_mood_day(entries):
    entries_with_mood = [
        entry for entry in entries
        if entry.mood is not None
    ]

    if not entries_with_mood:
        return None

    worst_entry = min(entries_with_mood, key=lambda entry: entry.mood)
    return worst_entry.date


def build_analytics_summary(entries, start_date=None, end_date=None):
    return {
        "start_date": start_date,
        "end_date": end_date,

        "tracked_days": len(entries),

        "average_sleep_hours": calculate_average_sleep_hours(entries),
        "average_mood": calculate_average_mood(entries),
        "average_energy": calculate_average_energy(entries),

        "total_deep_work_minutes": calculate_total_deep_work_minutes(entries),
        "average_deep_work_minutes": calculate_average_deep_work_minutes(entries),

        "total_exercise_minutes": calculate_total_exercise_minutes(entries),
        "average_exercise_minutes": calculate_average_exercise_minutes(entries),

        "total_stimulation_minutes": calculate_total_stimulation_minutes(entries),
        "average_stimulation_minutes": calculate_average_stimulation_minutes(entries),

        "average_litres_water": calculate_average_litres_water(entries),

        "best_mood_day": get_best_mood_day(entries),
        "worst_mood_day": get_worst_mood_day(entries),
    }