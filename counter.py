import asyncio

class Counter:
    def __init__(self, init_value=0):
        self.n = init_value
        self.lock = asyncio.Lock()

    async def increase(self, num: int):
        if num < 0:
            raise ValueError

        async with self.lock:
            self.n += num

    async def decrease(self, num: int):
        if num < 0:
            raise ValueError

        async with self.lock:
            self.n -= num

    async def is_eq(self, num: int):
        async with self.lock:
            return self.n == num
