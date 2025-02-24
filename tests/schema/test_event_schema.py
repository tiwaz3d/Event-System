import pytest
from pydantic import ValidationError
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
    assert any(
        "Invalid event type" in err["msg"]
        for err in exc_info.value.errors()
    )

def test_empty_payload():
    event_data = {"event_type": "message", "event_payload": ""}
    with pytest.raises(ValidationError) as exc_info:
        EventSchema(**event_data)
    assert any(
        "String should have at least 1 character" in err["msg"]
        for err in exc_info.value.errors()
    )