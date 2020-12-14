from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import asyncpg

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get('/')
async def root():
    return {'message': 'Hello, World!'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: Optional[str] = None):
    return {'item_id': item_id, 'q': q}

@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}

@app.get('/db/{person_id}')
async def db(person_id: int):
    # async with Database('postgresql://postgres:postgres@postgres:5432/postgres') as database:
    #     row = await database.fetch_one(query='SELECT * FROM people WHERE id = :person_id;', values={'person_id': person_id})
    #     return dict(row.items())
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', person_id)
    await connection.close()
    return dict(record.items())

async def load_data():
    from databases import Database
    async with Database('postgresql://postgres:postgres@postgres:5432/postgres') as database:
        execution = await database.execute(query='DROP TABLE IF EXISTS people;')
        execution = await database.execute(query='CREATE TABLE people (id SERIAL PRIMARY KEY, name VARCHAR, age INTEGER);')
        execution = await database.execute_many(query='INSERT INTO people(id, name, age) VALUES (:id, :name, :age) ON CONFLICT (id) DO NOTHING;', values=[
            {'id': 1, 'name': 'John', 'age': 31},
            {'id': 2, 'name': 'Kim', 'age': 29},
            {'id': 3, 'name': 'Jim', 'age': 34},
        ])
        rows = await database.fetch_all(query='SELECT * FROM people;')
        return rows
