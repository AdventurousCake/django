from django.urls import path, include
from rest_framework.authtoken import views
from .views import hello, MessagesViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('msg', MessagesViewSet)



urlpatterns = [
    path('', hello),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]