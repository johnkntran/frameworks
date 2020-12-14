from sanic import Sanic
from sanic.response import json, text
import asyncpg

app = Sanic()
app.config.ACCESS_LOG = False

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.get('/proxy')
async def index(request):
    # This should display external (public) addresses:
    return text(f"{request.remote_addr or None} connected to {request.url_for('index')}\nForwarded: {request.forwarded}")

@app.get('/db/<person_id>')
async def db(request, person_id):
    # async with Database('postgresql://postgres:postgres@postgres:5432/postgres') as database:
    #     row = await database.fetch_one(query='SELECT * FROM people WHERE id = :person_id;', values={'person_id': int(person_id)})
    #     return json(dict(row.items()))
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', int(person_id))
    await connection.close()
    return json(dict(record.items()))

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, workers=6, access_log=False, debug=False)
