import asyncio
from typing import Coroutine
from counter import Counter

class CoroPool:
    def __init__(self, size: int):
        self.size = size
        self.semaphore = asyncio.Semaphore(self.size)
        self.counter = Counter()
        self.num_of_spawn = 0
        self.end_event = asyncio.Event()

    async def _spawn(self, coroutine: Coroutine, future: asyncio.Future):
        async with self.semaphore:
            task = asyncio.create_task(coroutine)
            await task
            future.set_result(task.result())
            await self.counter.increase(1)
            if await self.counter.is_eq(self.num_of_spawn):
                self.end_event.set()

    def spawn(self, coroutine: Coroutine) -> asyncio.Future:
        future = asyncio.Future()
        asyncio.create_task(self._spawn(coroutine, future))
        self.num_of_spawn += 1
        return future

    async def join(self):
        await self.end_event.wait()
