import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from event_system.services.event_consumer.api.main import app, get_session
from event_system.services.event_consumer.models.event import Base
from test_config import TEST_DATABASE_URL

from fastapi.testclient import TestClient

@pytest.fixture
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(test_session) -> AsyncGenerator:
    async def override_get_session():
        yield test_session
        
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(transport=ASGITransport(app=app), 
                           base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_propagator_config():
    return {
        "EVENT_PROPAGATOR_TARGET_URL": "http://localhost:8000/event",
        "EVENT_PROPAGATOR_EVENTS_FILE": "events.json",
        "EVENT_PROPAGATOR_INTERVAL": 1
    }

@pytest.fixture
def mock_events_file(tmp_path):
    events_file = tmp_path / "events.json"
    events_file.write_text('[]')
    return str(events_file)