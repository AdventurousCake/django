from django.urls import path
from . import views

app_name = 'home'

# NOT DRF API
urlpatterns = [
    path('', views.index_page, name='index'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('edit_msg/<int:pk>/', views.edit_msg, name='edit_msg'),
    path('delete_msg/<int:pk>/', views.delete_msg, name='delete_msg'),

    path('msg/', views.msg_list, name='home_msg_list'),

    path('ping/', views.ping_req, name='ping'),
    path("signup/", views.SignUp.as_view(), name="signup"),

    path("users/<int:pk>/", views.UserDetails.as_view(), name="users_details")
]