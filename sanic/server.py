from sanic import Sanic
from sanic.response import json, text

app = Sanic()

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.get('/proxy')
async def index(request):
    # This should display external (public) addresses:
    return text(f"{request.remote_addr or None} connected to {request.url_for('index')}\nForwarded: {request.forwarded}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337, access_log=False, debug=False)
