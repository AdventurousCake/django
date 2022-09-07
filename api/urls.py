from django.urls import path, include
from rest_framework.authtoken import views
from .views import hello, MessagesViewSet, UserList, MsgSearchViewSet, UserViewSet, MsgLoadView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('msg', MessagesViewSet)
router.register('msg_search', MsgSearchViewSet)

# You cannot add generic Views in routers
# router.register('msg_load', MsgLoadView, basename="Message")

router.register('users', UserViewSet)


# if config.DEV:
#     urlpatterns.append(path())

# порядок важен, частный случай выше
urlpatterns = [
    path('', include(router.urls)),
    path('msg_load/', MsgLoadView.as_view(), name='msg_load'),

    path('hello/', hello),
    path('api-token-auth/', views.obtain_auth_token),
    path('users/<str:username>', UserList.as_view())
]
