from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal

class EventSchema(BaseModel):
    """Schema for event validation"""
    event_type: str = Field(
        ..., 
        description="Type of the event",
        examples=["message", "user_joined", "user_left"]
    )
    event_payload: str = Field(
        ..., 
        description="Payload of the event",
        min_length=1,
        max_length=1000
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_type": "message",
                    "event_payload": "hello"
                }
            ]
        }
    }
    
    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed_types = {"message", "user_joined", "user_left"}
        if not isinstance(v, str):
            raise ValueError(f"Event type must be a string (received {type(v).__name__})")
        if v not in allowed_types:
            raise ValueError(f"Invalid event type. Allowed types: {allowed_types}")
        return v

    @field_validator('event_payload')
    @classmethod
    def validate_payload(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError(f"Event payload must be a string (received {type(v).__name__})")
        if not v:
            raise ValueError("Event payload cannot be empty")
        if len(v) > 1000:
            raise ValueError(f"Event payload too long (max: 1000, received: {len(v)})")
        return v
    

class EventResponse(BaseModel):
    """Schema for event response"""
    message: str
    event_id: int
    created_at: datetime
    status: Literal["success", "error"] = "success"

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Event created successfully",
                "event_id": 1,
                "created_at": "2025-02-22T12:00:00Z",
                "status": "success"
            }
        }
    }