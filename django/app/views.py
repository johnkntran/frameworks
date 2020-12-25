from django.http import JsonResponse
import psycopg2
import asyncpg
from rest_framework.views import APIView
from rest_framework.response import Response

async def index(request):
    return JsonResponse({'message': 'Hello, from Django!'})

class DBView(APIView):

    def get(self, request, person_id: int = 1):
        request.query_params['format'] = 'json'
        conn = psycopg2.connect('host=postgres dbname=postgres user=postgres password=postgres')
        with conn.cursor() as cursor:
            cursor.execute('SELECT id, name, age FROM people WHERE id = %s;', (person_id,))
            res = cursor.fetchone()
        conn.close()
        body = {'id': res[0], 'name': res[1], 'age': res[2]}
        return Response(data=body, status=200)

async def db(request, person_id: int = 1):
    connection = await asyncpg.connect(user='postgres', password='postgres', database='postgres', host='postgres')
    record = await connection.fetchrow('SELECT * FROM people WHERE id = $1;', int(person_id))
    await connection.close()
    return JsonResponse(dict(record.items()))
