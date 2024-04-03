import asyncio
from fastapi import FastAPI, WebSocket
import time
from kafka import KafkaConsumer
import json
from typing import Dict
from config import KAFKA_SERVICE, STORE_SERVICE
import httpx

app = FastAPI(
    title="Gateway service",
    description="Service for sending events to other services and receiving them from Kafka broker",
    version="1.0.0",
    root_path="/gateway_service",
)

consumer = KafkaConsumer(
    'product-events',
    bootstrap_servers=[KAFKA_SERVICE],
    group_id='product-consumer-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

last_event=None


async def process_event(event: Dict):
    print("Received event:", event, flush=True)

    async with httpx.AsyncClient() as client:
        url = f'http://{STORE_SERVICE}/api/v1/products/{event["id"]}?price={event["price"]}&available_stock={event["available_stock"]}'
        res = await client.patch(url)

        res.raise_for_status()

        print("Database updated successfully", flush=True)


async def consume_events():
    for message in consumer:
        event = message.value
        await process_event(event)
        time.sleep(5)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.(last_event)

        time.sleep(5)


async def main():
    await consume_events()

if __name__ == "__main__":
    asyncio.run(main())
