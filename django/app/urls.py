from django.urls import path
from .views import index, AppView, query

urlpatterns = [
    path('', index, name='index'),
    path('query/', query, name='query'),
    path('query/<int:person_id>/', query, name='query_w_arg'),
    path('rest/', AppView.as_view(), name='rest'),
    path('rest/<int:person_id>/', AppView.as_view(), name='rest_w_arg'),
]
