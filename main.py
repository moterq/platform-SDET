from fastapi import FastAPI, WebSocket, BackgroundTasks
from pydantic import BaseModel
from typing import Dict
import random
import asyncio
from fastapi.exceptions import HTTPException

app = FastAPI()

orders_db: Dict[int, Dict] = {}


class Order(BaseModel):
    symbol: str
    quantity: int
    price: float


@app.get("/orders")
async def get_orders():
    return orders_db


@app.post("/orders")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    order_id = random.randint(1000, 9999)
    orders_db[order_id] = {"order": order.model_dump(), "status": "PENDING"}

    # Schedule the status change to EXECUTED as a background task
    background_tasks.add_task(change_order_status, order_id)

    return {"order_id": order_id, "status": "PENDING"}


async def change_order_status(order_id: int):
    await asyncio.sleep(random.uniform(0.1, 1.0))  # Simulate processing time
    if order_id in orders_db:
        orders_db[order_id]["status"] = "EXECUTED"
        await notify_clients(order_id, "EXECUTED")  # Notify clients of the status change


@app.get("/orders/{order_id}")
async def get_order(order_id: int):
    order = orders_db.get(order_id)
    if order:
        return {"order_id": order_id, **order}
    raise HTTPException(status_code=404, detail="Order not found")


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    if order_id in orders_db:
        if orders_db[order_id]["status"] == "PENDING":
            del orders_db[order_id]
            await notify_clients(order_id, "CANCELLED")
            return {"message": "Order canceled and deleted"}
        else:
            raise HTTPException(status_code=400, detail="Order cannot be cancelled and deleted once it is EXECUTED")
    raise HTTPException(status_code=404, detail="Order not found")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You wrote: {data}")


async def notify_clients(order_id: int, status: str):
    # Implement a method to notify all connected WebSocket clients
    # This function will loop through connected clients and send them the status update
    pass
