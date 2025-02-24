import asyncio
import json
import logging
import random
import sys
from typing import Any, Dict, List

import httpx
from shared.utils.logging import setup_logging

from ...shared.config.settings import PropagatorSettings

logger = setup_logging("propagator")


class EventPropagator:
    def __init__(self, settings: PropagatorSettings):
        self.interval = settings.interval
        self.target_url = settings.target_url
        self.events_file = settings.events_file
        self.events: List[Dict[str, Any]] = []
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(10.0), limits=httpx.Limits(max_keepalive_connections=5))

    async def __aenter__(self):
        await self.load_events()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def load_events(self):
        try:
            with open(self.events_file, "r") as f:
                self.events = json.load(f)
            logger.info(f"Loaded {len(self.events)} events from {self.events_file}")
        except Exception as e:
            logger.error(f"Failed to load events: {e}")
            raise

    async def send_event(self, event: Dict[str, Any]):
        try:
            response = await self.client.post(self.target_url, json=event)
            response.raise_for_status()
            logger.info(f"Successfully sent event: {event}")
        except Exception as e:
            logger.error(f"Failed to send event: {e}")
            raise

    async def run(self):
        while True:
            try:
                event = random.choice(self.events)
                await self.send_event(event)
                await asyncio.sleep(self.interval)
            except Exception as e:
                logger.error(f"Error in event propagation: {e}")
                await asyncio.sleep(self.interval)


async def main():
    settings = PropagatorSettings()
    async with EventPropagator(settings) as propagator:
        await propagator.run()


if __name__ == "__main__":
    asyncio.run(main())
