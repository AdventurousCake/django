from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('<username>', views.user_detail, name='user_detail'),
    path('follow/', views.user_follow, name='user_follow'),
]