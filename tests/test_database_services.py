from app.models import DailyEntry
from datetime import date
import app.services as services


def test_get_entries_by_date_range_returns_matching_entries(db_session):

    entry1 = DailyEntry(
        date=date(2026, 7, 13),
        mood=5,
        energy=5
    )
    entry2 = DailyEntry(
        date=date(2026, 7, 14),
        mood=6,
        energy=6
    )
    entry3 = DailyEntry(
        date=date(2026, 7, 15),
        mood=7,
        energy=7
    )

    db_session.add(entry1)
    db_session.add(entry2)
    db_session.add(entry3)
    db_session.commit()
    result = services.get_entries_by_date_range(
        db=db_session,
        start_date=date(2026, 7, 14),
        end_date=date(2026, 7, 15)
    )
    assert len(result) == 2
    assert result[0].energy == 7
    assert result[0].mood == 7
    assert result[0].date == date(2026, 7, 15)
    assert result[1].energy == 6
    assert result[1].mood == 6
    assert result[1].date == date(2026, 7, 14)
    result = services.get_entries_by_date_range(
        db=db_session,
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 25)
    )
    assert len(result) == 0
    