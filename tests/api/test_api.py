import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_event(client: AsyncClient):
    response = await client.post("/event", json={"event_type": "message", "event_payload": "test message"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Event created successfully"
    assert "event_id" in data


@pytest.mark.asyncio
async def test_invalid_event_type(client: AsyncClient):
    response = await client.post("/event", json={"event_type": "invalid", "event_payload": "test message"})
    assert response.status_code == 422
    data = response.json()
    assert "Value error, Invalid event type. Allowed types:" in data["detail"][0]["msg"]


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime" in data


@pytest.mark.asyncio
async def test_metrics_data(client: AsyncClient):
    await client.post("/event", json={"event_type": "message", "event_payload": "test1"})
    await client.post("/event", json={"event_type": "message", "event_payload": "test2"})

    response = await client.get("/metrics/data")
    assert response.status_code == 200
    data = response.json()
    assert "event_counts" in data
    assert "recent_events" in data
    assert data["event_counts"]["message"] == 2


@pytest.mark.asyncio
async def test_metrics_empty_data(client: AsyncClient):
    """Test metrics endpoint with no data"""
    response = await client.get("/metrics/data")
    assert response.status_code == 200
    data = response.json()
    assert "event_counts" in data
    assert "recent_events" in data
    assert len(data["recent_events"]) == 0


@pytest.mark.asyncio
async def test_metrics_html_page(client: AsyncClient):
    """Test the metrics HTML page endpoint"""
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
