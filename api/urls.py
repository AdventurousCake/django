from django.urls import path, include
from rest_framework.authtoken import views
from .views import hello, MessagesViewSet, UserList, MsgList
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('msg', MessagesViewSet)
router.register('msg_search', MsgList)

# if config.DEV:
#     urlpatterns.append(path())

# порядок важен, частный случай выше
urlpatterns = [
    path('', include(router.urls)),
    path('', hello),
    path('api-token-auth/', views.obtain_auth_token),
    path('users/<str:username>', UserList.as_view())
]
