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
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', person_id)
    await connection.close()
    return dict(record.items())
