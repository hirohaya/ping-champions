"""Fixtures and test database setup for integration tests"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..', 'backend'))

# Module-level test database setup
_test_engine = None
_TestingSessionLocal = None


def create_test_db():
    """Create in-memory test database with StaticPool for thread-safe access"""
    global _test_engine, _TestingSessionLocal
    
    # Create in-memory engine with StaticPool to share connection across threads
    # This is necessary for pytest with async and multi-threaded requests
    _test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Import models to register them with Base before creating tables
    from models import Event, Player, Match, Tournament  # noqa: F401
    from database import Base
    
    # Create all tables
    Base.metadata.create_all(bind=_test_engine)
    
    # Create session factory
    _TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_test_engine
    )


@pytest.fixture(autouse=True, scope="function")
def setup_test_database_session():
    """Create new database for each test"""
    create_test_db()
    yield
    # Cleanup
    global _test_engine
    if _test_engine:
        _test_engine.dispose()


@pytest.fixture
def db_session():
    """Provide a test database session"""
    db = _TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def client():
    """Create a test client with database dependency overridden"""
    from main import app
    from routers import events, players, matches, ranking, tournament
    
    def override_get_db():
        """Override database dependency with test session"""
        db = _TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Override get_db in all routers
    app.dependency_overrides[events.get_db] = override_get_db
    app.dependency_overrides[players.get_db] = override_get_db
    app.dependency_overrides[matches.get_db] = override_get_db
    app.dependency_overrides[ranking.get_db] = override_get_db
    app.dependency_overrides[tournament.get_db] = override_get_db
    
    # Create and yield client
    test_client = TestClient(app)
    yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def event(db_session):
    """Create a test event"""
    from models import Event
    
    event = Event(
        name="Test Event",
        date="2025-01-15",
        time="18:00",
        active=True
    )
    db_session.add(event)
    db_session.commit()
    return event


@pytest.fixture
def players(db_session, event):
    """Create test players"""
    from models import Player
    
    players_list = []
    for i in range(1, 9):  # 8 players for various test scenarios
        player = Player(
            name=f"Player {i}",
            event_id=event.id,
            elo_rating=1600
        )
        db_session.add(player)
        players_list.append(player)
    db_session.commit()
    return players_list
