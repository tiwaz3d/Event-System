from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
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

    async def get_all(self) -> List[Event]:
        result = await self._session.execute(select(Event))
        return result.scalars().all()

    async def get_by_type(self, event_type: str) -> List[Event]:
        result = await self._session.execute(
            select(Event).where(Event.event_type == event_type)
        )
        return result.scalars().all()