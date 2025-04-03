from coro_pool import CoroPool
import asyncio
from random import randint
POOL_SIZE = 20

pool = CoroPool(POOL_SIZE)
futures = []
async def worker(i: int):
    await asyncio.sleep(randint(0, 1))
    print(f"task {i} finishes")
    return i

async def main():
    todo = range(20)
    for i in todo:
        future = pool.spawn(worker(i))
        futures.append(future)
    await pool.join()
    assert sum(todo) == sum([ f.result() for f in futures])

asyncio.run(main())
