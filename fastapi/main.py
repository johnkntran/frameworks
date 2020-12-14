from typing import Optional

from fastapi import FastAPI
import asyncpg

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello, World!'}

@app.get('/db/{person_id}')
async def db(person_id: int):
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', person_id)
    await connection.close()
    return dict(record.items())
