import asyncio
import time
import psycopg2
# from databases import Database
import asyncpg


def time_sync(func):
    def inner(*args, **kwargs):
        t1 = time.time()
        res = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__}: {round((t2-t1)*1000, 1)} ms')
        return res
    return inner

def time_async(coroutine):
    t1 = time.time()
    res = asyncio.run(coroutine)
    # loop = asyncio.get_event_loop()
    # res = loop.run_until_complete(coroutine)
    t2 = time.time()
    print(f'{coroutine.__name__}: {round((t2-t1)*1000, 1)} ms')
    return res

@time_sync
def fetch_sync():
    connection = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM people;")
        res = cursor.fetchall()
    connection.close()
    return res

async def fetch_async():
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    res = await connection.fetch('SELECT * FROM people;')
    await connection.close()
    return res

res_sync = fetch_sync()
res_async = time_async(fetch_async())
