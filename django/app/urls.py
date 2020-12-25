from django.urls import path
from .views import index, DBView, db

urlpatterns = [
    path('', index, name='index'),
    path('db/', db, name='db'),
    path('db/<int:person_id>/', db, name='db_w_arg'),
    path('db2/', DBView.as_view(), name='db2'),
    path('db2/<int:person_id>/', DBView.as_view(), name='db2_w_arg'),
]
