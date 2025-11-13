"""Fixtures and test database setup"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
    from models import Event, Player, Match  # noqa: F401
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
def client():
    """Create a test client with database dependency overridden"""
    from main import app
    from routers import events, players, matches, ranking
    
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
    
    # Create and yield client
    test_client = TestClient(app)
    yield test_client
    
    # Clear overrides after test
    app.dependency_overrides.clear()

