# app.py

# Let's get this party started!
import json
import falcon
import psycopg2


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class AppResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = '{"message": "Hello, World!"}'

class DBResource:
    def on_get(self, req, resp, people_id):
        conn = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, name, age FROM people WHERE id = %s;', (people_id,))
            res = cursor.fetchone()
        conn.close()
        body = json.dumps({'id': res[0], 'name': res[1], 'age': res[2]})
        resp.status = falcon.HTTP_200
        resp.body = body

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
resource = AppResource()
db = DBResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', resource)
app.add_route('/db/{people_id}', db)

def load_data():
    connection = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS people;')
        cursor.execute('CREATE TABLE people (id SERIAL PRIMARY KEY, name VARCHAR, age INTEGER);')
        cursor.execute("INSERT INTO people(id, name, age) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", (1, 'John', 31))
        cursor.execute("INSERT INTO people(id, name, age) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", (2, 'Kim', 29))
        cursor.execute("INSERT INTO people(id, name, age) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING;", (3, 'Jim', 34))
        cursor.execute("SELECT * FROM people;")
        res = cursor.fetchall()
    connection.commit()
    connection.close()
    return res
