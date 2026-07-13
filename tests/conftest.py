from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

import pytest

TEST_DATABASE_URL = "sqlite:///test_database.db"

test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)



@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    test_db = TestingSessionLocal()
    try:
        yield test_db
    finally:
        test_db.close()
