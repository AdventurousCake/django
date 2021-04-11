from django.urls import path
from . import views


app_name = 'simplesite1'
urlpatterns = [
    # ex: /simplesite1/
    path('', views.index, name='index'),
]