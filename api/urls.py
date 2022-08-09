from django.urls import path
from rest_framework.authtoken import views
from .views import hello

urlpatterns = [
    path('', hello),
    path('api-token-auth/', views.obtain_auth_token)
]