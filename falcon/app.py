# app.py

# Let's get this party started!
import falcon


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

class QueryResource:
    def on_get(self, req, resp, query):
        resp.data = bytes(query, 'utf8')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
resource = AppResource()
query = QueryResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', resource)
app.add_route('/{query}', query)
