import pytest
import httpx

from main import app
from httpx import AsyncClient, ASGITransport
from config import BASE_URL, BASE_WEBSOCKET_URI


transport = ASGITransport(app=app)
base_url = BASE_URL
websocket_uri = BASE_WEBSOCKET_URI


@pytest.mark.asyncio
async def test_create_order_success_1():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        response = await ac.post("/orders", json={"symbol": "AAPL", "quantity": 10, "price": 150.0})
        assert response.status_code == 200
        data = response.json()
        assert "order_id" in data
        assert data["order_id"] > 0


@pytest.mark.asyncio
async def test_get_orders_success():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        response = await ac.get("/orders")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)


@pytest.mark.asyncio
async def test_get_order_by_id_success():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        create_response = await ac.post("/orders", json={"symbol": "AAPL", "quantity": 10, "price": 150.0})
        order_id = create_response.json()["order_id"]

        response = await ac.get(f"/orders/{order_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["order"]["symbol"] == "AAPL"
        assert data["status"] == "PENDING" or data["status"] == "EXECUTED"


# Flaky
@pytest.mark.asyncio
async def test_delete_pending_order():
    # Step 1: Create a new order
    async with httpx.AsyncClient() as ac:
        response = await ac.post(f"{base_url}/orders", json={"symbol": "AAPL", "quantity": 10, "price": 150.0})
        assert response.status_code == 200
        order_id = response.json()["order_id"]

        # Step 2: Delete the order within the same context
        delete_response = await ac.delete(f"{base_url}/orders/{order_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Order canceled and deleted"

        # Step 3: Verify the order has been deleted
        get_response = await ac.get(f"{base_url}/orders/{order_id}")
        assert get_response.status_code == 404
        assert get_response.json() == {"detail": "Order not found"}
