from app.models import DailyEntry
import app.services as services 
from datetime import date


entry1 = DailyEntry(
    date=date(2026, 7, 9), 
    sleep_hours=4, 
    energy=5, 
    mood=4, 
    deep_work_minutes=20, 
    exercise_minutes=75, 
    stimulation_minutes=15, 
    litres_water=1.5, 
    no_porn=True, 
    no_smoking=True, 
    no_alcohol=True
    )

entry2 = DailyEntry(
    date=date(2026, 7, 10), 
    sleep_hours=1, 
    energy=10, 
    mood=2, 
    deep_work_minutes=30, 
    exercise_minutes=100, 
    stimulation_minutes=60, 
    litres_water=0.5, 
    no_porn=True, 
    no_smoking=True, 
    no_alcohol=True
    )

entry3 = DailyEntry(
    date=date(2026, 7, 11), 
    sleep_hours=3, 
    energy=5, 
    mood=1, 
    deep_work_minutes=40, 
    exercise_minutes=25, 
    stimulation_minutes=70, 
    litres_water=2.5, 
    no_porn=False, 
    no_smoking=True, 
    no_alcohol=True
    )

entries = [entry1, entry2, entry3]

blank_entry1 = DailyEntry(
    date=date(2026, 7, 12), 
    sleep_hours=None,
    energy=None,
    mood=None,
    deep_work_minutes=None,
    exercise_minutes=None,
    stimulation_minutes=None,
    litres_water=None,
    no_porn=True,
    no_smoking=False,
    no_alcohol=True
    )

blank_entry2 = DailyEntry(
    date=date(2026, 7, 13), 
    sleep_hours=2,
    energy=None,
    mood=None,
    deep_work_minutes=None,
    exercise_minutes=None,
    stimulation_minutes=25,
    litres_water=None,
    no_porn=True,
    no_smoking=False,
    no_alcohol=True
    )

entries_blank = [entry1, blank_entry1, blank_entry2]


def test_calculate_total_deep_work():
    result = services.calculate_total(entries,"deep_work_minutes")
    assert result == 90
    result = services.calculate_total_deep_work_minutes(entries)
    assert result == 90
    result = services.calculate_total_deep_work_minutes(entries_blank)
    assert result == 20


def test_calculate_total_exercise():
    result = services.calculate_total(entries,"exercise_minutes")
    assert result == 200
    result = services.calculate_total_exercise_minutes(entries)
    assert result == 200
    result = services.calculate_total_exercise_minutes(entries_blank)
    assert result == 75


def test_calculate_total_stimulation():
    result = services.calculate_total(entries,"stimulation_minutes")
    assert result == 145
    result = services.calculate_total_stimulation_minutes(entries)
    assert result == 145
    result = services.calculate_total_stimulation_minutes(entries_blank)
    assert result == 40


def test_calculate_average_deep_work():
    result = services.calculate_average(entries,"deep_work_minutes")
    assert result == 30
    result = services.calculate_average_deep_work_minutes(entries)
    assert result == 30
    result = services.calculate_average_deep_work_minutes(entries_blank)
    assert result == 20


def test_calculate_average_exercise():
    result = services.calculate_average(entries,"exercise_minutes")
    assert result == 66.67
    result = services.calculate_average_exercise_minutes(entries)
    assert result == 66.67
    result = services.calculate_average_exercise_minutes(entries_blank)
    assert result == 75


def test_calculate_average_stimulation():
    result = services.calculate_average(entries,"stimulation_minutes")
    assert result == 48.33
    result = services.calculate_average_stimulation_minutes(entries)
    assert result == 48.33
    result = services.calculate_average_stimulation_minutes(entries_blank)
    assert result == 20


def test_calculate_average_sleep_hours():
    result = services.calculate_average(entries,"sleep_hours")
    assert result == 2.67
    result = services.calculate_average_sleep_hours(entries)
    assert result == 2.67
    result = services.calculate_average_sleep_hours(entries_blank)
    assert result == 3


def test_calculate_average_mood():
    result = services.calculate_average(entries,"mood")
    assert result == 2.33
    result = services.calculate_average_mood(entries)
    assert result == 2.33
    result = services.calculate_average_mood(entries_blank)
    assert result == 4


def test_calculate_average_energy():
    result = services.calculate_average(entries,"energy")
    assert result == 6.67
    result = services.calculate_average_energy(entries)
    assert result == 6.67
    result = services.calculate_average_energy(entries_blank)
    assert result == 5


def test_calculate_average_litres_water():
    result = services.calculate_average(entries,"litres_water")
    assert result == 1.5
    result = services.calculate_average_litres_water(entries)
    assert result == 1.5
    result = services.calculate_average_litres_water(entries_blank)
    assert result == 1.5


def test_get_clean_days():
    result = services.get_clean_days(entries)
    assert result == 2
    result = services.get_clean_days(entries_blank)
    assert result == 1


def test_get_best_mood_day():
    result = services.get_best_mood_day(entries)
    assert result == date(2026, 7, 9)
    result = services.get_best_mood_day(entries_blank)
    assert result == date(2026, 7, 9)


def test_get_worst_mood_day():
    result = services.get_worst_mood_day(entries)
    assert result == date(2026, 7, 11)
    result = services.get_worst_mood_day(entries_blank)
    assert result == date(2026, 7, 9)


def test_edge_case_empty_list():
    result = services.calculate_total([], "deep_work_minutes")
    assert result == 0
    result = services.calculate_average([], "deep_work_minutes")
    assert result is None
    result = services.get_clean_days([])
    assert result == 0
    result = services.get_best_mood_day([])
    assert result is None
    result = services.get_worst_mood_day([])
    assert result is None


def test_build_analytics_summary():
    result=services.build_analytics_summary(entries, start_date=date(2026, 7, 9), end_date=date(2026, 7, 11))
    assert result["start_date"] == date(2026, 7, 9)
    assert result["end_date"] == date(2026, 7, 11)
    assert result["tracked_days"] == 3
    assert result["average_sleep_hours"] == 2.67
    assert result["average_mood"] == 2.33
    assert result["average_energy"] == 6.67
    assert result["average_stimulation_minutes"] == 48.33
    assert result["total_stimulation_minutes"] == 145
    assert result["total_deep_work_minutes"] == 90
    assert result["average_deep_work_minutes"] == 30
    assert result["total_exercise_minutes"] == 200
    assert result["average_exercise_minutes"] == 66.67
    assert result["average_litres_water"] == 1.5
    assert result["clean_days"] == 2
    assert result["best_mood_day"] == date(2026, 7, 9)
    assert result["worst_mood_day"] == date(2026, 7, 11)
   