import pytest
import time
import statistics

from main import app
from httpx import AsyncClient, ASGITransport
from config import BASE_URL

transport = ASGITransport(app=app)
base_url = BASE_URL


@pytest.mark.asyncio
async def test_performance():
    async with AsyncClient(transport=transport, base_url=base_url) as ac:
        start_times = []  # List to store the start times of requests
        end_times = []  # List to store the end times of requests

        # Loop to create 100 orders
        for _ in range(100):
            start_times.append(time.time())  # Record the start time for the current order
            await ac.post("/orders", json={"symbol": "AAPL", "quantity": 10, "price": 150.0})
            end_times.append(time.time())  # Record the end time for the current order

        # Calculate delays for each order request
        delays = [end - start for start, end in zip(start_times, end_times)]

        # Print the average delay for all requests
        print(f"\nAverage delay: {statistics.mean(delays)}")
        # Print the standard deviation of the delays to understand variability
        print(f"Standard deviation: {statistics.stdev(delays)}")