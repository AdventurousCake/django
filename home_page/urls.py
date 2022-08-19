from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index_page, name='index'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('ping/', views.ping_req, name='ping'),
    path("signup/", views.SignUp.as_view(), name="signup")
]