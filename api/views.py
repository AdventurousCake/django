from django.http import JsonResponse
from rest_framework import permissions, filters
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import MsgSerializer, UserSerializer
# from rest_framework.decorators import action

from home_page.models import Message
from core.models import User


class MsgLoadView(APIView):
    throttle_classes = [UserRateThrottle]
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        # paginator
        messages = Message.objects.all()

        # OR serializers.ListSerializer FOR MANY=TRUE
        serializer = MsgSerializer(messages, many=True)

        text = {
            'status': 'ok',
            'data': serializer.data
        }
        return JsonResponse(text)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# alt users ReadOnlyModelViewSet; др юзеры не могут менять данные
class UserViewSetRO(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer


# global permissions dep; необходимо каждый раз передавать token, получив через auth
class UserList(APIView):
    def get(self, request, username):
        users = User.objects.filter(username=username)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# GET http://127.0.0.1:8000/api/v1/msg_search/?search=123
# GET http://127.0.0.1:8000/api/v1/msg_search/?text=236263
# viewset с фильтром и поиском
class MsgSearchViewSet(ModelViewSet):
    queryset = Message.objects.all()

    serializer_class = MsgSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', ]  # 'name'
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    ordering_fields = ['-created_date']


# viewset - multiple actions
class MessagesViewSet(ModelViewSet):
    # queryset = Message.objects.all() # not optimal for author field
    # queryset = Message.objects.all().select_related("author")

    # queryset = Message.objects.all().select_related("author").prefetch_related("groups", "user_permissions") # invalid parameters in prefetch
    # queryset = Message.objects.all().select_related("author").prefetch_related("author.groups", "author.user_permissions") # invalid parameters in prefetch

    # UNDERSCORE
    queryset = Message.objects.all().select_related("author").prefetch_related("author__groups", "author__user_permissions")
    # queryset = Message.objects.all().select_related("author").prefetch_related()
    serializer_class = MsgSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # throttle_classes = [UserRateThrottle]
    # throttle_scope = 'low_request'

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(author=self.request.user)
        else:
            # 401 unauthorized
            print(self.request.user)
            serializer.save(author='unknown')
