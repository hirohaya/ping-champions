"""Fixtures and test database setup"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import models to register them with Base
from models import Event, Player, Match  # noqa: F401
from database import Base
from main import app
from routers import events, players, matches, ranking


@pytest.fixture
def db_session():
    """Create a new in-memory database session for each test"""
    # Create in-memory engine with check_same_thread disabled
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Cleanup
    session.rollback()
    session.close()
    engine.dispose()


@pytest.fixture
def client(db_session):
    """Create a test client with overridden database dependency"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override get_db in all routers
    app.dependency_overrides[events.get_db] = override_get_db
    app.dependency_overrides[players.get_db] = override_get_db
    app.dependency_overrides[matches.get_db] = override_get_db
    app.dependency_overrides[ranking.get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

