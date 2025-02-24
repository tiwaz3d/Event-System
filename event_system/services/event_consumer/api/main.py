import logging
import sys
import time
from pathlib import Path
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from shared.errors import EventSystemException
from shared.utils.logging import setup_logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from event_system.shared.config.settings import consumer_settings

from ..repositories.event_repository import EventRepository
from ..schemas.event import EventResponse, EventSchema


logger = setup_logging("consumer")

templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))
app = FastAPI(title="Event Consumer Service")


engine = create_async_engine(consumer_settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

start_time = time.time()
request_count = 0
data_processed = 0


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@app.post("/event", response_model=EventResponse)
async def create_event(event: EventSchema, session: AsyncSession = Depends(get_session)):
    try:
        repository = EventRepository(session)
        created_event = await repository.create(event_type=event.event_type, event_payload=event.event_payload)
        return EventResponse(
            message="Event created successfully", event_id=created_event.id, created_at=created_event.created_at
        )
    except ValidationError as e:
        raise EventSystemException(status_code=422, message="Validation error", details=e.errors())
    except Exception as e:
        raise EventSystemException(status_code=500, message="Failed to create event", details={"error": str(e)})


@app.get("/health")
async def health_check():
    uptime = time.time() - start_time
    return {
        "status": "healthy",
        "uptime": uptime,
    }


@app.get("/metrics", response_class=HTMLResponse)
async def metrics_page(request: Request):
    return templates.TemplateResponse("metrics.html", {"request": request})


@app.get("/metrics/data")
async def metrics_data(session: AsyncSession = Depends(get_session)):
    repository = EventRepository(session)

    event_counts = await repository.get_event_counts()
    recent_events = await repository.get_recent_events()

    recent_events_data = [
        {
            "event_type": event.event_type,
            "event_payload": event.event_payload,
            "created_at": event.created_at.isoformat(),
        }
        for event in recent_events
    ]

    return {"event_counts": event_counts, "recent_events": recent_events_data[::-1]}
