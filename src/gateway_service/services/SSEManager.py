
import asyncio
from collections import deque
import json
from typing import Deque
from singleton_decorator import singleton


@singleton
class SSEManager():

    def __init__(self):
        self.buffer: Deque = deque()

    def append_data(self, data):
        self.buffer.append(data)

    async def streaming(self):
        data = (
            "event: product_update\n"
            f"data: None\n\n"
        )

        while True:
            if self.buffer:
                data = self.buffer.popleft()
                data = (
                    "event: product_update\n"
                    f"data: {json.dumps(data)}\n\n"
                )

            yield data

            await asyncio.sleep(0.1)
