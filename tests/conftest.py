# tests/conftest.py
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db
from app.db.models import User

# -----------------------------
# TEST DATABASE (SQLite ONLY)
# -----------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# -----------------------------
# CREATE TABLES ONCE
# -----------------------------
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# -----------------------------
# DB SESSION FIXTURE
# -----------------------------
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

# -----------------------------
# OVERRIDE FASTAPI DB DEPENDENCY
# -----------------------------
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# -----------------------------
# USER FIXTURE (FK SAFE)
# -----------------------------
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
