import pytest
from pydantic import ValidationError
from services.event_consumer.repositories.event_repository import EventRepository

from event_system.services.event_consumer.schemas.event import EventSchema


def test_valid_event_schema():
    event_data = {"event_type": "message", "event_payload": "hello"}
    event = EventSchema(**event_data)
    assert event.event_type == "message"
    assert event.event_payload == "hello"


def test_invalid_event_type():
    event_data = {"event_type": "invalid_type", "event_payload": "hello"}
    with pytest.raises(ValidationError) as exc_info:
        EventSchema(**event_data)
    assert "Invalid event type" in str(exc_info.value)


def test_empty_payload():
    event_data = {"event_type": "message", "event_payload": ""}
    with pytest.raises(ValidationError) as exc_info:
        EventSchema(**event_data)
    assert any("String should have at least 1 character" in err["msg"] for err in exc_info.value.errors())


@pytest.mark.asyncio
async def test_get_event_counts_empty(test_session):
    """Test get_event_counts with no events"""
    repository = EventRepository(test_session)
    counts = await repository.get_event_counts()
    assert counts == {}


@pytest.mark.asyncio
async def test_get_recent_events_empty(test_session):
    """Test get_recent_events with no events"""
    repository = EventRepository(test_session)
    events = await repository.get_recent_events()
    assert len(events) == 0


@pytest.mark.asyncio
async def test_get_recent_events_limit(test_session):
    """Test get_recent_events with limit"""
    repository = EventRepository(test_session)
    for i in range(5):
        await repository.create("message", f"test{i}")
    events = await repository.get_recent_events(limit=3)
    assert len(events) == 3
