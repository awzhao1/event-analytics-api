# tests/conftest.py
import uuid
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.models import User
from app.api.events import get_db


# TEST DATABASE (SQLite — Docker safe)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:////tmp/test.db",  # ✅ writable in Docker
)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
    if TEST_DATABASE_URL.startswith("sqlite")
    else {},
)

# ENABLE SQLITE FOREIGN KEYS
if TEST_DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# CREATE TABLES ONCE

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# DB SESSION FIXTURE (ROLLBACK PER TEST)

@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# OVERRIDE FASTAPI DB DEPENDENCY

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# USER FIXTURE

@pytest.fixture(scope="function")
def test_user(db):
    user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        api_key="test_api_key_123",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
