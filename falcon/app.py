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
        resp.body = ('Two things awe me most, the starry sky '
                     'above me and the moral law within me.'
                     '\n\n'
                     '    ~ Immanuel Kant')

class ParamResource:
    def on_get(self, req, resp, query):
        resp.data = bytes(query, 'utf8')

class DBResource:
    def on_get(self, req, resp, people_id=1):
        conn = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, name, age FROM people WHERE id = %s;', (people_id,))
            res = cursor.fetchone()
        conn.close()
        if not res:
            raise falcon.HTTPInvalidParam('Object not found', f'people_id={people_id}')
        resp.set_header('Powered-By', 'Falcon')
        body = json.dumps({'id': res[0], 'name': res[1], 'age': res[2]})
        resp.body = body
        resp.status = falcon.HTTP_200

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
resource = AppResource()
query = ParamResource()
db = DBResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', resource)
app.add_route('/{query}', query)
app.add_route('/db', db)
app.add_route('/db/{people_id}', db)

def load_data():
    connection = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
    with connection.cursor() as cursor:
        cursor.execute('DROP TABLE IF EXISTS people;')
        cursor.execute('CREATE TABLE people (id SERIAL PRIMARY KEY, name VARCHAR, age INTEGER);')
        cursor.execute("INSERT INTO people(id, name, age) VALUES (1, 'John', 31) ON CONFLICT (id) DO NOTHING;")
        cursor.execute("INSERT INTO people(id, name, age) VALUES (2, 'Kim', 29) ON CONFLICT (id) DO NOTHING;")
        cursor.execute("INSERT INTO people(id, name, age) VALUES (3, 'Jim', 34) ON CONFLICT (id) DO NOTHING;")
        cursor.execute("SELECT * FROM people;")
        res = cursor.fetchall()
    connection.commit()
    return res
