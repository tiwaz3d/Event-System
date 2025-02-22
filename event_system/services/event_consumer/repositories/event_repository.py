from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from typing import Dict, List
from ..models.event import Event

class EventRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, event_type: str, event_payload: str) -> Event:
        event = Event(event_type=event_type, event_payload=event_payload)
        self._session.add(event)
        await self._session.commit()
        await self._session.refresh(event)
        return event

    async def get_event_counts(self) -> Dict[str, int]:
        result = await self._session.execute(
            select(Event.event_type, func.count(Event.id))
            .group_by(Event.event_type)
        )
        return dict(result.all())

    async def get_recent_events(self, limit: int = 20) -> List[Event]:
        result = await self._session.execute(
            select(Event)
            .order_by(Event.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()