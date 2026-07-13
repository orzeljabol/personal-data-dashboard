from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, DailyEntry
from datetime import date
import app.services as services

TEST_DATABASE_URL = "sqlite:///test_database.db"

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def test_get_entries_by_date_range_returns_matching_entries():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    test_db = TestingSessionLocal()
    try:
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

        test_db.add(entry1)
        test_db.add(entry2)
        test_db.add(entry3)
        test_db.commit()
        result = services.get_entries_by_date_range(
            db=test_db,
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
            db=test_db,
            start_date=date(2026, 7, 20),
            end_date=date(2026, 7, 25)
        )
        assert len(result) == 0
    finally:
        test_db.close()
