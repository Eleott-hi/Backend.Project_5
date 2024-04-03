
import asyncio
from typing import Dict, List
from fastapi import FastAPI
from kafka import KafkaProducer
import json
import random
import time
import httpx
from config import STORE_SERVICE, KAFKA_SERVICE
from schemas import Product


# Инициализация Kafka Producer
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVICE,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


async def get_products() -> List[Product]:
    async with httpx.AsyncClient() as client:
        url = f'http://{STORE_SERVICE}/api/v1/products/'
        res = await client.get(url)

        res.raise_for_status()
        products = res.json()

        return products


async def generate_event():
    products: List[Dict] = await get_products()

    if products:
        product: dict = random.choice(products)
        product["price"] = random.uniform(0, 1000)
        product["available_stock"] = random.randint(0, 100)
        return product


async def main():
    while True:
        try:
            event = await generate_event()

            if event is not None:
                producer.send('product-events', value=event)

        except Exception as e:
            print(e)

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
