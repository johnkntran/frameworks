from sanic import Sanic
from sanic.response import json, text
import asyncpg

app = Sanic()

@app.route('/')
async def root(request):
    return json({'message': 'Hello, from Sanic!'})

@app.get('/db/<person_id>')
async def db(request, person_id):
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', int(person_id))
    await connection.close()
    return json(dict(record.items()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, workers=6, access_log=False, debug=False)
