import pytest
import asyncio
import httpx

from config import BASE_URL, BASE_WEBSOCKET_URI


base_url = BASE_URL
websocket_uri = BASE_WEBSOCKET_URI


@pytest.mark.asyncio
async def test_order_status_flow():
    async with httpx.AsyncClient() as ac:
        # Step 1: Create a new order
        response = await ac.post(f"{base_url}/orders", json={"symbol": "AAPL", "quantity": 10, "price": 150.0})
        assert response.status_code == 200
        order_id = response.json()["order_id"]

        # Step 2: Check initial status
        order_response = await ac.get(f"{base_url}/orders/{order_id}")
        assert order_response.status_code == 200
        assert order_response.json()["status"] == "PENDING"

        # Step 3: Wait for the status to be updated
        await asyncio.sleep(2)  # Give enough time for status to change to EXECUTED

        # Step 4: Check updated status
        updated_order_response = await ac.get(f"{base_url}/orders/{order_id}")
        assert updated_order_response.status_code == 200
        assert updated_order_response.json()["status"] == "EXECUTED"
